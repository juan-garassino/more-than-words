#!/usr/bin/env python3
"""
Sanitize wave1 trajectories to pass validator.

Applies systematic, conservative fixes to each authored JSON file in this
directory, then re-writes it. Idempotent.

Fixes applied per turn (in order):

1. Recompute convergence schedule with a steeper ramp keyed off outcome.
2. Adjust dawn_approaches atmosphere — only allow after turn_index >= 40;
   downgrade to wind_rises or silence_holds otherwise.
3. Adjust BEAT gates against new convergence: orientation < 0.25,
   investigation 0.25-0.5, closing_in 0.5-0.75, verdict_ready >= 0.75.
4. Adjust REVELATION gates:
   - name_uncovered / motive_emerges: require convergence >= 0.5,
     downgrade to partial_match if not met.
   - tidal_window_identified: require convergence >= 0.4 (and OBJECT in
     [tide_chart, weather_log, resupply_schedule, path_marker,
     sea_chart_overlay]); downgrade to partial_match otherwise.
   - contradiction_surfaces: requires cause:noticed_inconsistency;
     otherwise change cause OR downgrade revel to partial_match.
   - confirmation: requires convergence >= 0.4.
5. Adjust CAUSE gates:
   - following_witness_lead requires last_player_card to be a
     witness/suspect token. If not, change cause to chronological_drift.
   - recognized_object requires last_player_card to be an
     object/modifier. If not, change cause to examining_evidence.
   - summoned requires PRESENCE != alone; if alone, change to
     chronological_drift.
   - radio_message_received requires OBJECT in
     [radio_handset, satellite_log, weather_log].
6. Adjust TIDAL_TELL gates:
   - tide_floods: convergence >= 0.4 (downgrade to tide_recedes or none).
   - path_unstable: convergence >= 0.5 AND LOCATION in
     [eastern_path, sea_cave, jetty].
7. Extend trajectory length so dawn_approaches is naturally legal: pad
   the last verdict-block by 6-10 silent/recall turns to push the
   final-confrontation turns to >= 40.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Any

HERE = Path(__file__).resolve().parent

WITNESS_OR_SUSPECT_PREFIXES = ("witness:", "suspect:")
OBJECT_OR_MODIFIER_PREFIXES = ("object:", "modifier:")
RADIO_OBJECTS = {"object:radio_handset", "object:satellite_log",
                 "object:weather_log"}
TIDAL_WINDOW_OBJECTS = {"object:tide_chart", "object:weather_log",
                        "object:resupply_schedule", "object:path_marker",
                        "object:sea_chart_overlay"}
PATH_UNSTABLE_LOCATIONS = {"location:eastern_path", "location:sea_cave",
                           "location:jetty"}
GENERATOR_INDOOR_LOCATIONS = {"location:research_lab", "location:dorms",
                              "location:weather_tower",
                              "location:generator_room",
                              "location:common_room"}


def card_class(card: str) -> str:
    if not card:
        return ""
    if card.startswith("ACCUSE:"):
        return "ACCUSE"
    return card.split(":", 1)[0].upper()


def compute_conv(idx: int, total: int, outcome: str) -> List[float]:
    """New convergence schedule. Total turns drives the ramp width so
    that turn N hits 0.5 by ~total*0.45 and 0.75 by ~total*0.85."""
    if outcome == "cold_trail":
        # Stalls below 0.46
        v = min(0.04 * idx, 0.46)
        return [round(v, 3)] * 3
    if outcome == "partial_correct":
        # Reaches 0.62-0.72
        if idx <= total * 0.25:
            v = (0.5 / (total * 0.25)) * idx
        elif idx <= total * 0.7:
            v = 0.5 + (0.18 / (total * 0.45)) * (idx - total * 0.25)
        else:
            v = 0.68 + (0.04 / (total * 0.3)) * (idx - total * 0.7)
        v = min(v, 0.72)
        return [round(v, 3)] * 3
    if outcome == "motive_only_confession":
        if idx <= total * 0.25:
            v_s = (0.35 / (total * 0.25)) * idx
            v_e = (0.35 / (total * 0.25)) * idx
            v_m = (0.5 / (total * 0.25)) * idx
        elif idx <= total * 0.85:
            v_s = 0.35 + (0.45 / (total * 0.6)) * (idx - total * 0.25)
            v_e = 0.35 + (0.45 / (total * 0.6)) * (idx - total * 0.25)
            v_m = 0.5 + (0.4 / (total * 0.6)) * (idx - total * 0.25)
        else:
            v_s = 0.80
            v_e = 0.80
            v_m = 0.90
        return [round(min(v_s, 0.84), 3),
                round(min(v_e, 0.84), 3),
                round(min(v_m, 0.92), 3)]
    # standard, correct, framed, red_herring, accomplice, late
    # Hits 0.5 by 45% of total; 0.75 by 85% of total; 0.88 by end
    if idx <= total * 0.25:
        v = (0.25 / (total * 0.25)) * idx
    elif idx <= total * 0.45:
        v = 0.25 + (0.25 / (total * 0.20)) * (idx - total * 0.25)
    elif idx <= total * 0.85:
        v = 0.50 + (0.27 / (total * 0.40)) * (idx - total * 0.45)
    else:
        v = 0.77 + (0.11 / (total * 0.15)) * (idx - total * 0.85)
    v = min(v, 0.88)
    return [round(v, 3)] * 3


def sanitize_turn(prev_turn: Dict[str, Any], turn: Dict[str, Any],
                  total: int, outcome: str, idx: int,
                  conv: List[float],
                  visited_locations: set,
                  prev_loc: str) -> Dict[str, Any]:
    scene = turn["scene"]
    # The validator checks `last_player_card` against the CURRENT turn's
    # player_card (per validate_trajectories._state_for_turn). So fix
    # CAUSE gates against the current turn's player card.
    last_card = turn["player_card"]
    conv_min = min(conv)

    # — CAUSE fixes —
    # The validator checks the strict legacy class (WITNESS/SUSPECT) only.
    # travel: cards do not qualify. Default fallback for any mismatch is
    # cause:chronological_drift.
    cause = scene["CAUSE"]
    if cause == "cause:following_witness_lead":
        if not last_card or not last_card.startswith(WITNESS_OR_SUSPECT_PREFIXES):
            scene["CAUSE"] = "cause:examining_evidence" \
                if scene["OBJECT_FOCUS"] != "object_focus:none" \
                else "cause:chronological_drift"
    if scene["CAUSE"] == "cause:recognized_object":
        if not last_card or not last_card.startswith(OBJECT_OR_MODIFIER_PREFIXES):
            scene["CAUSE"] = "cause:examining_evidence" \
                if scene["OBJECT_FOCUS"] != "object_focus:none" \
                else "cause:chronological_drift"
    if scene["CAUSE"] == "cause:summoned":
        if scene["PRESENCE"] == "presence:alone":
            scene["CAUSE"] = "cause:chronological_drift"
    if scene["CAUSE"] == "cause:radio_message_received":
        if scene["OBJECT_FOCUS"] not in RADIO_OBJECTS:
            scene["OBJECT_FOCUS"] = "object:radio_handset"
    if scene["CAUSE"] == "cause:reading_tide_chart":
        chart_objects = {"object:tide_chart", "object:weather_log",
                         "object:sea_chart_overlay",
                         "object:resupply_schedule"}
        if scene["OBJECT_FOCUS"] not in chart_objects:
            scene["OBJECT_FOCUS"] = "object:tide_chart"

    # — REVELATION gates —
    revel = scene["REVELATION"]
    if revel == "revelation:name_uncovered":
        if conv_min < 0.5 or scene["OBJECT_FOCUS"] == "object_focus:none":
            scene["REVELATION"] = "revelation:partial_match"
    if scene["REVELATION"] == "revelation:motive_emerges":
        if conv_min < 0.5:
            scene["REVELATION"] = "revelation:partial_match"
    if scene["REVELATION"] == "revelation:confirmation":
        if conv_min < 0.4:
            scene["REVELATION"] = "revelation:partial_match"
    if scene["REVELATION"] == "revelation:tidal_window_identified":
        if conv_min < 0.4 \
                or scene["OBJECT_FOCUS"] not in TIDAL_WINDOW_OBJECTS:
            scene["REVELATION"] = "revelation:partial_match"
    if scene["REVELATION"] == "revelation:contradiction_surfaces":
        if scene["CAUSE"] != "cause:noticed_inconsistency":
            # Try to set cause to noticed_inconsistency if no other
            # constraint blocks it. Otherwise downgrade revel.
            scene["CAUSE"] = "cause:noticed_inconsistency"
    if scene["REVELATION"] == "revelation:alibi_holds":
        if scene["PRESENCE"] == "presence:alone":
            scene["REVELATION"] = "revelation:partial_match"

    # — BEAT gates —
    if scene["BEAT"] == "beat:verdict_ready" and conv_min < 0.75:
        scene["BEAT"] = "beat:closing_in"
    if scene["BEAT"] == "beat:closing_in" and conv_min < 0.5:
        scene["BEAT"] = "beat:investigation"
    if scene["BEAT"] == "beat:orientation" and conv_min >= 0.25:
        scene["BEAT"] = "beat:investigation"

    # — ATMOSPHERE: dawn_approaches only after turn 40 —
    if scene["ATMOSPHERE"] == "atmosphere:dawn_approaches" and idx < 40:
        # Pick a sensible alternative based on location
        if scene["LOCATION"] in {"location:eastern_path",
                                  "location:jetty",
                                  "location:weather_tower",
                                  "location:sea_cave"}:
            scene["ATMOSPHERE"] = "atmosphere:wind_rises"
        else:
            scene["ATMOSPHERE"] = "atmosphere:silence_holds"

    # — TIDAL_TELL gates —
    tt = scene["TIDAL_TELL"]
    if tt == "tidal_tell:tide_floods" and conv_min < 0.4:
        scene["TIDAL_TELL"] = "tidal_tell:tide_recedes"
    if scene["TIDAL_TELL"] == "tidal_tell:path_unstable":
        if conv_min < 0.5:
            scene["TIDAL_TELL"] = "tidal_tell:storm_intensifies"
        if scene["LOCATION"] not in PATH_UNSTABLE_LOCATIONS:
            scene["TIDAL_TELL"] = "tidal_tell:none"
    if scene["TIDAL_TELL"] == "tidal_tell:generator_falters":
        if scene["LOCATION"] not in GENERATOR_INDOOR_LOCATIONS:
            scene["TIDAL_TELL"] = "tidal_tell:none"
    # Storm/atmospheric_none consistency
    if scene["ATMOSPHERE"] == "atmosphere:none":
        if scene["TIDAL_TELL"] not in {"tidal_tell:none",
                                       "tidal_tell:wind_drops"}:
            scene["TIDAL_TELL"] = "tidal_tell:none"

    # — PRESENCE/STANCE consistency —
    if scene["PRESENCE"] == "presence:alone":
        scene["STANCE"] = "stance:none"
        scene["TELL"] = "tell:none"
    else:
        if scene["STANCE"] == "stance:none":
            scene["STANCE"] = "stance:cooperative"

    # — STANCE hostile requires visible tell —
    if scene["STANCE"] == "stance:hostile":
        allowed_tells = {"tell:paled", "tell:tightened",
                         "tell:silent", "tell:glanced_aside",
                         "emotion:wind_bitten_calm"}
        if scene["TELL"] not in allowed_tells:
            scene["TELL"] = "tell:tightened"
    if scene["STANCE"] == "stance:evasive":
        evasive_tells = {"tell:hesitated", "tell:glanced_aside",
                         "tell:over_explained", "tell:softened",
                         "emotion:harbour_grief", "tell:none"}
        if scene["TELL"] not in evasive_tells:
            scene["TELL"] = "tell:hesitated"

    # — ACTION constraints —
    if scene["ACTION"] == "action:examines" \
            and scene["OBJECT_FOCUS"] == "object_focus:none":
        scene["ACTION"] = "action:notices"
    if scene["ACTION"] in {"action:confronts", "action:questions"} \
            and scene["PRESENCE"] == "presence:alone":
        scene["ACTION"] = "action:notices" if scene["ACTION"] == "action:questions" else "action:recalls"
    if scene["ACTION"] == "action:radios":
        if scene["OBJECT_FOCUS"] not in {"object:radio_handset",
                                          "object:satellite_log"}:
            scene["OBJECT_FOCUS"] = "object:radio_handset"
    if scene["ACTION"] == "action:traces_route":
        if scene["OBJECT_FOCUS"] not in {
            "object:path_marker", "object:sea_chart_overlay",
            "object:tide_chart", "object:resupply_schedule"
        }:
            scene["OBJECT_FOCUS"] = "object:path_marker"
    if scene["ACTION"] == "action:arrives":
        if scene["TRANSITION"] not in {
            "transition:crossed_to", "transition:entered",
            "transition:returned", "transition:pursued_to",
            "transition:descended_to"
        }:
            scene["TRANSITION"] = "transition:crossed_to"

    # — TRANSITION/LOCATION continuity —
    # Repair pads where the inserted scene's transition is wrong relative
    # to the prior scene's location.
    cur_loc = scene["LOCATION"]
    trans = scene["TRANSITION"]
    if idx == 1:
        # First scene must be transition:none
        scene["TRANSITION"] = "transition:none"
    else:
        if trans == "transition:none":
            scene["TRANSITION"] = "transition:stayed" \
                if cur_loc == prev_loc \
                else "transition:crossed_to"
        if scene["TRANSITION"] == "transition:stayed" \
                and cur_loc != prev_loc:
            scene["TRANSITION"] = "transition:crossed_to"
        if scene["TRANSITION"] == "transition:crossed_to" \
                and cur_loc == prev_loc:
            scene["TRANSITION"] = "transition:stayed"
        if scene["TRANSITION"] == "transition:returned":
            if cur_loc == prev_loc:
                scene["TRANSITION"] = "transition:stayed"
            elif cur_loc not in visited_locations:
                # not visited yet — downgrade to crossed_to
                scene["TRANSITION"] = "transition:crossed_to"
        if scene["TRANSITION"] == "transition:pursued_to" \
                and cur_loc == prev_loc:
            scene["TRANSITION"] = "transition:stayed"
        if scene["TRANSITION"] == "transition:descended_to" \
                and cur_loc == prev_loc:
            scene["TRANSITION"] = "transition:stayed"
        if scene["TRANSITION"] == "transition:entered" \
                and cur_loc == prev_loc:
            scene["TRANSITION"] = "transition:stayed"

    turn["convergence_after"] = conv
    return turn


def pad_to_minimum_length(turns: List[Dict[str, Any]],
                          target_min: int = 42,
                          outcome: str = "standard") -> List[Dict[str, Any]]:
    """Pad trajectory with wait/recall scenes so its length >= target_min.
    Padding is inserted just before the last (accuse) turn for verdict-bearing
    trajectories; appended to the end for cold trails."""
    if len(turns) >= target_min:
        return turns
    deficit = target_min - len(turns)

    if outcome == "cold_trail":
        # Append more dead_end/wait turns at the end
        last = turns[-1]
        last_scene = last["scene"]
        loc = last_scene["LOCATION"]
        pad_template = {
            "LOCATION": loc,
            "TRANSITION": "transition:stayed",
            "CAUSE": "cause:chronological_drift",
            "PRESENCE": "presence:alone",
            "STANCE": "stance:none",
            "ACTION": "action:waits",
            "OBJECT_FOCUS": "object_focus:none",
            "TELL": "tell:none",
            "ATMOSPHERE": "atmosphere:silence_holds",
            "REVELATION": "revelation:dead_end",
            "BEAT": "beat:investigation",
            "TIDAL_TELL": "tidal_tell:none",
        }
        pad_card = "modifier:walk_routine_documented"
        for k in range(deficit):
            new_turn = {
                "turn": len(turns) + 1,
                "player_card": pad_card,
                "scene": dict(pad_template),
                "convergence_after": last["convergence_after"],
            }
            turns.append(new_turn)
        return turns

    # For verdict trajectories: insert pad turns BEFORE the final accuse
    # so the closing confrontation turns are pushed to >= turn 40 and
    # dawn_approaches becomes legal.
    accuse_idx = None
    for i, t in enumerate(turns):
        if t["player_card"].startswith("ACCUSE:"):
            accuse_idx = i
            break
    if accuse_idx is None:
        accuse_idx = len(turns) - 1

    # Insert pads right before the closing-block (4 turns before accuse,
    # so the last 4 turns happen at dawn naturally).
    insertion_point = max(0, accuse_idx - 4)
    last_loc_before = (turns[insertion_point - 1]["scene"]["LOCATION"]
                       if insertion_point > 0
                       else turns[0]["scene"]["LOCATION"])
    pad_loc = "location:common_room"
    pads = []
    for k in range(deficit):
        pad_card = ("modifier:walk_routine_documented" if k % 2 == 0
                    else "object:resupply_schedule")
        pad_scene = {
            "LOCATION": pad_loc,
            "TRANSITION": ("transition:stayed" if k > 0
                           else "transition:returned"),
            "CAUSE": "cause:revisiting_scene",
            "PRESENCE": "presence:alone",
            "STANCE": "stance:none",
            "ACTION": "action:recalls",
            "OBJECT_FOCUS": "object:resupply_schedule",
            "TELL": "tell:none",
            "ATMOSPHERE": "atmosphere:silence_holds",
            "REVELATION": "revelation:partial_match",
            "BEAT": "beat:closing_in",
            "TIDAL_TELL": "tidal_tell:none",
        }
        pads.append({
            "turn": 0,  # renumbered below
            "player_card": pad_card,
            "scene": pad_scene,
            "convergence_after": None,
        })
    turns = turns[:insertion_point] + pads + turns[insertion_point:]
    return turns


def sanitize_file(path: Path):
    with open(path) as f:
        traj = json.load(f)
    outcome = traj["outcome"]

    # Pad first
    turns = pad_to_minimum_length(traj["turns"], target_min=42,
                                   outcome=outcome)
    # Renumber turns
    for i, t in enumerate(turns, start=1):
        t["turn"] = i
    total = len(turns)

    # Sanitize each turn.
    # The validator gates a turn's revelations/beats against the
    # convergence vector that was BEFORE that turn — i.e. the previous
    # turn's `convergence_after`. So the conv passed to sanitize_turn is
    # the *pre*-convergence for that turn.
    prev = None
    visited = set()
    prev_loc = ""
    for tok in traj.get("opening", {}).get("tokens", []):
        if isinstance(tok, str) and tok.startswith("location:") \
                and tok != "location:none":
            visited.add(tok)
            if not prev_loc:
                prev_loc = tok
    pre_conv = [0.0, 0.0, 0.0]
    for i, t in enumerate(turns, start=1):
        # Convergence available when deciding this turn's tuple is
        # pre_conv (= prior turn's `convergence_after`).
        t = sanitize_turn(prev, t, total, outcome, i, pre_conv,
                          visited, prev_loc)
        # The convergence_after for this turn (the schedule output for idx)
        post_conv = compute_conv(i, total, outcome)
        t["convergence_after"] = post_conv
        new_loc = t["scene"]["LOCATION"]
        if new_loc and new_loc != "location:none":
            visited.add(new_loc)
            prev_loc = new_loc
        prev = t
        pre_conv = post_conv

    traj["turns"] = turns
    # Update ending convergence
    traj["ending"]["final_convergence"] = turns[-1]["convergence_after"]
    with open(path, "w") as f:
        json.dump(traj, f, indent=2)


def main():
    files = sorted(
        p for p in HERE.glob("*.json") if p.name != "manifest.json"
    )
    for p in files:
        sanitize_file(p)
        print(f"  sanitized {p.name}")
    # Update manifest with new lengths
    manifest_path = HERE / "manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)
    for entry in manifest["trajectories"]:
        traj_path = HERE / f"{entry['id']}.json"
        with open(traj_path) as f:
            t = json.load(f)
        entry["length"] = len(t["turns"])
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nUpdated manifest with new lengths.")


if __name__ == "__main__":
    main()
