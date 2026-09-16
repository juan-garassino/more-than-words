#!/usr/bin/env python3
"""
Authoring helper for tidal_interval — Wave 2 (+25 trajectories, total 50).

Wave 2 fills the gaps identified after wave 1 coverage:
- sea_cave location (0 → 6)
- storm_lantern object (0 → 6)
- entered/exited/pursued_to/called_away_to/descended_to transitions
- cause:summoned radio-call paths
- second variants for high-impact wrong-suspects and CFs hooks
- NEW OUTCOME: near_miss

Run once:
    python3 living_tales/trainer/cases/tidal_interval/trajectories/_author_wave2.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
# Reuse all helpers from wave 1.
from _author_wave1 import (  # noqa: E402
    DEFAULT_OPENING, S, beat_for, cold_examine, cross_to_examine,
    return_to_examine, cross_to_question, stay_question,
    return_to_question, confront_npc, recall_alone, discover_alone,
    trace_route, radio_in, wait_alone, accuse_scene,
    finalize, trajectory, conv_after,
)


# ─── Trajectory factory wrapping ─────────────────────────────────────────
def trajectory2(traj_id, description, outcome, starting_hypothesis,
                tags, turns_specs, ramp="standard", accused=None):
    """Wave 2 trajectory factory — overrides the ending derivation for the
    new outcome classes (near_miss)."""
    turns = finalize(turns_specs, ramp=ramp)
    if accused is None:
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
        elif outcome == "near_miss":
            # near_miss = barely-correct accusation under thin convergence
            accused = "suspect:piers_dunne"
        else:
            accused = None
    last_conv = turns[-1]["convergence_after"]
    if outcome == "near_miss":
        ending_type = "near_miss"
    elif outcome.startswith("correct_"):
        ending_type = "all_strong"
    elif outcome.startswith("partial_"):
        ending_type = "partial"
    elif outcome == "cold_trail":
        ending_type = "cold"
    else:
        ending_type = "wrong"
    ending = {
        "type": ending_type,
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


# ─── Extra helpers specific to wave 2 ────────────────────────────────────
def cross_with_lantern(loc, obj="object:storm_lantern",
                       atmos="atmosphere:wind_rises",
                       revel="revelation:partial_match",
                       beat="beat:investigation",
                       cause="cause:examining_evidence",
                       tidal="tidal_tell:storm_intensifies"):
    """Cross to a location while carrying / focusing on the storm lantern."""
    return S(loc, "transition:crossed_to", cause, "presence:alone",
             "stance:none", "action:examines", obj, "tell:none",
             atmos, revel, beat, tidal)


def descend_to_cave(obj="object:storm_lantern",
                    atmos="atmosphere:waves_against_rock",
                    revel="revelation:partial_match",
                    beat="beat:investigation",
                    cause="cause:pursued_suspicion",
                    tidal="tidal_tell:tide_recedes"):
    return S("location:sea_cave", "transition:descended_to", cause,
             "presence:alone", "stance:none", "action:arrives",
             obj, "tell:none", atmos, revel, beat, tidal)


def pursue_to(loc, presence, obj, atmos, revel, beat,
              cause="cause:pursued_suspicion",
              stance="stance:defensive", tell="tell:tightened",
              tidal="tidal_tell:storm_intensifies"):
    return S(loc, "transition:pursued_to", cause, presence, stance,
             "action:follows", obj, tell, atmos, revel, beat, tidal)


def called_away_to(loc, presence, obj, atmos, revel, beat,
                   cause="cause:summoned",
                   stance="stance:cooperative", tell="tell:none",
                   tidal="tidal_tell:radio_breaks_static"):
    return S(loc, "transition:called_away_to", cause, presence, stance,
             "action:arrives", obj, tell, atmos, revel, beat, tidal)


def enter_room(loc, obj, atmos, revel, beat,
               cause="cause:examining_evidence",
               tidal="tidal_tell:none"):
    return S(loc, "transition:entered", cause, "presence:alone",
             "stance:none", "action:examines", obj, "tell:none",
             atmos, revel, beat, tidal)


def exit_room(loc_dest, obj, atmos, revel, beat,
              cause="cause:pursued_suspicion",
              tidal="tidal_tell:wind_drops"):
    """Exit current and arrive at loc_dest (so this scene's LOCATION is the
    destination). Use 'exited' for the verb-shaped transition; the sanitize
    pass will repair if continuity breaks."""
    return S(loc_dest, "transition:exited", cause, "presence:alone",
             "stance:none", "action:leaves", obj, "tell:none",
             atmos, revel, beat, tidal)


def radio_summons(loc, presence, atmos, revel, beat,
                  obj="object:radio_handset",
                  stance="stance:cooperative", tell="tell:none",
                  tidal="tidal_tell:radio_breaks_static"):
    """A 'summoned' scene — the player is called away via the radio."""
    return S(loc, "transition:stayed", "cause:summoned", presence, stance,
             "action:radios", obj, tell, atmos, revel, beat, tidal)


# ╔════════════════════════════════════════════════════════════════════╗
# ║  CORRECT — dunne_via_sea_cave                                      ║
# ║  cave-descent path with storm_lantern                              ║
# ╚════════════════════════════════════════════════════════════════════╝
def dunne_via_sea_cave():
    t = []
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
    t.append(("object:storm_lantern",
              cold_examine("location:research_lab", "object:storm_lantern",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           cause="cause:recognized_object")))
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
    t.append(("object:storm_lantern",
              cold_examine("location:eastern_path", "object:storm_lantern",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:orientation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("witness:lighthouse_keeper",
              cross_to_question("location:weather_tower",
                                "presence:with_padraic_burne",
                                "object_focus:none",
                                "atmosphere:wind_rises",
                                "revelation:partial_match",
                                "beat:orientation",
                                tidal="tidal_tell:wind_drops")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:weather_tower",
                            "presence:with_padraic_burne",
                            "object:weather_log",
                            "atmosphere:wind_rises",
                            "revelation:partial_match", "beat:investigation",
                            cause="cause:recognized_object")))
    t.append(("travel:to_eastern_path",
              return_to_examine("location:eastern_path", "object:path_marker",
                                "atmosphere:wind_rises",
                                "revelation:partial_match", "beat:investigation",
                                tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_sea_cave",
              descend_to_cave("object:storm_lantern",
                              "atmosphere:waves_against_rock",
                              "revelation:partial_match",
                              "beat:investigation",
                              cause="cause:pursued_suspicion",
                              tidal="tidal_tell:tide_recedes")))
    t.append(("object:boot_with_fresh_soil",
              cold_examine("location:sea_cave",
                           "object:boot_with_fresh_soil",
                           "atmosphere:waves_against_rock",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:fresh_soil_on_base",
              cold_examine("location:sea_cave", "object:boot_with_fresh_soil",
                           "atmosphere:waves_against_rock",
                           "revelation:contradiction_surfaces",
                           "beat:investigation",
                           cause="cause:noticed_inconsistency",
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
                            cause="cause:noticed_inconsistency")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:tide_chart",
                               "atmosphere:wind_rises",
                               "revelation:tidal_window_identified",
                               "beat:investigation",
                               cause="cause:reading_tide_chart",
                               tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              cold_examine("location:weather_tower", "object:tide_chart",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:reading_tide_chart")))
    t.append(("travel:to_sea_cave",
              S("location:sea_cave", "transition:returned",
                "cause:revisiting_scene", "presence:alone", "stance:none",
                "action:traces_route", "object:path_marker",
                "tell:none", "atmosphere:waves_against_rock",
                "revelation:name_uncovered", "beat:closing_in",
                "tidal_tell:tide_floods")))
    t.append(("object:storm_lantern",
              cold_examine("location:sea_cave", "object:storm_lantern",
                           "atmosphere:waves_against_rock",
                           "revelation:confirmation", "beat:closing_in",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:tide_floods")))
    t.append(("motive:fishing_economy",
              recall_alone("location:sea_cave", "object:final_report",
                           "atmosphere:waves_against_rock",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion",
                           tidal="tidal_tell:tide_floods")))
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
                                "object:path_marker",
                                "atmosphere:silence_holds",
                                "revelation:confirmation",
                                "beat:closing_in",
                                stance="stance:defensive",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:storm_lantern",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:storm_lantern",
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
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:storm_lantern",
                                "atmosphere:dawn_approaches",
                                "revelation:confirmation",
                                "beat:verdict_ready",
                                stance="stance:hostile",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:storm_lantern",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:storm_lantern",
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
                           obj="object:storm_lantern")))
    return trajectory2(
        "dunne_via_sea_cave",
        "Detective follows the lantern's reflection down the cliff stair "
        "into the sea_cave, finds Sarah's boot and the cave debris, then "
        "ties Piers's storm-lantern to the path's relocation via the "
        "schedule in his hand. Sea_cave-anchored chain.",
        "correct_piers_dunne", "object_first",
        ["sea_cave_chain", "storm_lantern_chain", "marker_displaced",
         "descended_to_cave", "wave2"],
        t, ramp="standard",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  CORRECT — dunne_via_radio_summons                                 ║
# ║  cause:summoned radio-call variant                                 ║
# ╚════════════════════════════════════════════════════════════════════╝
def dunne_via_radio_summons():
    t = []
    t.append(("object:radio_handset",
              cold_examine("location:research_lab", "object:radio_handset",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none",
                           cause="cause:examining_evidence")))
    t.append(("witness:radio_operator",
              cross_to_question("location:research_lab",
                                "presence:with_kestrel_lin",
                                "object:radio_handset",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:orientation",
                                tidal="tidal_tell:radio_breaks_static")))
    t.append(("object:satellite_log",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            cause="cause:examining_evidence")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:radio_handset",
                            "atmosphere:rain_against_glass",
                            "revelation:contradiction_surfaces",
                            "beat:orientation",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:radio_breaks_static")))
    t.append(("object:radio_handset",
              radio_summons("location:research_lab",
                            "presence:with_kestrel_lin",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match",
                            "beat:orientation",
                            stance="stance:cooperative")))
    t.append(("travel:to_jetty",
              called_away_to("location:jetty",
                             "presence:with_mira_callan",
                             "object_focus:none",
                             "atmosphere:waves_against_rock",
                             "revelation:partial_match",
                             "beat:investigation",
                             stance="stance:evasive",
                             tell="tell:hesitated",
                             tidal="tidal_tell:tide_recedes")))
    t.append(("witness:boat_skipper",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object_focus:none",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:evasive",
                            tell="tell:hesitated")))
    t.append(("object:tide_chart",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:reading_tide_chart",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:tidal_window_identified",
                            "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
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
    t.append(("modifier:socket_hole_compressed",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_research_lab",
              return_to_examine("location:research_lab",
                                "object:satellite_log",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("witness:radio_operator",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            cause="cause:radio_message_received",
                            tidal="tidal_tell:radio_breaks_static")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:radio_handset",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:radio_breaks_static")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            cause="cause:recognized_object")))
    t.append(("suspect:piers_dunne",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object_focus:none",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:closing_in",
                            stance="stance:defensive", tell="tell:tightened")))
    t.append(("object:resupply_schedule",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:name_uncovered", "beat:closing_in",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:schedule_in_piers_hand",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:confirmation", "beat:closing_in",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("motive:fishing_economy",
              recall_alone("location:common_room", "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion")))
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
    t.append(("object:radio_handset",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:radio_handset",
                           "atmosphere:dawn_approaches",
                           "revelation:name_uncovered", "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:radio_handset")))
    return trajectory2(
        "dunne_via_radio_summons",
        "The detective is summoned by a radio call to the jetty mid-orient. "
        "Callan's hesitations and a blank radio log lead back to a "
        "compressed socket and to Piers's schedule. Radio-summons motif "
        "throughout, ends in a verdict-ready confrontation.",
        "correct_piers_dunne", "object_first",
        ["radio_summons_chain", "cause_summoned", "called_away_to",
         "satellite_log_first", "wave2"],
        t, ramp="standard",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  CORRECT — dunne_via_storm_pursuit                                 ║
# ║  pursued_to storm-chase                                            ║
# ╚════════════════════════════════════════════════════════════════════╝
def dunne_via_storm_pursuit():
    t = []
    t.append(("object:storm_lantern",
              cold_examine("location:research_lab", "object:storm_lantern",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("travel:to_generator_room",
              cross_to_examine("location:generator_room",
                               "object:weather_log",
                               "atmosphere:rain_against_glass",
                               "revelation:partial_match", "beat:orientation",
                               tidal="tidal_tell:generator_falters")))
    t.append(("witness:generator_engineer",
              stay_question("location:generator_room",
                            "presence:with_niall_brackett",
                            "object:weather_log",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            tidal="tidal_tell:generator_falters")))
    t.append(("modifier:generator_serviced_late",
              stay_question("location:generator_room",
                            "presence:with_niall_brackett",
                            "object:weather_log",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match",
                            "beat:orientation",
                            cause="cause:recognized_object",
                            tidal="tidal_tell:generator_falters")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match", "beat:orientation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("suspect:piers_dunne",
              S("location:eastern_path", "transition:stayed",
                "cause:noticed_inconsistency",
                "presence:with_piers_dunne", "stance:evasive",
                "action:notices", "object:path_marker", "tell:glanced_aside",
                "atmosphere:wind_rises", "revelation:partial_match",
                "beat:investigation",
                "tidal_tell:storm_intensifies")))
    t.append(("modifier:fresh_soil_on_base",
              stay_question("location:eastern_path",
                            "presence:with_piers_dunne",
                            "object:path_marker",
                            "atmosphere:wind_rises",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_jetty",
              pursue_to("location:jetty", "presence:with_piers_dunne",
                        "object:storm_lantern",
                        "atmosphere:waves_against_rock",
                        "revelation:partial_match", "beat:investigation",
                        cause="cause:pursued_suspicion",
                        tidal="tidal_tell:storm_intensifies")))
    t.append(("witness:boat_skipper",
              S("location:jetty", "transition:stayed",
                "cause:following_witness_lead",
                "presence:with_mira_callan", "stance:evasive",
                "action:questions", "object_focus:none", "tell:hesitated",
                "atmosphere:waves_against_rock",
                "revelation:partial_match", "beat:investigation",
                "tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:tidal_window_identified",
                            "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:reading_tide_chart",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_sea_cave",
              descend_to_cave("object:storm_lantern",
                              "atmosphere:waves_against_rock",
                              "revelation:partial_match", "beat:investigation",
                              cause="cause:pursued_suspicion",
                              tidal="tidal_tell:tide_floods")))
    t.append(("object:boot_with_fresh_soil",
              cold_examine("location:sea_cave",
                           "object:boot_with_fresh_soil",
                           "atmosphere:waves_against_rock",
                           "revelation:name_uncovered", "beat:closing_in",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:tide_floods")))
    t.append(("object:storm_lantern",
              cold_examine("location:sea_cave", "object:storm_lantern",
                           "atmosphere:waves_against_rock",
                           "revelation:confirmation", "beat:closing_in",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:tide_floods")))
    t.append(("travel:to_eastern_path",
              return_to_examine("location:eastern_path", "object:path_marker",
                                "atmosphere:wind_rises",
                                "revelation:confirmation", "beat:closing_in",
                                cause="cause:noticed_inconsistency",
                                tidal="tidal_tell:path_unstable")))
    t.append(("modifier:schedule_in_piers_hand",
              cold_examine("location:eastern_path", "object:resupply_schedule",
                           "atmosphere:wind_rises",
                           "revelation:name_uncovered", "beat:closing_in",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:path_unstable")))
    t.append(("motive:fishing_economy",
              recall_alone("location:eastern_path", "object:final_report",
                           "atmosphere:wind_rises",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion",
                           tidal="tidal_tell:path_unstable")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:closing_in")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:closing_in",
                            cause="cause:recognized_object")))
    t.append(("travel:to_common_room",
              S("location:common_room", "transition:stayed",
                "cause:pursued_suspicion", "presence:with_piers_dunne",
                "stance:defensive", "action:confronts", "object:storm_lantern",
                "tell:tightened", "atmosphere:silence_holds",
                "revelation:confirmation", "beat:closing_in",
                "tidal_tell:none")))
    t.append(("object:storm_lantern",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:storm_lantern",
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
    t.append(("modifier:schedule_in_piers_hand",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:resupply_schedule",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges", "beat:verdict_ready",
                           tell="tell:silent",
                           cause="cause:noticed_inconsistency")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:storm_lantern")))
    return trajectory2(
        "dunne_via_storm_pursuit",
        "Storm-chase: detective pursues Piers from the eastern path to the "
        "jetty in raised wind, then descends into the sea_cave for the "
        "boot and lantern, and locks in the verdict via the schedule. "
        "Pursued_to-anchored chain.",
        "correct_piers_dunne", "wrong_suspect_first",
        ["storm_pursuit_chain", "pursued_to", "sea_cave_chain",
         "storm_lantern_chain", "wave2"],
        t, ramp="standard",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  CORRECT — dunne_via_weather_tower_radio                           ║
# ║  fourth correct — entered weather tower path                       ║
# ╚════════════════════════════════════════════════════════════════════╝
def dunne_via_weather_tower_radio():
    t = []
    t.append(("object:weather_log",
              cold_examine("location:research_lab", "object:weather_log",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none",
                           cause="cause:examining_evidence")))
    t.append(("travel:to_weather_tower",
              enter_room("location:weather_tower", "object:weather_log",
                         "atmosphere:rain_against_glass",
                         "revelation:partial_match", "beat:orientation",
                         cause="cause:examining_evidence")))
    t.append(("modifier:storm_warning_issued",
              cold_examine("location:weather_tower", "object:weather_log",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:orientation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("witness:lighthouse_keeper",
              stay_question("location:weather_tower",
                            "presence:with_padraic_burne",
                            "object:weather_log",
                            "atmosphere:wind_rises",
                            "revelation:partial_match", "beat:orientation",
                            tidal="tidal_tell:wind_drops")))
    t.append(("object:radio_handset",
              radio_in("location:weather_tower",
                       "atmosphere:wind_rises",
                       "revelation:partial_match", "beat:orientation",
                       tidal="tidal_tell:radio_breaks_static")))
    t.append(("modifier:radio_log_blank",
              cold_examine("location:weather_tower", "object:satellite_log",
                           "atmosphere:wind_rises",
                           "revelation:contradiction_surfaces",
                           "beat:orientation",
                           cause="cause:noticed_inconsistency",
                           tidal="tidal_tell:radio_breaks_static")))
    t.append(("object:tide_chart",
              cold_examine("location:weather_tower", "object:tide_chart",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:reading_tide_chart")))
    t.append(("modifier:tide_data_annotated",
              cold_examine("location:weather_tower", "object:tide_chart",
                           "atmosphere:wind_rises",
                           "revelation:tidal_window_identified",
                           "beat:investigation",
                           cause="cause:reading_tide_chart")))
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
                           cause="cause:noticed_inconsistency",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:socket_hole_compressed",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            cause="cause:recognized_object")))
    t.append(("suspect:piers_dunne",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object_focus:none",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened")))
    t.append(("object:resupply_schedule",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:noticed_inconsistency")))
    t.append(("modifier:schedule_in_piers_hand",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:name_uncovered", "beat:closing_in",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("travel:to_weather_tower",
              return_to_examine("location:weather_tower",
                                "object:satellite_log",
                                "atmosphere:wind_rises",
                                "revelation:confirmation", "beat:closing_in",
                                cause="cause:radio_message_received",
                                tidal="tidal_tell:radio_breaks_static")))
    t.append(("witness:radio_operator",
              stay_question("location:weather_tower",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:wind_rises",
                            "revelation:confirmation", "beat:closing_in",
                            cause="cause:radio_message_received",
                            tidal="tidal_tell:radio_breaks_static")))
    t.append(("motive:fishing_economy",
              recall_alone("location:weather_tower", "object:final_report",
                           "atmosphere:wind_rises",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:path_marker",
                                "atmosphere:dawn_approaches",
                                "revelation:confirmation",
                                "beat:verdict_ready",
                                stance="stance:hostile", tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:dawn_approaches",
                           "revelation:name_uncovered", "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:resupply_schedule")))
    return trajectory2(
        "dunne_via_weather_tower_radio",
        "Weather-tower-first chain. Entered tower, found blank radio log "
        "and storm warning. Tidal window identified early; path-marker "
        "ties up the mechanism layer; satellite log corroborates Piers's "
        "afternoon traffic gap.",
        "correct_piers_dunne", "object_first",
        ["weather_tower_chain", "entered_tower", "satellite_log",
         "storm_warning_anchor", "wave2"],
        t, ramp="standard",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  WRONG — wrong_marcus_webb_v2 (2nd path)                           ║
# ╚════════════════════════════════════════════════════════════════════╝
def wrong_marcus_webb_v2():
    t = []
    t.append(("object:journal_letter",
              cold_examine("location:dorms", "object:journal_letter",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("witness:methodology_reviewer",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:defensive", tell="tell:tightened")))
    t.append(("object:final_report",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:final_report",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:defensive", tell="tell:over_explained",
                            cause="cause:examining_evidence")))
    t.append(("modifier:storm_warning_issued",
              cross_to_examine("location:weather_tower", "object:weather_log",
                               "atmosphere:wind_rises",
                               "revelation:partial_match", "beat:orientation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("witness:methodology_reviewer",
              cross_to_question("location:research_lab",
                                "presence:with_marcus_webb",
                                "object:final_report",
                                "atmosphere:silence_holds",
                                "revelation:contradiction_surfaces",
                                "beat:orientation",
                                stance="stance:hostile",
                                tell="tell:tightened",
                                cause="cause:noticed_inconsistency")))
    t.append(("object:journal_letter",
              stay_question("location:research_lab",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:examining_evidence")))
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
    t.append(("suspect:marcus_webb",
              cross_to_question("location:dorms",
                                "presence:with_marcus_webb",
                                "object:final_report",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:investigation",
                                stance="stance:hostile",
                                tell="tell:tightened")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:weather_log",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:resupply_schedule",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            cause="cause:recognized_object")))
    t.append(("object:journal_letter",
              cold_examine("location:common_room", "object:journal_letter",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:examining_evidence")))
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:hostile",
                                 tell="tell:tightened")))
    t.append(("modifier:storm_warning_issued",
              S("location:dorms", "transition:stayed",
                "cause:noticed_inconsistency", "presence:with_marcus_webb",
                "stance:hostile", "action:confronts", "object:weather_log",
                "tell:tightened", "atmosphere:silence_holds",
                "revelation:partial_match", "beat:closing_in",
                "tidal_tell:none")))
    t.append(("object:final_report",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("motive:methodology_grievance",
              recall_alone("location:dorms", "object:journal_letter",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           cause="cause:pursued_suspicion")))
    t.append(("object:journal_letter",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:journal_letter",
                           "atmosphere:dawn_approaches",
                           "revelation:partial_match", "beat:verdict_ready",
                           tell="tell:tightened")))
    t.append(("ACCUSE:suspect:marcus_webb",
              accuse_scene("location:dorms",
                           "presence:with_marcus_webb",
                           obj="object:journal_letter")))
    return trajectory2(
        "wrong_marcus_webb_v2",
        "Second wrong-Webb path. Anchored in the journal letter, dorm "
        "interview, and the methodology grievance. Detective never closes "
        "on the path-marker mechanism. Accuses Webb at dawn.",
        "wrong_marcus_webb", "wrong_suspect_first",
        ["webb_trap_v2", "journal_letter_first", "dorms_heavy",
         "methodology_misread", "wave2"],
        t, ramp="framed",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  WRONG — wrong_mira_callan_v2                                      ║
# ╚════════════════════════════════════════════════════════════════════╝
def wrong_mira_callan_v2():
    t = []
    t.append(("object:sea_chart_overlay",
              cold_examine("location:research_lab",
                           "object:sea_chart_overlay",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none",
                           cause="cause:reading_tide_chart")))
    t.append(("travel:to_jetty",
              cross_to_question("location:jetty",
                                "presence:with_mira_callan",
                                "object_focus:none",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:orientation",
                                stance="stance:evasive",
                                tell="tell:hesitated",
                                tidal="tidal_tell:tide_recedes")))
    t.append(("object:tide_chart",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:reading_tide_chart",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match",
                            "beat:orientation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:recognized_object",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("suspect:mira_callan",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:contradiction_surfaces",
                            "beat:orientation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:resupply_schedule",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:recognized_object",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:tide_chart",
                               "atmosphere:wind_rises",
                               "revelation:tidal_window_identified",
                               "beat:investigation",
                               cause="cause:reading_tide_chart",
                               tidal="tidal_tell:tide_recedes")))
    t.append(("witness:lighthouse_keeper",
              stay_question("location:weather_tower",
                            "presence:with_padraic_burne",
                            "object_focus:none",
                            "atmosphere:wind_rises",
                            "revelation:partial_match",
                            "beat:investigation")))
    t.append(("travel:to_jetty",
              return_to_question("location:jetty",
                                 "presence:with_mira_callan",
                                 "object:tide_chart",
                                 "atmosphere:waves_against_rock",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:hostile",
                                 tell="tell:tightened",
                                 tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:recognized_object",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("motive:family_on_the_boats",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object_focus:none",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:pursued_suspicion",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("object:tide_chart",
              confront_npc("location:jetty",
                           "presence:with_mira_callan",
                           "object:tide_chart",
                           "atmosphere:waves_against_rock",
                           "revelation:partial_match", "beat:investigation",
                           tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:weather_log",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match",
                            "beat:closing_in",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:recognized_object",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_weather_tower",
              return_to_examine("location:weather_tower", "object:tide_chart",
                                "atmosphere:wind_rises",
                                "revelation:partial_match",
                                "beat:closing_in",
                                cause="cause:reading_tide_chart")))
    t.append(("modifier:tide_data_annotated",
              cold_examine("location:weather_tower", "object:tide_chart",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:closing_in",
                           cause="cause:reading_tide_chart")))
    t.append(("travel:to_jetty",
              return_to_question("location:jetty",
                                 "presence:with_mira_callan",
                                 "object:tide_chart",
                                 "atmosphere:waves_against_rock",
                                 "revelation:partial_match", "beat:closing_in",
                                 stance="stance:hostile",
                                 tell="tell:tightened",
                                 tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              confront_npc("location:jetty",
                           "presence:with_mira_callan",
                           "object:tide_chart",
                           "atmosphere:waves_against_rock",
                           "revelation:partial_match", "beat:closing_in",
                           cause="cause:noticed_inconsistency",
                           tidal="tidal_tell:tide_recedes")))
    t.append(("object:tide_chart",
              confront_npc("location:jetty",
                           "presence:with_mira_callan",
                           "object:tide_chart",
                           "atmosphere:dawn_approaches",
                           "revelation:partial_match", "beat:verdict_ready",
                           tidal="tidal_tell:tide_recedes")))
    t.append(("motive:family_on_the_boats",
              confront_npc("location:jetty",
                           "presence:with_mira_callan",
                           "object_focus:none",
                           "atmosphere:dawn_approaches",
                           "revelation:partial_match", "beat:verdict_ready",
                           cause="cause:pursued_suspicion",
                           tidal="tidal_tell:tide_recedes")))
    t.append(("ACCUSE:suspect:mira_callan",
              accuse_scene("location:jetty",
                           "presence:with_mira_callan",
                           obj="object:tide_chart")))
    return trajectory2(
        "wrong_mira_callan_v2",
        "Second wrong-Callan path. Detective fixates on Callan's tide "
        "annotations and family ties to the boats; never reaches the "
        "path-marker mechanism layer. Accuses Mira at dawn.",
        "wrong_mira_callan", "witness_first",
        ["callan_trap_v2", "tide_chart_misread", "family_on_boats_misread",
         "no_marker_visit", "wave2"],
        t, ramp="framed",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  WRONG — wrong_oren_halloway_v2                                    ║
# ╚════════════════════════════════════════════════════════════════════╝
def wrong_oren_halloway_v2():
    t = []
    t.append(("object:final_report",
              cold_examine("location:research_lab", "object:final_report",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("witness:director",
              cross_to_question("location:common_room",
                                "presence:with_oren_halloway",
                                "object_focus:none",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:orientation",
                                stance="stance:defensive",
                                tell="tell:over_explained")))
    t.append(("object:final_report",
              stay_question("location:common_room",
                            "presence:with_oren_halloway",
                            "object:final_report",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:defensive", tell="tell:over_explained",
                            cause="cause:examining_evidence")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:common_room",
                            "presence:with_oren_halloway",
                            "object:weather_log",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:defensive", tell="tell:over_explained",
                            cause="cause:recognized_object")))
    t.append(("suspect:oren_halloway",
              stay_question("location:common_room",
                            "presence:with_oren_halloway",
                            "object_focus:none",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:hostile", tell="tell:tightened")))
    t.append(("object:resupply_schedule",
              stay_question("location:common_room",
                            "presence:with_oren_halloway",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_oren_halloway",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("travel:to_research_lab",
              cross_to_examine("location:research_lab", "object:journal_letter",
                               "atmosphere:silence_holds",
                               "revelation:partial_match",
                               "beat:investigation")))
    t.append(("motive:career_pressure",
              recall_alone("location:research_lab", "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:pursued_suspicion")))
    t.append(("travel:to_common_room",
              return_to_question("location:common_room",
                                 "presence:with_oren_halloway",
                                 "object:final_report",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:hostile",
                                 tell="tell:tightened")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:common_room",
                            "presence:with_oren_halloway",
                            "object:weather_log",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile",
                            tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_common_room",
              return_to_question("location:common_room",
                                 "presence:with_oren_halloway",
                                 "object:final_report",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:closing_in",
                                 stance="stance:hostile",
                                 tell="tell:tightened")))
    t.append(("object:final_report",
              confront_npc("location:common_room",
                           "presence:with_oren_halloway",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("motive:career_pressure",
              confront_npc("location:common_room",
                           "presence:with_oren_halloway",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:pursued_suspicion")))
    t.append(("object:journal_letter",
              confront_npc("location:common_room",
                           "presence:with_oren_halloway",
                           "object:journal_letter",
                           "atmosphere:dawn_approaches",
                           "revelation:partial_match", "beat:verdict_ready",
                           tell="tell:tightened")))
    t.append(("ACCUSE:suspect:oren_halloway",
              accuse_scene("location:common_room",
                           "presence:with_oren_halloway",
                           obj="object:final_report")))
    return trajectory2(
        "wrong_oren_halloway_v2",
        "Second wrong-Halloway path. Detective triangulates director's "
        "career pressure and storm warning, ignores Piers entirely. "
        "Accuses Halloway at dawn.",
        "wrong_oren_halloway", "witness_first",
        ["director_trap_v2", "career_pressure_misread", "final_report_first",
         "common_room_anchor", "wave2"],
        t, ramp="framed",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  WRONG — wrong_tovi_ansgar_v2                                      ║
# ╚════════════════════════════════════════════════════════════════════╝
def wrong_tovi_ansgar_v2():
    t = []
    t.append(("object:research_notebook",
              cold_examine("location:research_lab", "object:research_notebook",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("witness:junior_researcher",
              stay_question("location:research_lab",
                            "presence:with_tovi_ansgar",
                            "object:research_notebook",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:evasive", tell="tell:softened")))
    t.append(("object:journal_letter",
              stay_question("location:research_lab",
                            "presence:with_tovi_ansgar",
                            "object:journal_letter",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match",
                            "beat:orientation",
                            stance="stance:evasive", tell="tell:softened",
                            cause="cause:examining_evidence")))
    t.append(("suspect:tovi_ansgar",
              stay_question("location:research_lab",
                            "presence:with_tovi_ansgar",
                            "object:research_notebook",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:orientation",
                            stance="stance:hostile", tell="tell:tightened")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:research_lab",
                            "presence:with_tovi_ansgar",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("travel:to_dorms",
              cross_to_question("location:dorms",
                                "presence:with_tovi_ansgar",
                                "object:journal_letter",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                stance="stance:hostile",
                                tell="tell:tightened")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:dorms",
                            "presence:with_tovi_ansgar",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("motive:methodology_grievance",
              stay_question("location:dorms",
                            "presence:with_tovi_ansgar",
                            "object_focus:none",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:pursued_suspicion")))
    t.append(("travel:to_research_lab",
              return_to_question("location:research_lab",
                                 "presence:with_tovi_ansgar",
                                 "object:research_notebook",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:hostile",
                                 tell="tell:tightened")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:research_lab",
                            "presence:with_tovi_ansgar",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("object:journal_letter",
              confront_npc("location:research_lab",
                           "presence:with_tovi_ansgar",
                           "object:journal_letter",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:investigation",
                           tell="tell:tightened")))
    t.append(("object:research_notebook",
              confront_npc("location:research_lab",
                           "presence:with_tovi_ansgar",
                           "object:research_notebook",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:investigation",
                           tell="tell:tightened")))
    t.append(("motive:methodology_grievance",
              confront_npc("location:research_lab",
                           "presence:with_tovi_ansgar",
                           "object:research_notebook",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:pursued_suspicion")))
    t.append(("object:research_notebook",
              confront_npc("location:research_lab",
                           "presence:with_tovi_ansgar",
                           "object:research_notebook",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("modifier:walk_routine_documented",
              confront_npc("location:research_lab",
                           "presence:with_tovi_ansgar",
                           "object:resupply_schedule",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:recognized_object")))
    t.append(("object:journal_letter",
              confront_npc("location:research_lab",
                           "presence:with_tovi_ansgar",
                           "object:journal_letter",
                           "atmosphere:dawn_approaches",
                           "revelation:partial_match", "beat:verdict_ready",
                           tell="tell:tightened")))
    t.append(("ACCUSE:suspect:tovi_ansgar",
              accuse_scene("location:research_lab",
                           "presence:with_tovi_ansgar",
                           obj="object:research_notebook")))
    return trajectory2(
        "wrong_tovi_ansgar_v2",
        "Second wrong-Tovi path. Detective fixates on her methodology "
        "grievance and the resolved disagreement, never visits the "
        "eastern path or the schedule. Accuses Tovi at dawn.",
        "wrong_tovi_ansgar", "witness_first",
        ["tovi_trap_v2", "research_lab_anchor", "methodology_misread",
         "wave2"],
        t, ramp="framed",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  COLD TRAILS                                                       ║
# ╚════════════════════════════════════════════════════════════════════╝
def cold_trail_sea_cave_loop():
    t = []
    t.append(("object:storm_lantern",
              cold_examine("location:research_lab", "object:storm_lantern",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:storm_lantern",
                               "atmosphere:wind_rises",
                               "revelation:partial_match", "beat:orientation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_sea_cave",
              descend_to_cave("object:storm_lantern",
                              "atmosphere:waves_against_rock",
                              "revelation:partial_match",
                              "beat:orientation",
                              cause="cause:examining_evidence",
                              tidal="tidal_tell:tide_recedes")))
    for k in range(15):
        t.append(("object:storm_lantern",
                  cold_examine("location:sea_cave", "object:storm_lantern",
                               "atmosphere:waves_against_rock",
                               "revelation:dead_end",
                               "beat:investigation",
                               cause="cause:examining_evidence",
                               tidal="tidal_tell:tide_recedes")))
    return trajectory2(
        "cold_trail_sea_cave_loop",
        "Detective loops in the sea_cave examining the storm lantern; "
        "never returns to the path-marker or any witness. The case stalls.",
        "cold_trail", "object_first",
        ["cold_trail_sea_cave", "sea_cave_loop", "storm_lantern_loop",
         "wave2"],
        t, ramp="cold",
    )


def cold_trail_storm_summons_loop():
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
    for k in range(16):
        t.append(("object:radio_handset",
                  S("location:research_lab", "transition:stayed",
                    "cause:radio_message_received",
                    "presence:with_kestrel_lin", "stance:cooperative",
                    "action:radios", "object:radio_handset", "tell:none",
                    "atmosphere:silence_holds",
                    "revelation:dead_end",
                    "beat:investigation",
                    "tidal_tell:radio_breaks_static")))
    return trajectory2(
        "cold_trail_storm_summons_loop",
        "Detective and the radio operator wait at the bench. Static "
        "after static, and the storm and the silence outlast the case.",
        "cold_trail", "witness_first",
        ["cold_trail_storm_summons", "radio_loop", "static_loop",
         "wave2"],
        t, ramp="cold",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  PARTIAL CORRECT                                                   ║
# ╚════════════════════════════════════════════════════════════════════╝
def partial_dunne_wrong_marker():
    t = []
    t.append(("object:path_marker",
              cold_examine("location:research_lab", "object:path_marker",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
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
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
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
    t.append(("travel:to_eastern_path",
              return_to_examine("location:eastern_path", "object:path_marker",
                                "atmosphere:wind_rises",
                                "revelation:partial_match",
                                "beat:investigation",
                                tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:socket_hole_compressed",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_common_room",
              return_to_question("location:common_room",
                                 "presence:with_piers_dunne",
                                 "object:resupply_schedule",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:defensive",
                                 tell="tell:tightened")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("modifier:marker_displaced_eleven_meters",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:recognized_object")))
    t.append(("object:resupply_schedule",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:resupply_schedule",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:path_marker")))
    return trajectory2(
        "partial_dunne_wrong_marker",
        "Right suspect, weak chain. Detective gets to Piers but never "
        "ties the marker displacement to the tide-chart window; "
        "convergence plateaus around 0.70 and the verdict is partial.",
        "partial_correct", "object_first",
        ["right_suspect_weak_marker", "no_tidal_window", "partial_chain",
         "wave2"],
        t, ramp="partial",
    )


def partial_motive_only_window():
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
    t.append(("modifier:tide_data_annotated",
              cold_examine("location:weather_tower", "object:tide_chart",
                           "atmosphere:wind_rises",
                           "revelation:tidal_window_identified",
                           "beat:orientation",
                           cause="cause:reading_tide_chart",
                           tidal="tidal_tell:tide_recedes")))
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
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:orientation",
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
    t.append(("modifier:processing_facility_loan_due",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("motive:fishing_economy",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:pursued_suspicion")))
    t.append(("witness:boat_skipper",
              cross_to_question("location:jetty",
                                "presence:with_mira_callan",
                                "object_focus:none",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:investigation",
                                stance="stance:evasive",
                                tell="tell:hesitated",
                                tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:reading_tide_chart",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_common_room",
              return_to_question("location:common_room",
                                 "presence:with_piers_dunne",
                                 "object:final_report",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:defensive",
                                 tell="tell:tightened")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:recognized_object")))
    t.append(("motive:fishing_economy",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:pursued_suspicion")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:final_report")))
    return trajectory2(
        "partial_motive_only_window",
        "Right suspect, motive established and tidal window seen, but "
        "the path-marker mechanism never enters the chain. Verdict is "
        "partial — Piers confesses to the motive only.",
        "partial_correct", "object_first",
        ["right_suspect_motive_only", "tidal_window_seen",
         "no_marker_chain", "partial_chain", "wave2"],
        t, ramp="partial",
    )


def partial_via_callan_misread():
    t = []
    t.append(("witness:boat_skipper",
              S("location:research_lab", "transition:none",
                "cause:examining_evidence", "presence:alone", "stance:none",
                "action:examines", "object:tide_chart", "tell:none",
                "atmosphere:rain_against_glass",
                "revelation:partial_match", "beat:orientation",
                "tidal_tell:none")))
    t.append(("travel:to_jetty",
              cross_to_question("location:jetty",
                                "presence:with_mira_callan",
                                "object_focus:none",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:orientation",
                                stance="stance:evasive",
                                tell="tell:hesitated",
                                tidal="tidal_tell:tide_recedes")))
    t.append(("object:tide_chart",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:reading_tide_chart",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match",
                            "beat:orientation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:recognized_object",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:resupply_schedule",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match",
                            "beat:orientation",
                            stance="stance:evasive",
                            tell="tell:hesitated",
                            cause="cause:recognized_object",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:orientation")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            cause="cause:recognized_object")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("suspect:piers_dunne",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                stance="stance:defensive",
                                tell="tell:tightened")))
    t.append(("object:resupply_schedule",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:closing_in",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("motive:fishing_economy",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:pursued_suspicion")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:resupply_schedule")))
    return trajectory2(
        "partial_via_callan_misread",
        "Detective spends too long reading Callan's annotations; gets to "
        "Piers late, with the marker but no tidal window confirmation. "
        "Verdict is partial.",
        "partial_correct", "witness_first",
        ["callan_misread", "right_suspect_no_window", "partial_chain",
         "wave2"],
        t, ramp="partial",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  ACCOMPLICE                                                        ║
# ╚════════════════════════════════════════════════════════════════════╝
def accomplice_via_oren_halloway():
    t = []
    t.append(("object:final_report",
              cold_examine("location:research_lab", "object:final_report",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("witness:director",
              cross_to_question("location:common_room",
                                "presence:with_oren_halloway",
                                "object:final_report",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:orientation",
                                stance="stance:cooperative")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_oren_halloway",
                            "object:resupply_schedule",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match",
                            "beat:orientation",
                            cause="cause:recognized_object")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:orientation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("suspect:piers_dunne",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object_focus:none",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:defensive",
                            tell="tell:tightened")))
    t.append(("object:resupply_schedule",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("witness:director",
              return_to_question("location:common_room",
                                 "presence:with_oren_halloway",
                                 "object:final_report",
                                 "atmosphere:silence_holds",
                                 "revelation:contradiction_surfaces",
                                 "beat:investigation",
                                 stance="stance:evasive",
                                 tell="tell:over_explained",
                                 cause="cause:noticed_inconsistency")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:common_room",
                            "presence:with_oren_halloway",
                            "object:weather_log",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:evasive",
                            tell="tell:over_explained",
                            cause="cause:recognized_object")))
    t.append(("modifier:schedule_in_piers_hand",
              stay_question("location:common_room",
                            "presence:with_oren_halloway",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:evasive",
                            tell="tell:over_explained",
                            cause="cause:recognized_object")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:tide_chart",
                               "atmosphere:wind_rises",
                               "revelation:tidal_window_identified",
                               "beat:closing_in",
                               cause="cause:reading_tide_chart",
                               tidal="tidal_tell:tide_recedes")))
    t.append(("motive:fishing_economy",
              recall_alone("location:weather_tower", "object:final_report",
                           "atmosphere:wind_rises",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion")))
    t.append(("travel:to_common_room",
              return_to_question("location:common_room",
                                 "presence:with_piers_dunne",
                                 "object:path_marker",
                                 "atmosphere:silence_holds",
                                 "revelation:confirmation",
                                 "beat:closing_in",
                                 stance="stance:hostile",
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
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges", "beat:verdict_ready",
                           tell="tell:paled",
                           cause="cause:noticed_inconsistency")))
    t.append(("accomplice:oren_halloway",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation", "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:path_marker")))
    return trajectory2(
        "accomplice_via_oren_halloway",
        "Director Halloway named as the accomplice — he had approved the "
        "report's burial and the marker placement, and his evasions "
        "betray the prior knowledge. Piers correctly accused, Halloway "
        "named.",
        "accomplice_found", "object_first",
        ["accomplice_chain", "halloway_named", "director_complicity",
         "wave2"],
        t, ramp="accomplice",
    )


def accomplice_via_kestrel_lin():
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
    t.append(("object:satellite_log",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            cause="cause:examining_evidence")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:rain_against_glass",
                            "revelation:contradiction_surfaces",
                            "beat:orientation",
                            cause="cause:noticed_inconsistency")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:orientation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_research_lab",
              return_to_question("location:research_lab",
                                 "presence:with_kestrel_lin",
                                 "object:radio_handset",
                                 "atmosphere:silence_holds",
                                 "revelation:contradiction_surfaces",
                                 "beat:investigation",
                                 stance="stance:evasive",
                                 tell="tell:hesitated",
                                 cause="cause:noticed_inconsistency",
                                 tidal="tidal_tell:radio_breaks_static")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:recognized_object")))
    t.append(("suspect:piers_dunne",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                stance="stance:defensive",
                                tell="tell:tightened")))
    t.append(("object:resupply_schedule",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:schedule_in_piers_hand",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:noticed_inconsistency")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:tide_chart",
                               "atmosphere:wind_rises",
                               "revelation:tidal_window_identified",
                               "beat:closing_in",
                               cause="cause:reading_tide_chart",
                               tidal="tidal_tell:tide_recedes")))
    t.append(("motive:fishing_economy",
              recall_alone("location:weather_tower", "object:final_report",
                           "atmosphere:wind_rises",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion")))
    t.append(("travel:to_common_room",
              return_to_question("location:common_room",
                                 "presence:with_piers_dunne",
                                 "object:path_marker",
                                 "atmosphere:silence_holds",
                                 "revelation:confirmation",
                                 "beat:closing_in",
                                 stance="stance:hostile",
                                 tell="tell:tightened",
                                 cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:name_uncovered", "beat:closing_in",
                           tell="tell:paled")))
    t.append(("accomplice:kestrel_lin",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:satellite_log",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation", "beat:verdict_ready",
                           tell="tell:silent",
                           cause="cause:noticed_inconsistency")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:path_marker")))
    return trajectory2(
        "accomplice_via_kestrel_lin",
        "Radio operator Kestrel Lin named as the accomplice — the blank "
        "log at the relevant hour was not silence, it was a deletion. "
        "Piers correctly accused, Lin named.",
        "accomplice_found", "object_first",
        ["accomplice_chain", "kestrel_lin_named", "radio_log_complicity",
         "wave2"],
        t, ramp="accomplice",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  FRAMED                                                            ║
# ╚════════════════════════════════════════════════════════════════════╝
def framed_oren_halloway():
    t = []
    t.append(("object:final_report",
              cold_examine("location:research_lab", "object:final_report",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("witness:director",
              cross_to_question("location:common_room",
                                "presence:with_oren_halloway",
                                "object:final_report",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:orientation",
                                stance="stance:defensive",
                                tell="tell:over_explained")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:common_room",
                            "presence:with_oren_halloway",
                            "object:weather_log",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match",
                            "beat:orientation",
                            stance="stance:defensive",
                            tell="tell:over_explained",
                            cause="cause:recognized_object")))
    t.append(("object:journal_letter",
              stay_question("location:common_room",
                            "presence:with_oren_halloway",
                            "object:journal_letter",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:orientation",
                            stance="stance:defensive",
                            tell="tell:over_explained",
                            cause="cause:examining_evidence")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:orientation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:fresh_soil_on_base",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:contradiction_surfaces",
                           "beat:investigation",
                           cause="cause:noticed_inconsistency",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_common_room",
              return_to_question("location:common_room",
                                 "presence:with_oren_halloway",
                                 "object:final_report",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:hostile",
                                 tell="tell:tightened")))
    t.append(("witness:cook",
              return_to_question("location:common_room",
                                 "presence:with_eira_voss",
                                 "object_focus:none",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            cause="cause:recognized_object")))
    t.append(("modifier:storm_warning_issued",
              S("location:common_room", "transition:stayed",
                "cause:noticed_inconsistency",
                "presence:with_oren_halloway", "stance:hostile",
                "action:confronts", "object:weather_log",
                "tell:tightened", "atmosphere:silence_holds",
                "revelation:contradiction_surfaces", "beat:investigation",
                "tidal_tell:none")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:tide_chart",
                               "atmosphere:wind_rises",
                               "revelation:tidal_window_identified",
                               "beat:investigation",
                               cause="cause:reading_tide_chart",
                               tidal="tidal_tell:tide_recedes")))
    t.append(("motive:career_pressure",
              recall_alone("location:weather_tower", "object:final_report",
                           "atmosphere:wind_rises",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion")))
    t.append(("travel:to_common_room",
              return_to_question("location:common_room",
                                 "presence:with_oren_halloway",
                                 "object:final_report",
                                 "atmosphere:silence_holds",
                                 "revelation:name_uncovered",
                                 "beat:closing_in",
                                 stance="stance:hostile",
                                 tell="tell:tightened",
                                 cause="cause:pursued_suspicion")))
    t.append(("object:final_report",
              confront_npc("location:common_room",
                           "presence:with_oren_halloway",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:confirmation", "beat:closing_in",
                           tell="tell:paled")))
    t.append(("object:journal_letter",
              confront_npc("location:common_room",
                           "presence:with_oren_halloway",
                           "object:journal_letter",
                           "atmosphere:dawn_approaches",
                           "revelation:name_uncovered", "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("ACCUSE:suspect:oren_halloway",
              accuse_scene("location:common_room",
                           "presence:with_oren_halloway",
                           obj="object:final_report")))
    return trajectory2(
        "framed_oren_halloway",
        "Detective frames Director Halloway on circumstantial career-"
        "pressure motive. Convergence climbs misleadingly because the "
        "report ties him to the funding council, but the marker mechanism "
        "is Piers's not his.",
        "framed_suspect", "wrong_suspect_first",
        ["framed_chain", "halloway_circumstantial", "career_pressure_motive",
         "high_apparent_convergence_wrong", "wave2"],
        t, ramp="framed",
    )


def framed_kestrel_lin():
    t = []
    t.append(("object:satellite_log",
              cold_examine("location:research_lab", "object:satellite_log",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("witness:radio_operator",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:radio_handset",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            tidal="tidal_tell:radio_breaks_static")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:rain_against_glass",
                            "revelation:contradiction_surfaces",
                            "beat:orientation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:noticed_inconsistency")))
    t.append(("object:radio_handset",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:radio_handset",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:orientation",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("suspect:kestrel_lin",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:radio_handset",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile",
                            tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_research_lab",
              return_to_question("location:research_lab",
                                 "presence:with_kestrel_lin",
                                 "object:satellite_log",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:hostile",
                                 tell="tell:tightened")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile",
                            tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:tide_chart",
                               "atmosphere:wind_rises",
                               "revelation:tidal_window_identified",
                               "beat:investigation",
                               cause="cause:reading_tide_chart",
                               tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_research_lab",
              return_to_question("location:research_lab",
                                 "presence:with_kestrel_lin",
                                 "object:satellite_log",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:closing_in",
                                 stance="stance:hostile",
                                 tell="tell:tightened")))
    t.append(("modifier:radio_log_blank",
              confront_npc("location:research_lab",
                           "presence:with_kestrel_lin",
                           "object:satellite_log",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:noticed_inconsistency")))
    t.append(("object:radio_handset",
              confront_npc("location:research_lab",
                           "presence:with_kestrel_lin",
                           "object:radio_handset",
                           "atmosphere:silence_holds",
                           "revelation:name_uncovered", "beat:closing_in",
                           tell="tell:paled")))
    t.append(("object:satellite_log",
              confront_npc("location:research_lab",
                           "presence:with_kestrel_lin",
                           "object:satellite_log",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation", "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("ACCUSE:suspect:kestrel_lin",
              accuse_scene("location:research_lab",
                           "presence:with_kestrel_lin",
                           obj="object:satellite_log")))
    return trajectory2(
        "framed_kestrel_lin",
        "Detective frames Kestrel Lin on the blank radio log — the "
        "silence reads as guilt instead of as static. Apparent "
        "convergence is high, but the mechanism layer is Piers's.",
        "framed_suspect", "witness_first",
        ["framed_chain", "lin_circumstantial", "radio_log_misread",
         "high_apparent_convergence_wrong", "wave2"],
        t, ramp="framed",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  LATE REVELATION                                                   ║
# ╚════════════════════════════════════════════════════════════════════╝
def late_revelation_after_callan():
    t = []
    t.append(("witness:boat_skipper",
              S("location:research_lab", "transition:none",
                "cause:examining_evidence", "presence:alone", "stance:none",
                "action:examines", "object:tide_chart", "tell:none",
                "atmosphere:rain_against_glass",
                "revelation:partial_match", "beat:orientation",
                "tidal_tell:none")))
    t.append(("travel:to_jetty",
              cross_to_question("location:jetty",
                                "presence:with_mira_callan",
                                "object:tide_chart",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:orientation",
                                stance="stance:evasive",
                                tell="tell:hesitated",
                                tidal="tidal_tell:tide_recedes")))
    for k in range(6):
        t.append(("modifier:tide_data_annotated",
                  stay_question("location:jetty",
                                "presence:with_mira_callan",
                                "object:tide_chart",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:orientation",
                                stance="stance:evasive",
                                tell="tell:hesitated",
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
                           cause="cause:noticed_inconsistency",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("suspect:piers_dunne",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                stance="stance:defensive",
                                tell="tell:tightened")))
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
                            "revelation:name_uncovered",
                            "beat:closing_in",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("motive:fishing_economy",
              recall_alone("location:common_room", "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation", "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:path_marker")))
    return trajectory2(
        "late_revelation_after_callan",
        "Slow-start: detective lingers at the jetty with Callan's tide "
        "annotations; pivots late to the path-marker and lands the "
        "correct accusation just in time.",
        "late_revelation", "witness_first",
        ["late_revelation", "callan_first_then_redirect", "slow_start_fast_close",
         "wave2"],
        t, ramp="late",
    )


def late_revelation_after_storm_pass():
    t = []
    t.append(("object:weather_log",
              cold_examine("location:research_lab", "object:weather_log",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:weather_log",
                               "atmosphere:rain_against_glass",
                               "revelation:partial_match", "beat:orientation",
                               tidal="tidal_tell:storm_intensifies")))
    for k in range(6):
        t.append(("modifier:storm_warning_issued",
                  cold_examine("location:weather_tower",
                               "object:weather_log",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:orientation",
                               cause="cause:recognized_object",
                               tidal="tidal_tell:storm_intensifies")))
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
                           cause="cause:noticed_inconsistency",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("suspect:piers_dunne",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                stance="stance:defensive",
                                tell="tell:tightened")))
    t.append(("modifier:schedule_in_piers_hand",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:name_uncovered", "beat:closing_in",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("motive:fishing_economy",
              recall_alone("location:common_room", "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation", "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:path_marker")))
    return trajectory2(
        "late_revelation_after_storm_pass",
        "Slow-start: detective re-reads the weather log six times while "
        "the storm passes over the island; pivots late to the marker "
        "and the schedule and lands the correct accusation.",
        "late_revelation", "object_first",
        ["late_revelation", "weather_tower_first", "storm_pass",
         "slow_start_fast_close", "wave2"],
        t, ramp="late",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  MOTIVE-ONLY CONFESSION                                            ║
# ╚════════════════════════════════════════════════════════════════════╝
def motive_only_via_protected_area_report():
    t = []
    t.append(("object:final_report",
              cold_examine("location:research_lab", "object:final_report",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("modifier:processing_facility_loan_due",
              cold_examine("location:research_lab", "object:final_report",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           cause="cause:recognized_object")))
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
                            "revelation:partial_match",
                            "beat:orientation",
                            cause="cause:recognized_object")))
    t.append(("suspect:piers_dunne",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object_focus:none",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:orientation",
                            stance="stance:defensive",
                            tell="tell:tightened")))
    t.append(("object:final_report",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:processing_facility_loan_due",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("motive:fishing_economy",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:motive_emerges",
                            "beat:closing_in",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:pursued_suspicion")))
    t.append(("motive:family_on_the_boats",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:motive_emerges",
                            "beat:closing_in",
                            stance="stance:defensive",
                            tell="tell:paled",
                            cause="cause:pursued_suspicion")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:paled",
                           cause="cause:noticed_inconsistency")))
    t.append(("object:final_report",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges", "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:final_report")))
    return trajectory2(
        "motive_only_via_protected_area_report",
        "Detective never visits the path-marker. Confronts Piers solely "
        "on the protected-area report and the loan papers; Piers "
        "confesses only to the motive — the killing remains technically "
        "unproven.",
        "motive_only_confession", "object_first",
        ["motive_first_chain", "protected_area_report_anchor",
         "loan_papers_first", "no_marker_chain", "wave2"],
        t, ramp="motive_only",
    )


def motive_only_via_fishing_quota_threat():
    t = []
    t.append(("modifier:processing_facility_loan_due",
              cold_examine("location:research_lab", "object:final_report",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none",
                           cause="cause:recognized_object")))
    t.append(("witness:boat_skipper",
              cross_to_question("location:jetty",
                                "presence:with_mira_callan",
                                "object_focus:none",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:orientation",
                                stance="stance:evasive",
                                tell="tell:hesitated",
                                tidal="tidal_tell:tide_recedes")))
    t.append(("motive:fishing_economy",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object_focus:none",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match",
                            "beat:orientation",
                            stance="stance:evasive",
                            tell="tell:hesitated",
                            cause="cause:pursued_suspicion",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:orientation")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:orientation",
                            cause="cause:recognized_object")))
    t.append(("suspect:piers_dunne",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object_focus:none",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:defensive",
                            tell="tell:tightened")))
    t.append(("object:final_report",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("motive:fishing_economy",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:motive_emerges",
                            "beat:closing_in",
                            stance="stance:defensive",
                            tell="tell:paled",
                            cause="cause:pursued_suspicion")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:paled",
                           cause="cause:recognized_object")))
    t.append(("motive:family_on_the_boats",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object_focus:none",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges",
                           "beat:closing_in",
                           tell="tell:silent",
                           cause="cause:pursued_suspicion")))
    t.append(("motive:fishing_economy",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges",
                           "beat:verdict_ready",
                           tell="tell:silent",
                           cause="cause:pursued_suspicion")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:final_report")))
    return trajectory2(
        "motive_only_via_fishing_quota_threat",
        "Detective never visits the eastern path; argues the fishing "
        "quota threat alone. Piers confesses to the motive only.",
        "motive_only_confession", "object_first",
        ["motive_first_chain", "fishing_quota_anchored",
         "no_marker_chain", "wave2"],
        t, ramp="motive_only",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  NEAR MISS  (NEW outcome class)                                    ║
# ╚════════════════════════════════════════════════════════════════════╝
def near_miss_recovers_from_webb():
    """Detective opens chasing Webb; recovers to Piers under thin
    convergence — barely-correct verdict."""
    t = []
    t.append(("suspect:marcus_webb",
              S("location:research_lab", "transition:none",
                "cause:examining_evidence",
                "presence:with_marcus_webb", "stance:hostile",
                "action:questions", "object:journal_letter",
                "tell:tightened",
                "atmosphere:rain_against_glass",
                "revelation:partial_match", "beat:orientation",
                "tidal_tell:none")))
    t.append(("object:journal_letter",
              stay_question("location:research_lab",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:hostile",
                            tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:storm_warning_issued",
              cross_to_examine("location:weather_tower", "object:weather_log",
                               "atmosphere:wind_rises",
                               "revelation:partial_match", "beat:orientation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:orientation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:contradiction_surfaces",
                           "beat:investigation",
                           cause="cause:noticed_inconsistency",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:fresh_soil_on_base",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match",
                           "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("suspect:piers_dunne",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                stance="stance:defensive",
                                tell="tell:tightened")))
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
                            "revelation:name_uncovered",
                            "beat:closing_in",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("motive:fishing_economy",
              recall_alone("location:common_room", "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:confirmation", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:path_marker")))
    return trajectory2(
        "near_miss_recovers_from_webb",
        "Detective opens chasing Webb's journal letter, recovers to Piers "
        "via the marker and the schedule. Barely-correct verdict — "
        "convergence around 0.78. Could have gone either way.",
        "near_miss", "wrong_suspect_first",
        ["near_miss", "webb_first", "recovers_to_dunne",
         "barely_correct", "wave2"],
        t, ramp="partial",
    )


def near_miss_recovers_from_callan():
    t = []
    t.append(("suspect:mira_callan",
              S("location:research_lab", "transition:none",
                "cause:examining_evidence",
                "presence:with_mira_callan", "stance:hostile",
                "action:questions", "object:tide_chart",
                "tell:tightened",
                "atmosphere:rain_against_glass",
                "revelation:partial_match", "beat:orientation",
                "tidal_tell:none")))
    t.append(("travel:to_jetty",
              cross_to_question("location:jetty",
                                "presence:with_mira_callan",
                                "object:tide_chart",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:orientation",
                                stance="stance:hostile",
                                tell="tell:tightened",
                                tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match",
                            "beat:orientation",
                            stance="stance:evasive",
                            tell="tell:hesitated",
                            cause="cause:recognized_object",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:orientation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:contradiction_surfaces",
                           "beat:investigation",
                           cause="cause:noticed_inconsistency",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("suspect:piers_dunne",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                stance="stance:defensive",
                                tell="tell:tightened")))
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
                            "revelation:name_uncovered", "beat:closing_in",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("motive:fishing_economy",
              recall_alone("location:common_room", "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:confirmation", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:path_marker")))
    return trajectory2(
        "near_miss_recovers_from_callan",
        "Detective opens by interrogating Callan as the suspect, only "
        "recovers to Piers in the closing turns. Barely-correct verdict.",
        "near_miss", "wrong_suspect_first",
        ["near_miss", "callan_first", "recovers_to_dunne",
         "barely_correct", "wave2"],
        t, ramp="partial",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  RED HERRING TRAP                                                  ║
# ╚════════════════════════════════════════════════════════════════════╝
def red_herring_trap_storm_alibi_decoy():
    t = []
    t.append(("object:weather_log",
              cold_examine("location:research_lab", "object:weather_log",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("witness:methodology_reviewer",
              cross_to_question("location:dorms",
                                "presence:with_marcus_webb",
                                "object:journal_letter",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:orientation",
                                stance="stance:hostile",
                                tell="tell:tightened")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:weather_log",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("object:journal_letter",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile",
                            tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("motive:methodology_grievance",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:hostile",
                            tell="tell:tightened",
                            cause="cause:noticed_inconsistency")))
    t.append(("travel:to_research_lab",
              return_to_examine("location:research_lab", "object:final_report",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("witness:methodology_reviewer",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:hostile",
                                 tell="tell:tightened")))
    t.append(("modifier:storm_warning_issued",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:weather_log",
                           "atmosphere:silence_holds",
                           "revelation:partial_match",
                           "beat:investigation",
                           tell="tell:tightened",
                           cause="cause:recognized_object")))
    t.append(("object:final_report",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:name_uncovered", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("motive:methodology_grievance",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:journal_letter",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:pursued_suspicion")))
    t.append(("object:journal_letter",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:journal_letter",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation", "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("ACCUSE:suspect:marcus_webb",
              accuse_scene("location:dorms",
                           "presence:with_marcus_webb",
                           obj="object:journal_letter")))
    return trajectory2(
        "red_herring_trap_storm_alibi_decoy",
        "Storm-alibi decoy: detective reads Webb's storm-night absence "
        "as guilt, never visits the eastern path or the schedule, accuses "
        "Webb at high apparent convergence. Trap closes.",
        "red_herring_trap", "wrong_suspect_first",
        ["red_herring_trap", "storm_alibi_decoy", "webb_circumstantial",
         "high_apparent_convergence", "wave2"],
        t, ramp="red_herring",
    )


def red_herring_trap_satellite_log_misread():
    t = []
    t.append(("object:satellite_log",
              cold_examine("location:research_lab", "object:satellite_log",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("witness:radio_operator",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:defensive", tell="tell:tightened",
                            tidal="tidal_tell:radio_breaks_static")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:rain_against_glass",
                            "revelation:contradiction_surfaces",
                            "beat:orientation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:noticed_inconsistency")))
    t.append(("object:radio_handset",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:radio_handset",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:defensive",
                            tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("suspect:kestrel_lin",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile",
                            tell="tell:tightened")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile",
                            tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:partial_match",
                            "beat:investigation",
                            stance="stance:hostile",
                            tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("object:radio_handset",
              confront_npc("location:research_lab",
                           "presence:with_kestrel_lin",
                           "object:radio_handset",
                           "atmosphere:silence_holds",
                           "revelation:name_uncovered", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("motive:methodology_grievance",
              confront_npc("location:research_lab",
                           "presence:with_kestrel_lin",
                           "object:satellite_log",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:pursued_suspicion")))
    t.append(("object:satellite_log",
              confront_npc("location:research_lab",
                           "presence:with_kestrel_lin",
                           "object:satellite_log",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation", "beat:verdict_ready",
                           tell="tell:silent")))
    t.append(("ACCUSE:suspect:kestrel_lin",
              accuse_scene("location:research_lab",
                           "presence:with_kestrel_lin",
                           obj="object:satellite_log")))
    return trajectory2(
        "red_herring_trap_satellite_log_misread",
        "Satellite-log decoy: detective reads the silent uplink window as "
        "Lin's guilt rather than as the storm. Apparent convergence is "
        "high but the marker mechanism is Piers's.",
        "red_herring_trap", "witness_first",
        ["red_herring_trap", "satellite_log_misread", "lin_circumstantial",
         "high_apparent_convergence", "wave2"],
        t, ramp="red_herring",
    )


# ─── Main ────────────────────────────────────────────────────────────────
def main():
    builders = [
        # Correct (4)
        dunne_via_sea_cave,
        dunne_via_radio_summons,
        dunne_via_storm_pursuit,
        dunne_via_weather_tower_radio,
        # Wrong v2 (4)
        wrong_marcus_webb_v2,
        wrong_mira_callan_v2,
        wrong_oren_halloway_v2,
        wrong_tovi_ansgar_v2,
        # Cold trails (2)
        cold_trail_sea_cave_loop,
        cold_trail_storm_summons_loop,
        # Partial (3)
        partial_dunne_wrong_marker,
        partial_motive_only_window,
        partial_via_callan_misread,
        # Accomplice (2)
        accomplice_via_oren_halloway,
        accomplice_via_kestrel_lin,
        # Framed (2)
        framed_oren_halloway,
        framed_kestrel_lin,
        # Late revelation (2)
        late_revelation_after_callan,
        late_revelation_after_storm_pass,
        # Motive-only (2)
        motive_only_via_protected_area_report,
        motive_only_via_fishing_quota_threat,
        # Near miss (2)
        near_miss_recovers_from_webb,
        near_miss_recovers_from_callan,
        # Red herring (2)
        red_herring_trap_storm_alibi_decoy,
        red_herring_trap_satellite_log_misread,
    ]
    assert len(builders) == 25, f"expected 25 builders, got {len(builders)}"

    out_dir = HERE
    new_entries = []
    for build in builders:
        traj = build()
        traj_id = traj["trajectory_id"]
        path = out_dir / f"{traj_id}.json"
        with open(path, "w") as f:
            json.dump(traj, f, indent=2)
        new_entries.append({
            "id": traj_id,
            "outcome": traj["outcome"],
            "length": len(traj["turns"]),
            "starting_hypothesis": traj["starting_hypothesis"],
            "tags": traj["tags"],
        })
        print(f"  wrote {traj_id}  ({len(traj['turns'])} turns)")

    # Merge into existing manifest (preserve wave 1 entries).
    manifest_path = out_dir / "manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)
    existing_ids = {e["id"] for e in manifest["trajectories"]}
    for e in new_entries:
        if e["id"] not in existing_ids:
            manifest["trajectories"].append(e)
    manifest["_comment"] = (
        "Index of hand-authored trajectories for The Tidal Interval. "
        "Wave 2 of 2 (50 total = 25 wave1 + 25 wave2). The trainer "
        "loads the manifest first, then reads each listed trajectory file."
    )
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nUpdated manifest.json — {len(manifest['trajectories'])} total entries.")


if __name__ == "__main__":
    main()
