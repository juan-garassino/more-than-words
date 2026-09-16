#!/usr/bin/env python3
"""
Authoring helper for tidal_interval — 10 counterfactual branches.

Each CF is a short (5-8 turns) standalone trajectory that diverges from a
parent wave-1 trajectory at a named anchor turn and dimension, leading to
a different outcome class. CFs are saved as `cf_<src>_<label>.json` files,
appended to the manifest with `starting_hypothesis = "counterfactual"`.

Run once:
    python3 living_tales/trainer/cases/tidal_interval/trajectories/_author_cfs.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _author_wave1 import (  # noqa: E402
    S, cold_examine, cross_to_examine, return_to_examine,
    cross_to_question, stay_question, return_to_question,
    confront_npc, recall_alone, accuse_scene,
)


def cf_opening(loc: str) -> Dict[str, Any]:
    """Per-CF opening — anchor location seeds visited set."""
    return {
        "tokens": [loc, "event:sarah_does_not_return",
                   "event:final_report_approved"],
    }


def cf_trajectory(traj_id: str,
                  description: str,
                  outcome: str,
                  branch_of: str,
                  branch_turn: int,
                  divergence_token: str,
                  tags: List[str],
                  turns_specs: List[Tuple[str, Dict]],
                  opening_loc: str,
                  accused: str,
                  base_conv: float = 0.68,
                  turn_offset: int = 37) -> Dict[str, Any]:
    """Build a CF — turns get convergence_after derived from a thin gradient
    relative to the anchor turn's convergence. The CF's first turn carries
    a game_turn number offset (default 38) so that the dawn_approaches
    atmosphere is legal in the verdict scene. `pre_branch_state` seeds the
    validator with the inherited convergence from the parent at the
    divergence point — required to honor BEAT/REVELATION gates."""
    turns = []
    for i, (card, scene) in enumerate(turns_specs, start=1):
        conv = round(min(0.88, base_conv + 0.04 * i), 3)
        turns.append({
            "turn": turn_offset + i,
            "player_card": card,
            "scene": scene,
            "convergence_after": [conv, conv, conv],
        })
    last_conv = turns[-1]["convergence_after"]
    if outcome == "near_miss":
        ending_type = "near_miss"
    elif outcome.startswith("correct_"):
        ending_type = "all_strong"
    elif outcome.startswith("partial_"):
        ending_type = "partial"
    elif outcome == "cold_trail":
        ending_type = "cold"
    elif outcome == "late_revelation":
        ending_type = "all_strong"
    elif outcome.startswith("accomplice_"):
        ending_type = "all_strong"
    elif outcome == "motive_only_confession":
        ending_type = "partial"
    else:
        ending_type = "wrong"
    ending = {
        "type": ending_type,
        "accused": accused,
        "final_convergence": last_conv,
        "_note": f"Counterfactual branch — see branch_of={branch_of}",
    }
    return {
        "schema_version": 1,
        "trajectory_id": traj_id,
        "case_id": "tidal_interval",
        "description": description,
        "outcome": outcome,
        "starting_hypothesis": "counterfactual",
        "branch_of": branch_of,
        "branch_turn": branch_turn,
        "divergence_token": divergence_token,
        "tags": tags,
        "_authoring_note": (
            f"CF — diverges from {branch_of} at turn {branch_turn} on "
            f"{divergence_token}."
        ),
        "pre_branch_state": {
            "convergence_dims": [base_conv, base_conv, base_conv],
        },
        "opening": cf_opening(opening_loc),
        "turns": turns,
        "ending": ending,
    }


# ─── CF builders ─────────────────────────────────────────────────────────

# 1. dunne_via_path_marker → diverge at TIDAL_TELL → motive_only_confession
def cf_dunne_via_path_marker_motive_only():
    t = []
    t.append(("object:resupply_schedule",
              S("location:common_room", "transition:none",
                "cause:examining_evidence", "presence:with_piers_dunne",
                "stance:defensive", "action:examines",
                "object:resupply_schedule", "tell:tightened",
                "atmosphere:silence_holds",
                "revelation:partial_match", "beat:investigation",
                "tidal_tell:none")))
    t.append(("modifier:processing_facility_loan_due",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:closing_in",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("motive:fishing_economy",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:motive_emerges", "beat:closing_in",
                            stance="stance:defensive", tell="tell:paled",
                            cause="cause:pursued_suspicion")))
    t.append(("motive:family_on_the_boats",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:silent",
                           cause="cause:pursued_suspicion")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges", "beat:verdict_ready",
                           tell="tell:silent",
                           cause="cause:recognized_object")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:final_report")))
    return cf_trajectory(
        "cf_dunne_via_path_marker_motive_only",
        "Counterfactual: at the closing turns of dunne_via_path_marker, "
        "the marker mechanism is dropped and only the motive is "
        "confronted. Piers confesses to the motive only — no mechanism.",
        "motive_only_confession",
        "dunne_via_path_marker", 28,
        "TIDAL_TELL=tidal_tell:none",
        ["counterfactual", "tidal_tell_divergence",
         "motive_only_confession", "wave2_cf"],
        t, "location:common_room", "suspect:piers_dunne",
    )


# 2. dunne_via_tidal_window → diverge at OBJECT_FOCUS → wrong_marcus_webb
def cf_dunne_via_tidal_window_to_webb():
    t = []
    t.append(("object:journal_letter",
              S("location:research_lab", "transition:none",
                "cause:examining_evidence", "presence:alone", "stance:none",
                "action:examines", "object:journal_letter", "tell:none",
                "atmosphere:silence_holds",
                "revelation:partial_match", "beat:investigation",
                "tidal_tell:none")))
    t.append(("witness:methodology_reviewer",
              cross_to_question("location:dorms",
                                "presence:with_marcus_webb",
                                "object:journal_letter",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                stance="stance:hostile",
                                tell="tell:tightened")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:weather_log",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("object:journal_letter",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:journal_letter",
                           "atmosphere:silence_holds",
                           "revelation:name_uncovered", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("motive:methodology_grievance",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:journal_letter",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges", "beat:verdict_ready",
                           tell="tell:silent",
                           cause="cause:pursued_suspicion")))
    t.append(("ACCUSE:suspect:marcus_webb",
              accuse_scene("location:dorms",
                           "presence:with_marcus_webb",
                           obj="object:journal_letter")))
    return cf_trajectory(
        "cf_dunne_via_tidal_window_to_webb",
        "Counterfactual: at the tidal_window scene in dunne_via_tidal_window, "
        "the player pivots to Webb's journal letter instead. Apparent "
        "convergence builds toward Webb — wrong verdict.",
        "wrong_marcus_webb",
        "dunne_via_tidal_window", 18,
        "OBJECT_FOCUS=object:journal_letter",
        ["counterfactual", "object_focus_divergence",
         "wrong_marcus_webb", "wave2_cf"],
        t, "location:research_lab", "suspect:marcus_webb",
    )


# 3. dunne_via_radio_log → diverge at PRESENCE → accomplice_found
def cf_dunne_via_radio_log_to_accomplice():
    t = []
    t.append(("witness:radio_operator",
              S("location:research_lab", "transition:none",
                "cause:noticed_inconsistency",
                "presence:with_kestrel_lin", "stance:evasive",
                "action:questions", "object:satellite_log",
                "tell:hesitated", "atmosphere:silence_holds",
                "revelation:contradiction_surfaces", "beat:investigation",
                "tidal_tell:radio_breaks_static")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:closing_in",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:noticed_inconsistency")))
    t.append(("suspect:piers_dunne",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:resupply_schedule",
                                "atmosphere:silence_holds",
                                "revelation:name_uncovered",
                                "beat:closing_in",
                                stance="stance:defensive",
                                tell="tell:tightened")))
    t.append(("motive:fishing_economy",
              recall_alone("location:common_room", "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion")))
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
                           obj="object:satellite_log")))
    return cf_trajectory(
        "cf_dunne_via_radio_log_to_accomplice",
        "Counterfactual: in dunne_via_radio_log, the radio operator's "
        "hesitation is read as complicity rather than as static. Piers "
        "correctly accused; Lin named as accomplice.",
        "accomplice_found",
        "dunne_via_radio_log", 14,
        "PRESENCE=presence:with_kestrel_lin",
        ["counterfactual", "presence_divergence",
         "accomplice_found", "wave2_cf"],
        t, "location:research_lab", "suspect:piers_dunne",
    )


# 4. wrong_marcus_webb → diverge at CAUSE → correct_piers_dunne
def cf_wrong_marcus_webb_to_correct():
    t = []
    t.append(("modifier:schedule_in_piers_hand",
              S("location:common_room", "transition:none",
                "cause:noticed_inconsistency",
                "presence:with_piers_dunne", "stance:defensive",
                "action:notices", "object:resupply_schedule",
                "tell:tightened", "atmosphere:silence_holds",
                "revelation:contradiction_surfaces", "beat:investigation",
                "tidal_tell:none")))
    t.append(("object:path_marker",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:path_marker",
                            "atmosphere:silence_holds",
                            "revelation:name_uncovered", "beat:closing_in",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:noticed_inconsistency")))
    t.append(("modifier:processing_facility_loan_due",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:motive_emerges", "beat:closing_in",
                            stance="stance:defensive", tell="tell:paled",
                            cause="cause:noticed_inconsistency")))
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
    return cf_trajectory(
        "cf_wrong_marcus_webb_to_correct",
        "Counterfactual: in wrong_marcus_webb, the detective notices the "
        "inconsistency in the schedule instead of dismissing it; pivots "
        "to Piers and lands the correct verdict.",
        "correct_piers_dunne",
        "wrong_marcus_webb", 22,
        "CAUSE=cause:noticed_inconsistency",
        ["counterfactual", "cause_divergence",
         "correct_piers_dunne", "wave2_cf"],
        t, "location:common_room", "suspect:piers_dunne",
    )


# 5. accomplice_via_callan → diverge at STANCE → cold_trail
def cf_accomplice_via_callan_to_cold():
    t = []
    t.append(("witness:boat_skipper",
              S("location:jetty", "transition:none",
                "cause:examining_evidence",
                "presence:with_mira_callan", "stance:cooperative",
                "action:questions", "object_focus:none", "tell:none",
                "atmosphere:waves_against_rock",
                "revelation:partial_match", "beat:investigation",
                "tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:cooperative", tell="tell:none",
                            cause="cause:recognized_object",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("object:tide_chart",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:dead_end", "beat:investigation",
                            stance="stance:cooperative", tell="tell:none",
                            cause="cause:reading_tide_chart",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:walk_routine_documented",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:resupply_schedule",
                            "atmosphere:waves_against_rock",
                            "revelation:dead_end", "beat:investigation",
                            stance="stance:cooperative", tell="tell:none",
                            cause="cause:recognized_object",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("witness:boat_skipper",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object_focus:none",
                            "atmosphere:waves_against_rock",
                            "revelation:dead_end", "beat:investigation",
                            stance="stance:cooperative", tell="tell:none",
                            tidal="tidal_tell:tide_recedes")))
    return cf_trajectory(
        "cf_accomplice_via_callan_to_cold",
        "Counterfactual: in accomplice_via_callan, Callan reads as "
        "cooperative rather than evasive; her hesitation is taken at "
        "face value. The lead dissolves into a cold trail.",
        "cold_trail",
        "accomplice_via_callan", 20,
        "STANCE=stance:cooperative",
        ["counterfactual", "stance_divergence",
         "cold_trail", "wave2_cf"],
        t, "location:jetty", None,
        base_conv=0.30, turn_offset=20,
    )


# 6. framed_marcus_webb → diverge at REVELATION → correct_piers_dunne
def cf_framed_marcus_webb_to_correct():
    t = []
    t.append(("modifier:marker_displaced_eleven_meters",
              S("location:eastern_path", "transition:none",
                "cause:noticed_inconsistency", "presence:alone",
                "stance:none", "action:examines", "object:path_marker",
                "tell:none", "atmosphere:wind_rises",
                "revelation:contradiction_surfaces", "beat:investigation",
                "tidal_tell:storm_intensifies")))
    t.append(("modifier:fresh_soil_on_base",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("suspect:piers_dunne",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:resupply_schedule",
                                "atmosphere:silence_holds",
                                "revelation:name_uncovered",
                                "beat:closing_in",
                                stance="stance:defensive",
                                tell="tell:tightened")))
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
    return cf_trajectory(
        "cf_framed_marcus_webb_to_correct",
        "Counterfactual: in framed_marcus_webb, the contradiction at the "
        "marker is recognized as Piers's not Webb's. Pivots to Piers, "
        "correct verdict.",
        "correct_piers_dunne",
        "framed_marcus_webb", 16,
        "REVELATION=revelation:contradiction_surfaces",
        ["counterfactual", "revelation_divergence",
         "correct_piers_dunne", "wave2_cf"],
        t, "location:eastern_path", "suspect:piers_dunne",
    )


# 7. red_herring_trap_storm_alibi → diverge at BEAT → near_miss
def cf_red_herring_trap_storm_alibi_to_near_miss():
    t = []
    t.append(("travel:to_eastern_path",
              S("location:eastern_path", "transition:none",
                "cause:examining_evidence", "presence:alone",
                "stance:none", "action:examines", "object:path_marker",
                "tell:none", "atmosphere:wind_rises",
                "revelation:partial_match", "beat:investigation",
                "tidal_tell:storm_intensifies")))
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
    return cf_trajectory(
        "cf_red_herring_trap_storm_alibi_to_near_miss",
        "Counterfactual: in red_herring_trap_storm_alibi, the detective "
        "doesn't reach beat:verdict_ready against Webb; instead pivots "
        "to Piers at the last possible moment. Barely-correct.",
        "near_miss",
        "red_herring_trap_storm_alibi", 24,
        "BEAT=beat:investigation",
        ["counterfactual", "beat_divergence",
         "near_miss", "wave2_cf"],
        t, "location:eastern_path", "suspect:piers_dunne",
    )


# 8. cold_trail_radio_silence → diverge at ATMOSPHERE → late_revelation
def cf_cold_trail_radio_silence_to_late():
    t = []
    t.append(("object:radio_handset",
              S("location:research_lab", "transition:none",
                "cause:noticed_inconsistency",
                "presence:with_kestrel_lin", "stance:cooperative",
                "action:radios", "object:radio_handset", "tell:none",
                "atmosphere:wind_rises",
                "revelation:contradiction_surfaces", "beat:investigation",
                "tidal_tell:radio_breaks_static")))
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:satellite_log",
                            "atmosphere:wind_rises",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:radio_breaks_static")))
    t.append(("travel:to_eastern_path",
              cross_to_examine("location:eastern_path", "object:path_marker",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:marker_displaced_eleven_meters",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:name_uncovered", "beat:closing_in",
                           cause="cause:noticed_inconsistency",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("suspect:piers_dunne",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:resupply_schedule",
                                "atmosphere:silence_holds",
                                "revelation:name_uncovered",
                                "beat:closing_in",
                                stance="stance:defensive",
                                tell="tell:tightened")))
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
    return cf_trajectory(
        "cf_cold_trail_radio_silence_to_late",
        "Counterfactual: in cold_trail_radio_silence, the rising wind "
        "breaks the bench's stasis; the detective pivots out, lands a "
        "late but correct verdict.",
        "late_revelation",
        "cold_trail_radio_silence", 18,
        "ATMOSPHERE=atmosphere:wind_rises",
        ["counterfactual", "atmosphere_divergence",
         "late_revelation", "wave2_cf"],
        t, "location:research_lab", "suspect:piers_dunne",
    )


# 9. partial_dunne_misread_motive_a → diverge at TIDAL_TELL → correct
def cf_partial_dunne_misread_motive_a_to_correct():
    t = []
    t.append(("travel:to_eastern_path",
              S("location:eastern_path", "transition:none",
                "cause:revisiting_scene", "presence:alone", "stance:none",
                "action:traces_route", "object:path_marker", "tell:none",
                "atmosphere:wind_rises",
                "revelation:tidal_window_identified", "beat:closing_in",
                "tidal_tell:path_unstable")))
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
                                "revelation:confirmation", "beat:closing_in",
                                stance="stance:hostile", tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
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
                           obj="object:path_marker")))
    return cf_trajectory(
        "cf_partial_dunne_misread_motive_a_to_correct",
        "Counterfactual: in partial_dunne_misread_motive_a, the path "
        "becomes unstable at the right moment — the tidal window snaps "
        "into focus and the motive aligns. Correct verdict.",
        "correct_piers_dunne",
        "partial_dunne_misread_motive_a", 26,
        "TIDAL_TELL=tidal_tell:path_unstable",
        ["counterfactual", "tidal_tell_divergence",
         "correct_piers_dunne", "wave2_cf"],
        t, "location:eastern_path", "suspect:piers_dunne",
    )


# 10. late_revelation_after_webb → diverge at TRANSITION → near_miss
def cf_late_revelation_after_webb_to_near_miss():
    t = []
    t.append(("travel:to_common_room",
              S("location:common_room", "transition:none",
                "cause:pursued_suspicion",
                "presence:with_piers_dunne", "stance:defensive",
                "action:questions", "object:resupply_schedule",
                "tell:tightened", "atmosphere:silence_holds",
                "revelation:partial_match", "beat:investigation",
                "tidal_tell:none")))
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
    return cf_trajectory(
        "cf_late_revelation_after_webb_to_near_miss",
        "Counterfactual: in late_revelation_after_webb, the detective "
        "stays in the common room instead of pursuing the marker; "
        "convergence rises just enough for a thin verdict. Barely-correct.",
        "near_miss",
        "late_revelation_after_webb", 28,
        "TRANSITION=transition:stayed",
        ["counterfactual", "transition_divergence",
         "near_miss", "wave2_cf"],
        t, "location:common_room", "suspect:piers_dunne",
    )


# ─── Main ────────────────────────────────────────────────────────────────
def main():
    builders = [
        cf_dunne_via_path_marker_motive_only,
        cf_dunne_via_tidal_window_to_webb,
        cf_dunne_via_radio_log_to_accomplice,
        cf_wrong_marcus_webb_to_correct,
        cf_accomplice_via_callan_to_cold,
        cf_framed_marcus_webb_to_correct,
        cf_red_herring_trap_storm_alibi_to_near_miss,
        cf_cold_trail_radio_silence_to_late,
        cf_partial_dunne_misread_motive_a_to_correct,
        cf_late_revelation_after_webb_to_near_miss,
    ]
    assert len(builders) == 10, f"expected 10 CFs, got {len(builders)}"

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
            "starting_hypothesis": "counterfactual",
            "tags": traj["tags"],
        })
        print(f"  wrote {traj_id}  ({len(traj['turns'])} turns)")

    # Append to manifest.
    manifest_path = out_dir / "manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)
    existing_ids = {e["id"] for e in manifest["trajectories"]}
    for e in new_entries:
        if e["id"] not in existing_ids:
            manifest["trajectories"].append(e)
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nUpdated manifest.json — {len(manifest['trajectories'])} total entries.")


if __name__ == "__main__":
    main()
