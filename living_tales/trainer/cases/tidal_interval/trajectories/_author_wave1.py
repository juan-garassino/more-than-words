#!/usr/bin/env python3
"""
Authoring helper for tidal_interval — Wave 1 (25 trajectories).

Compact specification language: each trajectory is a list of dim-tuple
fragments produced by short helper builders. The script renders 25 JSON
files + manifest.json into the trajectories/ directory.

Run once:
    python3 living_tales/trainer/cases/tidal_interval/trajectories/_author_wave1.py
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple

HERE = Path(__file__).resolve().parent

# Opening tokens — these seed `previous_locations` for the validator. We
# use a starting location that matches a real V2 vocab location so the
# very-first transition can be transition:none and the second turn can
# transition:stayed without violating @equals_previous_scene_location.
DEFAULT_OPENING = {
    "tokens": [
        "location:research_lab",
        "event:sarah_does_not_return",
        "event:final_report_approved",
    ]
}


# ─── Convergence schedules ───────────────────────────────────────────────
def conv_after(idx: int, ramp: str = "standard") -> List[float]:
    """Return convergence vector for turn idx (1-indexed)."""
    if ramp == "cold":
        if idx <= 5:
            v = 0.04 * idx
        elif idx <= 22:
            v = 0.20 + 0.011 * (idx - 5)
        else:
            v = 0.385 + 0.004 * (idx - 22)
        v = min(v, 0.46)
    elif ramp == "partial":
        if idx <= 8:
            v = 0.03 * idx
        elif idx <= 25:
            v = 0.24 + 0.018 * (idx - 8)
        else:
            v = 0.55 + 0.009 * (idx - 25)
        v = min(v, 0.71)
    elif ramp == "framed":
        if idx <= 6:
            v = 0.04 * idx
        elif idx <= 22:
            v = 0.24 + 0.022 * (idx - 6)
        else:
            v = 0.59 + 0.014 * (idx - 22)
        v = min(v, 0.84)
    elif ramp == "late":
        if idx <= 12:
            v = 0.02 * idx
        elif idx <= 30:
            v = 0.24 + 0.012 * (idx - 12)
        else:
            v = 0.46 + 0.030 * (idx - 30)
        v = min(v, 0.86)
    elif ramp == "red_herring":
        if idx <= 6:
            v = 0.04 * idx
        elif idx <= 25:
            v = 0.24 + 0.024 * (idx - 6)
        else:
            v = 0.696 + 0.011 * (idx - 25)
        v = min(v, 0.83)
    elif ramp == "motive_only":
        if idx <= 8:
            v = 0.03 * idx
        elif idx <= 25:
            v = 0.24 + 0.020 * (idx - 8)
        else:
            v = 0.58 + 0.014 * (idx - 25)
        v = min(v, 0.83)
    elif ramp == "accomplice":
        if idx <= 7:
            v = 0.035 * idx
        elif idx <= 25:
            v = 0.245 + 0.021 * (idx - 7)
        else:
            v = 0.623 + 0.014 * (idx - 25)
        v = min(v, 0.87)
    else:  # standard — correct trajectory
        if idx <= 7:
            v = 0.035 * idx
        elif idx <= 25:
            v = 0.245 + 0.020 * (idx - 7)
        elif idx <= 35:
            v = 0.605 + 0.018 * (idx - 25)
        else:
            v = 0.785 + 0.009 * (idx - 35)
        v = min(v, 0.88)
    return [round(v, 3), round(v, 3), round(v, 3)]


# ─── Scene constructor ───────────────────────────────────────────────────
def S(loc, trans, cause, presence, stance, action, obj, tell, atmos,
      revel, beat, tidal_tell="tidal_tell:none"):
    return {
        "LOCATION":     loc,
        "TRANSITION":   trans,
        "CAUSE":        cause,
        "PRESENCE":     presence,
        "STANCE":       stance,
        "ACTION":       action,
        "OBJECT_FOCUS": obj,
        "TELL":         tell,
        "ATMOSPHERE":   atmos,
        "REVELATION":   revel,
        "BEAT":         beat,
        "TIDAL_TELL":   tidal_tell,
    }


# ─── Helper shortcuts ────────────────────────────────────────────────────
# Beat helper — auto-pick BEAT based on turn index (under standard ramp).
def beat_for(idx: int, ramp: str = "standard") -> str:
    # Use the projected convergence to gate
    v = conv_after(idx, ramp)[0]
    if v < 0.25:
        return "beat:orientation"
    if v < 0.5:
        return "beat:investigation"
    if v < 0.75:
        return "beat:closing_in"
    return "beat:verdict_ready"


# Common scene-tuple shortcuts (use full S() in the trajectory body for
# clarity; helpers only for very common patterns).
def cold_examine(loc, obj, atmos, revel, beat,
                 trans="transition:stayed",
                 cause="cause:examining_evidence",
                 tidal="tidal_tell:none"):
    return S(loc, trans, cause, "presence:alone", "stance:none",
             "action:examines", obj, "tell:none", atmos, revel, beat, tidal)


def cross_to_examine(loc, obj, atmos, revel, beat,
                     cause="cause:examining_evidence",
                     tidal="tidal_tell:none"):
    return S(loc, "transition:crossed_to", cause, "presence:alone",
             "stance:none", "action:examines", obj, "tell:none",
             atmos, revel, beat, tidal)


def return_to_examine(loc, obj, atmos, revel, beat,
                      cause="cause:revisiting_scene",
                      tidal="tidal_tell:none"):
    return S(loc, "transition:returned", cause, "presence:alone",
             "stance:none", "action:examines", obj, "tell:none",
             atmos, revel, beat, tidal)


def cross_to_question(loc, presence, obj, atmos, revel, beat,
                      stance="stance:cooperative", tell="tell:none",
                      cause="cause:following_witness_lead",
                      tidal="tidal_tell:none"):
    return S(loc, "transition:crossed_to", cause, presence, stance,
             "action:questions", obj, tell, atmos, revel, beat, tidal)


def stay_question(loc, presence, obj, atmos, revel, beat,
                  stance="stance:cooperative", tell="tell:none",
                  cause="cause:following_witness_lead",
                  tidal="tidal_tell:none"):
    return S(loc, "transition:stayed", cause, presence, stance,
             "action:questions", obj, tell, atmos, revel, beat, tidal)


def return_to_question(loc, presence, obj, atmos, revel, beat,
                       stance="stance:defensive", tell="tell:tightened",
                       cause="cause:noticed_inconsistency",
                       tidal="tidal_tell:none"):
    return S(loc, "transition:returned", cause, presence, stance,
             "action:questions", obj, tell, atmos, revel, beat, tidal)


def confront_npc(loc, presence, obj, atmos, revel, beat,
                 trans="transition:stayed",
                 tell="tell:tightened",
                 cause="cause:pursued_suspicion",
                 tidal="tidal_tell:none"):
    return S(loc, trans, cause, presence, "stance:hostile",
             "action:confronts", obj, tell, atmos, revel, beat, tidal)


def recall_alone(loc, obj, atmos, revel, beat,
                 trans="transition:stayed",
                 cause="cause:recognized_object",
                 tidal="tidal_tell:none"):
    return S(loc, trans, cause, "presence:alone", "stance:none",
             "action:recalls", obj, "tell:none", atmos, revel, beat, tidal)


def discover_alone(loc, obj, atmos, revel, beat,
                   trans="transition:stayed",
                   cause="cause:recognized_object",
                   tidal="tidal_tell:none"):
    return S(loc, trans, cause, "presence:alone", "stance:none",
             "action:discovers", obj, "tell:none", atmos, revel, beat, tidal)


def trace_route(loc, obj, atmos, revel, beat,
                trans="transition:returned",
                cause="cause:revisiting_scene",
                tidal="tidal_tell:path_unstable"):
    return S(loc, trans, cause, "presence:alone", "stance:none",
             "action:traces_route", obj, "tell:none", atmos, revel, beat,
             tidal)


def radio_in(loc, atmos, revel, beat,
             obj="object:radio_handset",
             trans="transition:stayed",
             cause="cause:radio_message_received",
             tidal="tidal_tell:radio_breaks_static"):
    return S(loc, trans, cause, "presence:alone", "stance:none",
             "action:radios", obj, "tell:none", atmos, revel, beat, tidal)


def wait_alone(loc, atmos, beat, tidal="tidal_tell:none"):
    return S(loc, "transition:stayed", "cause:chronological_drift",
             "presence:alone", "stance:none", "action:waits",
             "object_focus:none", "tell:none", atmos, "revelation:none",
             beat, tidal)


def accuse_scene(loc, presence, obj="object_focus:none",
                 atmos="atmosphere:dawn_approaches",
                 revel="revelation:confirmation"):
    return S(loc, "transition:stayed", "cause:pursued_suspicion",
             presence, "stance:hostile", "action:confronts", obj,
             "tell:tightened", atmos, revel, "beat:verdict_ready",
             "tidal_tell:none")


# ─── Trajectory finalizer ────────────────────────────────────────────────
def finalize(turns_with_cards: List[Tuple[str, Dict]],
             ramp: str = "standard") -> List[Dict]:
    """Attach turn numbers + convergence_after to a list of (player_card, scene)."""
    out = []
    for i, (card, scene) in enumerate(turns_with_cards, start=1):
        out.append({
            "turn": i,
            "player_card": card,
            "scene": scene,
            "convergence_after": conv_after(i, ramp),
        })
    return out


def trajectory(traj_id, description, outcome, starting_hypothesis,
               tags, turns_specs, ramp="standard", accused=None):
    turns = finalize(turns_specs, ramp=ramp)
    if accused is None:
        # default: derive from outcome
        if outcome.startswith("correct_"):
            accused = "suspect:" + outcome.replace("correct_", "", 1)
        elif outcome.startswith("wrong_"):
            accused = "suspect:" + outcome.replace("wrong_", "", 1)
        elif outcome.startswith("framed_"):
            accused = "suspect:" + outcome.replace("framed_", "", 1)
        elif outcome.startswith("partial_"):
            accused = "suspect:piers_dunne"
        elif outcome.startswith("accomplice_"):
            accused = "suspect:piers_dunne"
        elif outcome == "late_revelation":
            accused = "suspect:piers_dunne"
        elif outcome == "motive_only_confession":
            accused = "suspect:piers_dunne"
        elif outcome == "red_herring_trap":
            accused = "suspect:marcus_webb"
        else:
            accused = None
    last_conv = turns[-1]["convergence_after"]
    ending = {
        "type": ("all_strong" if outcome.startswith("correct_")
                 else "partial" if outcome.startswith("partial_")
                 else "cold" if outcome == "cold_trail"
                 else "wrong"),
        "accused": accused,
        "final_convergence": last_conv,
    }
    return {
        "schema_version": 1,
        "trajectory_id": traj_id,
        "case_id": "tidal_interval",
        "description": description,
        "outcome": outcome,
        "starting_hypothesis": starting_hypothesis,
        "tags": tags,
        "opening": DEFAULT_OPENING,
        "turns": turns,
        "ending": ending,
    }


# ╔════════════════════════════════════════════════════════════════════╗
# ║  CORRECT — dunne_via_path_marker                                   ║
# ╚════════════════════════════════════════════════════════════════════╝
def dunne_via_path_marker():
    t = []
    # ── Orientation: 1-8 ──
    t.append(("object:path_marker",
              cold_examine("location:research_lab", "object:path_marker",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("event:sarah_does_not_return",
              cold_examine("location:research_lab",
                           "object:research_notebook",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match", "beat:orientation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:orientation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:fresh_soil_on_base",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:orientation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:orientation")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:resupply_schedule",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            cause="cause:recognized_object")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:tide_chart",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               cause="cause:reading_tide_chart")))
    # ── Investigation: 9-25 ──
    t.append(("object:tide_chart",
              cold_examine("location:weather_tower", "object:tide_chart",
                           "atmosphere:wind_rises",
                           "revelation:contradiction_surfaces",
                           "beat:investigation",
                           cause="cause:noticed_inconsistency")))
    t.append(("witness:cook",
              return_to_question("location:common_room",
                                 "presence:with_eira_voss",
                                 "object_focus:none",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:cooperative",
                                 tell="tell:hesitated",
                                 cause="cause:following_witness_lead")))
    t.append(("suspect:piers_dunne",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("object:resupply_schedule",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("witness:generator_engineer",
              cross_to_question("location:generator_room",
                                "presence:with_niall_brackett",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                tidal="tidal_tell:generator_falters")))
    t.append(("modifier:schedule_in_piers_hand",
              stay_question("location:generator_room",
                            "presence:with_niall_brackett",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            cause="cause:recognized_object",
                            tidal="tidal_tell:generator_falters")))
    t.append(("travel:to_eastern_path",
              return_to_examine("location:eastern_path", "object:path_marker",
                                "atmosphere:wind_rises",
                                "revelation:contradiction_surfaces",
                                "beat:investigation",
                                cause="cause:noticed_inconsistency",
                                tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:socket_hole_compressed",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("object:radio_handset",
              radio_in("location:eastern_path",
                       "atmosphere:wind_rises",
                       "revelation:partial_match", "beat:investigation",
                       tidal="tidal_tell:radio_breaks_static")))
    t.append(("travel:to_weather_tower",
              return_to_examine("location:weather_tower", "object:tide_chart",
                                "atmosphere:wind_rises",
                                "revelation:tidal_window_identified",
                                "beat:investigation",
                                cause="cause:reading_tide_chart",
                                tidal="tidal_tell:tide_recedes")))
    t.append(("witness:lighthouse_keeper",
              cross_to_question("location:weather_tower",
                                "presence:with_padraic_burne",
                                "object_focus:none",
                                "atmosphere:wind_rises",
                                "revelation:partial_match",
                                "beat:investigation",
                                tidal="tidal_tell:wind_drops")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:weather_tower",
                            "presence:with_padraic_burne",
                            "object:tide_chart",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:wind_drops")))
    t.append(("travel:to_research_lab",
              return_to_examine("location:research_lab",
                                "object:sea_chart_overlay",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                cause="cause:reading_tide_chart")))
    t.append(("suspect:piers_dunne",
              return_to_question("location:common_room",
                                 "presence:with_piers_dunne",
                                 "object:resupply_schedule",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:defensive",
                                 tell="tell:tightened")))
    t.append(("object:boot_with_fresh_soil",
              cold_examine("location:common_room",
                           "object:boot_with_fresh_soil",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:recognized_object")))
    t.append(("travel:to_eastern_path",
              return_to_examine("location:eastern_path", "object:path_marker",
                                "atmosphere:wind_rises",
                                "revelation:name_uncovered",
                                "beat:closing_in",
                                cause="cause:recognized_object",
                                tidal="tidal_tell:tide_floods")))
    t.append(("object:path_marker",
              trace_route("location:eastern_path", "object:path_marker",
                          "atmosphere:wind_rises",
                          "revelation:tidal_window_identified",
                          "beat:closing_in",
                          trans="transition:stayed",
                          tidal="tidal_tell:path_unstable")))
    # ── Closing-in: 26-38 ──
    t.append(("motive:fishing_economy",
              recall_alone("location:eastern_path", "object:final_report",
                           "atmosphere:wind_rises",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion",
                           tidal="tidal_tell:path_unstable")))
    t.append(("witness:boat_skipper",
              cross_to_question("location:jetty",
                                "presence:with_mira_callan",
                                "object_focus:none",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:closing_in",
                                stance="stance:evasive",
                                tell="tell:hesitated",
                                tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:closing_in",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:path_marker",
                                "atmosphere:silence_holds",
                                "revelation:confirmation",
                                "beat:closing_in",
                                stance="stance:defensive",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:confirmation", "beat:closing_in")))
    t.append(("object:resupply_schedule",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:resupply_schedule",
                           "atmosphere:silence_holds",
                           "revelation:name_uncovered", "beat:closing_in",
                           tell="tell:paled")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:paled",
                           cause="cause:noticed_inconsistency")))
    t.append(("witness:generator_engineer",
              return_to_question("location:generator_room",
                                 "presence:with_niall_brackett",
                                 "object:weather_log",
                                 "atmosphere:silence_holds",
                                 "revelation:confirmation",
                                 "beat:closing_in",
                                 stance="stance:cooperative",
                                 tell="tell:none",
                                 cause="cause:following_witness_lead",
                                 tidal="tidal_tell:generator_falters")))
    # ── Verdict-ready: 35-end ──
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:path_marker",
                                "atmosphere:dawn_approaches",
                                "revelation:confirmation",
                                "beat:verdict_ready",
                                stance="stance:hostile",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:dawn_approaches",
                           "revelation:name_uncovered", "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("modifier:schedule_in_piers_hand",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:resupply_schedule",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges",
                           "beat:verdict_ready",
                           tell="tell:silent",
                           cause="cause:noticed_inconsistency")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:path_marker")))
    return trajectory(
        "dunne_via_path_marker",
        "The detective opens with the displaced path marker, traces the "
        "moved socket to Piers via the resupply schedule in his hand, the "
        "tide chart's forty-minute window, the cook's account of Sarah's "
        "Sunday walk, the boat skipper's evasive admission of having "
        "warned Piers what the report would mean, and confronts him at "
        "dawn in the common room. Path-marker first, evidence-led, "
        "verdict_ready by turn 38.",
        "correct_piers_dunne", "object_first",
        ["path_marker_chain", "marker_displaced", "schedule_in_piers_hand",
         "eastern_path_anchored", "starter_template", "flagship"],
        t, ramp="standard",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  CORRECT — dunne_via_tidal_window                                  ║
# ╚════════════════════════════════════════════════════════════════════╝
def dunne_via_tidal_window():
    t = []
    t.append(("object:tide_chart",
              cold_examine("location:research_lab", "object:tide_chart",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none",
                           cause="cause:reading_tide_chart")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:tide_chart",
                               "atmosphere:rain_against_glass",
                               "revelation:partial_match", "beat:orientation",
                               cause="cause:reading_tide_chart")))
    t.append(("object:weather_log",
              cold_examine("location:weather_tower", "object:weather_log",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           cause="cause:reading_tide_chart")))
    t.append(("modifier:storm_warning_issued",
              cold_examine("location:weather_tower", "object:weather_log",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:orientation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("witness:radio_operator",
              cross_to_question("location:research_lab",
                                "presence:with_kestrel_lin",
                                "object:radio_handset",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:orientation",
                                tidal="tidal_tell:radio_breaks_static")))
    t.append(("object:radio_handset",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:radio_handset",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            cause="cause:radio_message_received",
                            tidal="tidal_tell:radio_breaks_static")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:radio_handset",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            cause="cause:noticed_inconsistency")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("object:path_marker",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:contradiction_surfaces",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_weather_tower",
              return_to_examine("location:weather_tower", "object:tide_chart",
                                "atmosphere:wind_rises",
                                "revelation:tidal_window_identified",
                                "beat:investigation",
                                cause="cause:reading_tide_chart",
                                tidal="tidal_tell:tide_recedes")))
    t.append(("object:sea_chart_overlay",
              cold_examine("location:weather_tower",
                           "object:sea_chart_overlay",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:reading_tide_chart",
                           tidal="tidal_tell:tide_recedes")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:resupply_schedule",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:investigation",
                            cause="cause:recognized_object")))
    t.append(("suspect:piers_dunne",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("object:resupply_schedule",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:schedule_in_piers_hand",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("object:radio_handset",
              radio_in("location:research_lab",
                       "atmosphere:wind_rises",
                       "revelation:partial_match", "beat:investigation")))
    t.append(("witness:lighthouse_keeper",
              cross_to_question("location:weather_tower",
                                "presence:with_padraic_burne",
                                "object_focus:none",
                                "atmosphere:wind_rises",
                                "revelation:partial_match",
                                "beat:investigation",
                                tidal="tidal_tell:wind_drops")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:weather_tower",
                            "presence:with_padraic_burne",
                            "object:tide_chart",
                            "atmosphere:silence_holds",
                            "revelation:tidal_window_identified",
                            "beat:investigation",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:wind_drops")))
    t.append(("travel:to_eastern_path",
              return_to_examine("location:eastern_path", "object:path_marker",
                                "atmosphere:wind_rises",
                                "revelation:name_uncovered",
                                "beat:closing_in",
                                cause="cause:recognized_object",
                                tidal="tidal_tell:tide_floods")))
    t.append(("object:path_marker",
              trace_route("location:eastern_path", "object:path_marker",
                          "atmosphere:wind_rises",
                          "revelation:tidal_window_identified",
                          "beat:closing_in",
                          trans="transition:stayed",
                          tidal="tidal_tell:path_unstable")))
    t.append(("motive:fishing_economy",
              recall_alone("location:eastern_path", "object:final_report",
                           "atmosphere:wind_rises",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion",
                           tidal="tidal_tell:path_unstable")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:tide_chart",
                                "atmosphere:silence_holds",
                                "revelation:confirmation",
                                "beat:closing_in",
                                stance="stance:defensive",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:tide_chart",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:tide_chart",
                           "atmosphere:silence_holds",
                           "revelation:confirmation", "beat:closing_in")))
    t.append(("modifier:tide_data_annotated",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:tide_chart",
                           "atmosphere:silence_holds",
                           "revelation:name_uncovered", "beat:closing_in",
                           tell="tell:paled",
                           cause="cause:noticed_inconsistency")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:paled",
                           cause="cause:noticed_inconsistency")))
    t.append(("witness:boat_skipper",
              cross_to_question("location:jetty",
                                "presence:with_mira_callan",
                                "object_focus:none",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:closing_in",
                                stance="stance:evasive",
                                tell="tell:hesitated",
                                tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:confirmation", "beat:closing_in",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:tide_chart",
                                "atmosphere:dawn_approaches",
                                "revelation:confirmation",
                                "beat:verdict_ready",
                                stance="stance:hostile",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:tide_chart",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:tide_chart",
                           "atmosphere:dawn_approaches",
                           "revelation:name_uncovered",
                           "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges",
                           "beat:verdict_ready",
                           tell="tell:silent",
                           cause="cause:noticed_inconsistency")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation",
                           "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:tide_chart")))
    return trajectory(
        "dunne_via_tidal_window",
        "TIDAL_TELL-heavy chain. The detective works the tide chart, the "
        "weather log, the radio's static, and the sea-chart overlay to "
        "isolate the forty-minute window. The marker, the schedule, and "
        "the loan papers close on Piers in the common room at dawn.",
        "correct_piers_dunne", "object_first",
        ["tidal_window_chain", "weather_tower_heavy",
         "tide_chart_first", "radio_static_heavy", "TIDAL_TELL_rich"],
        t, ramp="standard",
    )


# Each correct trajectory follows the same shape but anchors the chain
# on a different object/witness. Helper to compress code below.

# ╔════════════════════════════════════════════════════════════════════╗
# ║  CORRECT — dunne_via_radio_log                                     ║
# ╚════════════════════════════════════════════════════════════════════╝
def dunne_via_radio_log():
    t = []
    t.append(("object:radio_handset",
              cold_examine("location:research_lab", "object:radio_handset",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("witness:radio_operator",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:radio_handset",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            tidal="tidal_tell:radio_breaks_static")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:radio_handset",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            cause="cause:recognized_object",
                            tidal="tidal_tell:radio_breaks_static")))
    t.append(("object:satellite_log",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            cause="cause:noticed_inconsistency")))
    t.append(("object:radio_handset",
              radio_in("location:research_lab",
                       "atmosphere:wind_rises",
                       "revelation:partial_match", "beat:investigation",
                       trans="transition:stayed")))
    t.append(("witness:lighthouse_keeper",
              radio_in("location:research_lab",
                       "atmosphere:wind_rises",
                       "revelation:partial_match", "beat:investigation",
                       trans="transition:stayed")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:weather_log",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               cause="cause:reading_tide_chart")))
    t.append(("object:tide_chart",
              cold_examine("location:weather_tower", "object:tide_chart",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:reading_tide_chart")))
    t.append(("object:weather_log",
              cold_examine("location:weather_tower", "object:weather_log",
                           "atmosphere:wind_rises",
                           "revelation:tidal_window_identified",
                           "beat:investigation",
                           cause="cause:reading_tide_chart",
                           tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_jetty",
              cross_to_question("location:jetty",
                                "presence:with_mira_callan",
                                "object_focus:none",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:investigation",
                                tidal="tidal_tell:tide_recedes")))
    t.append(("witness:boat_skipper",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object_focus:none",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_research_lab",
              return_to_examine("location:research_lab",
                                "object:satellite_log",
                                "atmosphere:silence_holds",
                                "revelation:contradiction_surfaces",
                                "beat:investigation",
                                cause="cause:noticed_inconsistency")))
    t.append(("witness:radio_operator",
              return_to_question("location:research_lab",
                                 "presence:with_kestrel_lin",
                                 "object:satellite_log",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:cooperative",
                                 tell="tell:hesitated",
                                 cause="cause:following_witness_lead")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("object:path_marker",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:contradiction_surfaces",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("suspect:piers_dunne",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:schedule_in_piers_hand",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:noticed_inconsistency")))
    t.append(("travel:to_eastern_path",
              return_to_examine("location:eastern_path", "object:path_marker",
                                "atmosphere:wind_rises",
                                "revelation:name_uncovered",
                                "beat:closing_in",
                                cause="cause:recognized_object",
                                tidal="tidal_tell:tide_floods")))
    t.append(("object:path_marker",
              trace_route("location:eastern_path", "object:path_marker",
                          "atmosphere:wind_rises",
                          "revelation:tidal_window_identified",
                          "beat:closing_in",
                          trans="transition:stayed",
                          tidal="tidal_tell:path_unstable")))
    t.append(("motive:fishing_economy",
              recall_alone("location:eastern_path", "object:final_report",
                           "atmosphere:wind_rises",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion",
                           tidal="tidal_tell:path_unstable")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:radio_handset",
                                "atmosphere:silence_holds",
                                "revelation:confirmation",
                                "beat:closing_in",
                                stance="stance:defensive",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:satellite_log",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:satellite_log",
                           "atmosphere:silence_holds",
                           "revelation:confirmation", "beat:closing_in")))
    t.append(("modifier:radio_log_blank",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:satellite_log",
                           "atmosphere:silence_holds",
                           "revelation:name_uncovered", "beat:closing_in",
                           tell="tell:paled",
                           cause="cause:noticed_inconsistency")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:paled",
                           cause="cause:noticed_inconsistency")))
    t.append(("witness:generator_engineer",
              cross_to_question("location:generator_room",
                                "presence:with_niall_brackett",
                                "object:weather_log",
                                "atmosphere:silence_holds",
                                "revelation:confirmation",
                                "beat:closing_in",
                                tidal="tidal_tell:generator_falters")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:radio_handset",
                                "atmosphere:dawn_approaches",
                                "revelation:confirmation",
                                "beat:verdict_ready",
                                stance="stance:hostile",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:satellite_log",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:satellite_log",
                           "atmosphere:dawn_approaches",
                           "revelation:name_uncovered",
                           "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges",
                           "beat:verdict_ready",
                           tell="tell:silent",
                           cause="cause:noticed_inconsistency")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:satellite_log")))
    return trajectory(
        "dunne_via_radio_log",
        "Radio-first chain. The detective notes the blank radio log and "
        "the failed satellite uplink during the relevant hour, follows "
        "the silence back to Lin, then triangulates through Callan's "
        "tide times and Brackett's generator entries to the marker and "
        "Piers in the common room.",
        "correct_piers_dunne", "object_first",
        ["radio_log_chain", "satellite_log_first",
         "silent_uplink_pattern", "radio_operator_heavy"],
        t, ramp="standard",
    )


# I'll continue with the remaining 22 trajectories in a compact form.
# Each one will share the bulk of factory work using helpers.

# ╔════════════════════════════════════════════════════════════════════╗
# ║  CORRECT — dunne_via_callan_corroboration                          ║
# ╚════════════════════════════════════════════════════════════════════╝
def dunne_via_callan_corroboration():
    t = []
    t.append(("witness:boat_skipper",
              S("location:research_lab", "transition:none",
                "cause:following_witness_lead", "presence:alone",
                "stance:none", "action:notices", "object_focus:none",
                "tell:none", "atmosphere:rain_against_glass",
                "revelation:none", "beat:orientation",
                "tidal_tell:none"))),
    # Detective stays in lab momentarily, then crosses to jetty
    t.append(("travel:to_jetty",
              cross_to_question("location:jetty",
                                "presence:with_mira_callan",
                                "object_focus:none",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:orientation",
                                tidal="tidal_tell:wind_drops")))
    t.append(("witness:boat_skipper",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:orientation",
                            tidal="tidal_tell:wind_drops")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:recognized_object",
                            tidal="tidal_tell:wind_drops")))
    t.append(("object:tide_chart",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:reading_tide_chart",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:tide_chart",
                               "atmosphere:wind_rises",
                               "revelation:partial_match", "beat:orientation",
                               cause="cause:reading_tide_chart",
                               tidal="tidal_tell:tide_recedes")))
    t.append(("object:weather_log",
              cold_examine("location:weather_tower", "object:weather_log",
                           "atmosphere:wind_rises",
                           "revelation:contradiction_surfaces",
                           "beat:investigation",
                           cause="cause:noticed_inconsistency")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:fresh_soil_on_base",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:contradiction_surfaces",
                           "beat:investigation",
                           cause="cause:noticed_inconsistency",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_jetty",
              return_to_examine("location:jetty", "object:tide_chart",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:investigation",
                                cause="cause:reading_tide_chart",
                                tidal="tidal_tell:tide_recedes")))
    t.append(("witness:boat_skipper",
              return_to_question("location:jetty",
                                 "presence:with_mira_callan",
                                 "object:tide_chart",
                                 "atmosphere:waves_against_rock",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:evasive",
                                 tell="tell:hesitated",
                                 tidal="tidal_tell:tide_recedes")))
    t.append(("motive:fishing_economy",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:final_report",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:pursued_suspicion",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:silence_holds",
                            "revelation:tidal_window_identified",
                            "beat:investigation",
                            stance="stance:evasive",
                            tell="tell:over_explained",
                            cause="cause:noticed_inconsistency")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:resupply_schedule",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:investigation",
                            cause="cause:recognized_object")))
    t.append(("suspect:piers_dunne",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("object:resupply_schedule",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:schedule_in_piers_hand",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("travel:to_jetty",
              return_to_question("location:jetty",
                                 "presence:with_mira_callan",
                                 "object:tide_chart",
                                 "atmosphere:waves_against_rock",
                                 "revelation:name_uncovered",
                                 "beat:closing_in",
                                 stance="stance:evasive",
                                 tell="tell:hesitated",
                                 tidal="tidal_tell:tide_floods")))
    t.append(("object:path_marker",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:path_marker",
                            "atmosphere:waves_against_rock",
                            "revelation:confirmation",
                            "beat:closing_in",
                            stance="stance:evasive",
                            tell="tell:over_explained",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:tide_floods")))
    t.append(("motive:fishing_economy",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:final_report",
                            "atmosphere:waves_against_rock",
                            "revelation:motive_emerges", "beat:closing_in",
                            stance="stance:evasive",
                            tell="tell:over_explained",
                            cause="cause:pursued_suspicion",
                            tidal="tidal_tell:tide_floods")))
    t.append(("travel:to_eastern_path",
              return_to_examine("location:eastern_path", "object:path_marker",
                                "atmosphere:wind_rises",
                                "revelation:confirmation",
                                "beat:closing_in",
                                cause="cause:recognized_object",
                                tidal="tidal_tell:path_unstable")))
    t.append(("object:path_marker",
              trace_route("location:eastern_path", "object:path_marker",
                          "atmosphere:wind_rises",
                          "revelation:tidal_window_identified",
                          "beat:closing_in",
                          trans="transition:stayed",
                          tidal="tidal_tell:path_unstable")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:path_marker",
                                "atmosphere:silence_holds",
                                "revelation:confirmation",
                                "beat:closing_in",
                                stance="stance:defensive",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:name_uncovered", "beat:closing_in",
                           tell="tell:paled")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:paled",
                           cause="cause:noticed_inconsistency")))
    t.append(("witness:lighthouse_keeper",
              cross_to_question("location:weather_tower",
                                "presence:with_padraic_burne",
                                "object_focus:none",
                                "atmosphere:wind_rises",
                                "revelation:confirmation",
                                "beat:closing_in",
                                tidal="tidal_tell:wind_drops")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:weather_tower",
                            "presence:with_padraic_burne",
                            "object:tide_chart",
                            "atmosphere:silence_holds",
                            "revelation:confirmation",
                            "beat:closing_in",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:wind_drops")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:path_marker",
                                "atmosphere:dawn_approaches",
                                "revelation:confirmation",
                                "beat:verdict_ready",
                                stance="stance:hostile",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:tide_chart",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:tide_chart",
                           "atmosphere:dawn_approaches",
                           "revelation:name_uncovered",
                           "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges",
                           "beat:verdict_ready",
                           tell="tell:silent",
                           cause="cause:noticed_inconsistency")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation",
                           "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:path_marker")))
    return trajectory(
        "dunne_via_callan_corroboration",
        "Mira Callan's evasion is the key. The detective notices her "
        "hesitation early at the jetty, follows the tide-chart "
        "annotations she made in Piers's hand, and triangulates against "
        "the path marker and the loan papers. Callan breaks late in "
        "the jetty interview and names the moment she warned him.",
        "correct_piers_dunne", "witness_first",
        ["callan_corroboration_chain", "jetty_heavy", "boat_skipper_breaks",
         "tide_chart_annotated", "witness_first_pattern"],
        t, ramp="standard",
    )


# Continue with remaining trajectories. Due to size, switching to a more
# compressed pattern: many trajectories share the same skeleton.

# ╔════════════════════════════════════════════════════════════════════╗
# ║  CORRECT — dunne_via_webb_alibi_collapse                           ║
# ╚════════════════════════════════════════════════════════════════════╝
def dunne_via_webb_alibi_collapse():
    """Player initially pursues Webb (the red herring) — alibi fails to
    hold, recognises the obvious-suspect trap, redirects to Piers via
    the marker and schedule."""
    t = []
    t.append(("object:journal_letter",
              cold_examine("location:research_lab", "object:journal_letter",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("suspect:marcus_webb",
              cross_to_question("location:dorms",
                                "presence:with_marcus_webb",
                                "object:journal_letter",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:orientation",
                                stance="stance:defensive",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:journal_letter",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:rain_against_glass",
                            "revelation:alibi_holds", "beat:orientation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:orientation")))
    t.append(("witness:cook",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object_focus:none",
                            "atmosphere:rain_against_glass",
                            "revelation:alibi_holds", "beat:orientation",
                            cause="cause:following_witness_lead")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:resupply_schedule",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:investigation",
                            cause="cause:recognized_object")))
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:silence_holds",
                                 "revelation:alibi_holds",
                                 "beat:investigation",
                                 stance="stance:defensive",
                                 tell="tell:over_explained")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:weather_log",
                            "atmosphere:silence_holds",
                            "revelation:dead_end", "beat:investigation",
                            stance="stance:defensive",
                            tell="tell:over_explained",
                            cause="cause:noticed_inconsistency")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               cause="cause:revisiting_scene",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("object:path_marker",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:contradiction_surfaces",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:tide_chart",
                               "atmosphere:wind_rises",
                               "revelation:tidal_window_identified",
                               "beat:investigation",
                               cause="cause:reading_tide_chart",
                               tidal="tidal_tell:tide_recedes")))
    t.append(("witness:radio_operator",
              cross_to_question("location:research_lab",
                                "presence:with_kestrel_lin",
                                "object:radio_handset",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                tidal="tidal_tell:radio_breaks_static")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:radio_handset",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            cause="cause:noticed_inconsistency")))
    t.append(("suspect:piers_dunne",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("object:resupply_schedule",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:schedule_in_piers_hand",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("witness:generator_engineer",
              cross_to_question("location:generator_room",
                                "presence:with_niall_brackett",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                tidal="tidal_tell:generator_falters")))
    t.append(("modifier:generator_serviced_late",
              stay_question("location:generator_room",
                            "presence:with_niall_brackett",
                            "object:weather_log",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:generator_falters")))
    t.append(("travel:to_eastern_path",
              return_to_examine("location:eastern_path", "object:path_marker",
                                "atmosphere:wind_rises",
                                "revelation:name_uncovered",
                                "beat:closing_in",
                                cause="cause:recognized_object",
                                tidal="tidal_tell:tide_floods")))
    t.append(("object:path_marker",
              trace_route("location:eastern_path", "object:path_marker",
                          "atmosphere:wind_rises",
                          "revelation:tidal_window_identified",
                          "beat:closing_in",
                          trans="transition:stayed",
                          tidal="tidal_tell:path_unstable")))
    t.append(("motive:fishing_economy",
              recall_alone("location:eastern_path", "object:final_report",
                           "atmosphere:wind_rises",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion",
                           tidal="tidal_tell:path_unstable")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:path_marker",
                                "atmosphere:silence_holds",
                                "revelation:confirmation",
                                "beat:closing_in",
                                stance="stance:defensive",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:confirmation", "beat:closing_in")))
    t.append(("object:resupply_schedule",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:resupply_schedule",
                           "atmosphere:silence_holds",
                           "revelation:name_uncovered", "beat:closing_in",
                           tell="tell:paled")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:paled",
                           cause="cause:noticed_inconsistency")))
    t.append(("witness:boat_skipper",
              cross_to_question("location:jetty",
                                "presence:with_mira_callan",
                                "object_focus:none",
                                "atmosphere:waves_against_rock",
                                "revelation:confirmation",
                                "beat:closing_in",
                                stance="stance:evasive",
                                tell="tell:hesitated",
                                tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:confirmation", "beat:closing_in",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:path_marker",
                                "atmosphere:dawn_approaches",
                                "revelation:confirmation",
                                "beat:verdict_ready",
                                stance="stance:hostile",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:dawn_approaches",
                           "revelation:name_uncovered",
                           "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges",
                           "beat:verdict_ready",
                           tell="tell:silent",
                           cause="cause:noticed_inconsistency")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:path_marker")))
    return trajectory(
        "dunne_via_webb_alibi_collapse",
        "Webb-first false-start. The detective opens with Webb's "
        "journal-letter grievance, finds his alibi holds despite "
        "appearances, redirects to the logistics layer, and closes on "
        "Piers via the marker, the schedule, and the loan papers.",
        "correct_piers_dunne", "wrong_suspect_first",
        ["webb_false_start", "alibi_redirect", "obvious_suspect_collapse",
         "logistics_redirect"],
        t, ramp="standard",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  CORRECT — dunne_via_research_notebook                             ║
# ╚════════════════════════════════════════════════════════════════════╝
def dunne_via_research_notebook():
    t = []
    t.append(("object:research_notebook",
              cold_examine("location:research_lab", "object:research_notebook",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("object:final_report",
              cold_examine("location:research_lab", "object:final_report",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:orientation")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:research_notebook",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            cause="cause:recognized_object")))
    t.append(("travel:to_research_lab",
              return_to_examine("location:research_lab",
                                "object:research_notebook",
                                "atmosphere:rain_against_glass",
                                "revelation:contradiction_surfaces",
                                "beat:investigation",
                                cause="cause:noticed_inconsistency")))
    t.append(("modifier:walk_routine_documented",
              cold_examine("location:research_lab",
                           "object:research_notebook",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:recognized_object")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:tide_chart",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               cause="cause:reading_tide_chart")))
    t.append(("object:tide_chart",
              cold_examine("location:weather_tower", "object:tide_chart",
                           "atmosphere:wind_rises",
                           "revelation:tidal_window_identified",
                           "beat:investigation",
                           cause="cause:reading_tide_chart",
                           tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:contradiction_surfaces",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:fresh_soil_on_base",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("suspect:piers_dunne",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("object:research_notebook",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:research_notebook",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:schedule_in_piers_hand",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("witness:radio_operator",
              cross_to_question("location:research_lab",
                                "presence:with_kestrel_lin",
                                "object:radio_handset",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                tidal="tidal_tell:radio_breaks_static")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:radio_handset",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            cause="cause:noticed_inconsistency")))
    t.append(("travel:to_eastern_path",
              return_to_examine("location:eastern_path", "object:path_marker",
                                "atmosphere:wind_rises",
                                "revelation:name_uncovered",
                                "beat:closing_in",
                                cause="cause:recognized_object",
                                tidal="tidal_tell:tide_floods")))
    t.append(("object:path_marker",
              trace_route("location:eastern_path", "object:path_marker",
                          "atmosphere:wind_rises",
                          "revelation:tidal_window_identified",
                          "beat:closing_in",
                          trans="transition:stayed",
                          tidal="tidal_tell:path_unstable")))
    t.append(("motive:fishing_economy",
              recall_alone("location:eastern_path", "object:final_report",
                           "atmosphere:wind_rises",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion",
                           tidal="tidal_tell:path_unstable")))
    t.append(("witness:boat_skipper",
              cross_to_question("location:jetty",
                                "presence:with_mira_callan",
                                "object_focus:none",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:closing_in",
                                stance="stance:evasive",
                                tell="tell:hesitated",
                                tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:closing_in",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:research_notebook",
                                "atmosphere:silence_holds",
                                "revelation:confirmation",
                                "beat:closing_in",
                                stance="stance:defensive",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:research_notebook",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:research_notebook",
                           "atmosphere:silence_holds",
                           "revelation:confirmation", "beat:closing_in")))
    t.append(("object:final_report",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:name_uncovered", "beat:closing_in",
                           tell="tell:paled")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:paled",
                           cause="cause:noticed_inconsistency")))
    t.append(("witness:generator_engineer",
              cross_to_question("location:generator_room",
                                "presence:with_niall_brackett",
                                "object:weather_log",
                                "atmosphere:silence_holds",
                                "revelation:confirmation",
                                "beat:closing_in",
                                tidal="tidal_tell:generator_falters")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:research_notebook",
                                "atmosphere:dawn_approaches",
                                "revelation:confirmation",
                                "beat:verdict_ready",
                                stance="stance:hostile",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:dawn_approaches",
                           "revelation:name_uncovered",
                           "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("modifier:schedule_in_piers_hand",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:resupply_schedule",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges",
                           "beat:verdict_ready",
                           tell="tell:silent",
                           cause="cause:noticed_inconsistency")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:research_notebook")))
    return trajectory(
        "dunne_via_research_notebook",
        "Research-notebook chain. Sarah's own notebook shows her walk "
        "routine annotated by Piers's hand on the resupply schedule "
        "she'd left on the bench. The detective triangulates the marker "
        "and the loan papers and closes on Piers.",
        "correct_piers_dunne", "object_first",
        ["notebook_chain", "research_lab_anchor", "annotation_pattern"],
        t, ramp="standard",
    )
