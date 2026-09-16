#!/usr/bin/env python3
"""Wave 1 part D — remaining 11 builders + manifest + writer."""
from __future__ import annotations
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _author_wave1 import (  # noqa: E402
    S, conv_after, trajectory, DEFAULT_OPENING,
    cold_examine, cross_to_examine, return_to_examine,
    cross_to_question, stay_question, return_to_question,
    confront_npc, recall_alone, discover_alone, trace_route,
    radio_in, wait_alone, accuse_scene,
    dunne_via_path_marker, dunne_via_tidal_window, dunne_via_radio_log,
    dunne_via_callan_corroboration, dunne_via_webb_alibi_collapse,
    dunne_via_research_notebook,
)
from _author_wave1_b import (  # noqa: E402
    wrong_marcus_webb, wrong_mira_callan, wrong_oren_halloway,
    wrong_tovi_ansgar, wrong_niall_brackett, wrong_kestrel_lin,
)
from _author_wave1_c import (  # noqa: E402
    cold_trail_circular, cold_trail_storm_loop, cold_trail_radio_silence,
)


# Helper: orientation block (5 turns) common across partials/accomplice
def orient_marker_open():
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
    return t


def mid_investigation_marker_only():
    """Investigation block — marker chain but motive is misread."""
    t = []
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:tide_chart",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               cause="cause:reading_tide_chart")))
    t.append(("object:tide_chart",
              cold_examine("location:weather_tower", "object:tide_chart",
                           "atmosphere:wind_rises",
                           "revelation:contradiction_surfaces",
                           "beat:investigation",
                           cause="cause:noticed_inconsistency")))
    t.append(("travel:to_common_room",
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
    t.append(("travel:to_eastern_path",
              return_to_examine("location:eastern_path", "object:path_marker",
                                "atmosphere:wind_rises",
                                "revelation:partial_match",
                                "beat:investigation",
                                cause="cause:revisiting_scene",
                                tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:socket_hole_compressed",
              cold_examine("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
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
    return t


# ╔════════════════════════════════════════════════════════════════════╗
# ║  PARTIAL CORRECT — partial_dunne_misread_motive_a                  ║
# ║  Right suspect, wrong motive (career_pressure not fishing_economy) ║
# ╚════════════════════════════════════════════════════════════════════╝
def partial_dunne_misread_motive_a():
    t = orient_marker_open()
    t.extend(mid_investigation_marker_only())
    # Pursue Piers via career_pressure (wrong motive)
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
    t.append(("motive:career_pressure",
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
                                "revelation:partial_match",
                                "beat:closing_in",
                                stance="stance:defensive",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:confirmation",
                           "beat:closing_in")))
    t.append(("motive:career_pressure",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:noticed_inconsistency")))
    t.append(("object:resupply_schedule",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:resupply_schedule",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("modifier:schedule_in_piers_hand",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:resupply_schedule",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
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
                            "revelation:partial_match", "beat:closing_in",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:path_marker",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:closing_in",
                                stance="stance:hostile",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:final_report",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("motive:career_pressure",
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
                           obj="object:path_marker",
                           atmos="atmosphere:silence_holds",
                           revel="revelation:partial_match")))
    return trajectory(
        "partial_dunne_misread_motive_a",
        "Right suspect, wrong motive. The detective gets Piers via the "
        "marker chain but reads the motive as career pressure rather "
        "than the deeper fishing-economy crisis. Partial verdict.",
        "partial_correct", "object_first",
        ["right_suspect_wrong_motive", "career_pressure_misread",
         "partial_chain"],
        t, ramp="partial",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  PARTIAL CORRECT — partial_dunne_misread_motive_b                  ║
# ║  Right suspect, wrong motive (father_legacy not fishing_economy)   ║
# ╚════════════════════════════════════════════════════════════════════╝
def partial_dunne_misread_motive_b():
    t = orient_marker_open()
    t.extend(mid_investigation_marker_only())
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
    t.append(("motive:father_legacy",
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
                                "revelation:partial_match",
                                "beat:closing_in",
                                stance="stance:defensive",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:confirmation",
                           "beat:closing_in")))
    t.append(("motive:father_legacy",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:noticed_inconsistency")))
    t.append(("object:resupply_schedule",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:resupply_schedule",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("modifier:schedule_in_piers_hand",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:resupply_schedule",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
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
                            "revelation:partial_match", "beat:closing_in",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:path_marker",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:closing_in",
                                stance="stance:hostile",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("motive:father_legacy",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:pursued_suspicion")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:path_marker",
                           atmos="atmosphere:silence_holds",
                           revel="revelation:partial_match")))
    return trajectory(
        "partial_dunne_misread_motive_b",
        "Right suspect, wrong motive. The detective gets Piers via the "
        "marker but reads the motive as his father's legacy rather than "
        "the wider fishing-economy crisis. Partial verdict.",
        "partial_correct", "object_first",
        ["right_suspect_wrong_motive", "father_legacy_misread",
         "partial_chain"],
        t, ramp="partial",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  PARTIAL CORRECT — partial_dunne_wrong_window                      ║
# ║  Right suspect, mechanism understood but tidal window misread       ║
# ╚════════════════════════════════════════════════════════════════════╝
def partial_dunne_wrong_window():
    t = orient_marker_open()
    t.extend(mid_investigation_marker_only())
    t.append(("travel:to_eastern_path",
              return_to_examine("location:eastern_path", "object:path_marker",
                                "atmosphere:wind_rises",
                                "revelation:name_uncovered",
                                "beat:closing_in",
                                cause="cause:recognized_object",
                                tidal="tidal_tell:storm_intensifies")))
    t.append(("object:tide_chart",
              recall_alone("location:eastern_path", "object:tide_chart",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:closing_in",
                           cause="cause:reading_tide_chart",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("motive:fishing_economy",
              recall_alone("location:eastern_path", "object:final_report",
                           "atmosphere:wind_rises",
                           "revelation:motive_emerges", "beat:closing_in",
                           cause="cause:pursued_suspicion",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:path_marker",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:closing_in",
                                stance="stance:defensive",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:confirmation",
                           "beat:closing_in")))
    t.append(("object:resupply_schedule",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:resupply_schedule",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:noticed_inconsistency")))
    t.append(("object:tide_chart",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:tide_chart",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
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
                                "revelation:partial_match",
                                "beat:closing_in",
                                stance="stance:hostile",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("object:path_marker",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:path_marker",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("modifier:processing_facility_loan_due",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:noticed_inconsistency")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:path_marker",
                           atmos="atmosphere:silence_holds",
                           revel="revelation:partial_match")))
    return trajectory(
        "partial_dunne_wrong_window",
        "Right suspect, right motive, but the player never identifies "
        "the forty-minute tidal window cleanly. Mechanism chain holds "
        "loosely; partial verdict.",
        "partial_correct", "object_first",
        ["right_suspect_loose_window", "tidal_window_missed",
         "partial_chain"],
        t, ramp="partial",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  ACCOMPLICE FOUND — accomplice_via_callan                          ║
# ║  Dunne accused + Callan named as the one who warned him             ║
# ╚════════════════════════════════════════════════════════════════════╝
def accomplice_via_callan():
    t = orient_marker_open()
    t.extend(mid_investigation_marker_only())
    t.append(("travel:to_jetty",
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
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("motive:family_on_the_boats",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object_focus:none",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:pursued_suspicion",
                            tidal="tidal_tell:tide_recedes")))
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
    t.append(("travel:to_jetty",
              return_to_question("location:jetty",
                                 "presence:with_mira_callan",
                                 "object:path_marker",
                                 "atmosphere:waves_against_rock",
                                 "revelation:confirmation",
                                 "beat:closing_in",
                                 stance="stance:evasive",
                                 tell="tell:over_explained",
                                 tidal="tidal_tell:tide_floods")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:name_uncovered", "beat:closing_in",
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
                           "revelation:confirmation",
                           "beat:closing_in")))
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
    t.append(("travel:to_jetty",
              return_to_question("location:jetty",
                                 "presence:with_mira_callan",
                                 "object_focus:none",
                                 "atmosphere:waves_against_rock",
                                 "revelation:partial_match",
                                 "beat:closing_in",
                                 stance="stance:hostile",
                                 tell="tell:silent",
                                 cause="cause:pursued_suspicion",
                                 tidal="tidal_tell:tide_floods")))
    t.append(("motive:family_on_the_boats",
              confront_npc("location:jetty",
                           "presence:with_mira_callan",
                           "object_focus:none",
                           "atmosphere:waves_against_rock",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:silent",
                           cause="cause:pursued_suspicion",
                           tidal="tidal_tell:tide_floods")))
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
        "accomplice_via_callan",
        "The detective accuses Piers and names Mira Callan as the one "
        "who told him what the report would mean. Callan's role is "
        "warning, not killing; the moral weight lands on Piers.",
        "accomplice_found", "object_first",
        ["accomplice_chain", "callan_warning", "moral_weight_dunne",
         "mira_named_at_jetty"],
        t, ramp="accomplice",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  ACCOMPLICE FOUND — accomplice_via_webb                            ║
# ║  Dunne accused; Webb's grievance positioning identified as foil    ║
# ╚════════════════════════════════════════════════════════════════════╝
def accomplice_via_webb():
    t = orient_marker_open()
    t.append(("travel:to_dorms",
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
                            "revelation:alibi_holds", "beat:orientation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.extend(mid_investigation_marker_only())
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
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:silence_holds",
                                 "revelation:alibi_holds",
                                 "beat:closing_in",
                                 stance="stance:defensive",
                                 tell="tell:over_explained")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:weather_log",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:closing_in",
                            stance="stance:defensive",
                            tell="tell:over_explained",
                            cause="cause:recognized_object")))
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
                           "revelation:confirmation",
                           "beat:closing_in")))
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
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:silence_holds",
                                 "revelation:alibi_holds",
                                 "beat:closing_in",
                                 stance="stance:cooperative",
                                 tell="tell:softened",
                                 cause="cause:following_witness_lead")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:closing_in",
                            stance="stance:cooperative", tell="tell:softened",
                            cause="cause:recognized_object")))
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
        "accomplice_via_webb",
        "The detective accuses Piers; Webb is identified as the "
        "convenient grievance-foil who let Piers's role go un-noticed "
        "in the first days. Webb is not an accomplice in act, but his "
        "presence served the killer's misdirection.",
        "accomplice_found", "object_first",
        ["accomplice_chain", "webb_as_foil",
         "misdirection_named", "dunne_correctly_accused"],
        t, ramp="accomplice",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  FRAMED — framed_marcus_webb                                       ║
# ╚════════════════════════════════════════════════════════════════════╝
def framed_marcus_webb():
    """Player accuses Webb. Convergence reaches verdict_ready but on the
    wrong suspect — feels confident but the mechanism doesn't land."""
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
    t.append(("motive:methodology_grievance",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:pursued_suspicion")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:weather_log",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:orientation")))
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:defensive",
                                 tell="tell:tightened")))
    t.append(("object:research_notebook",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:research_notebook",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:noticed_inconsistency")))
    t.append(("motive:methodology_grievance",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:pursued_suspicion")))
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
    t.append(("modifier:walk_routine_documented",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:resupply_schedule",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            cause="cause:noticed_inconsistency")))
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:hostile",
                                 tell="tell:tightened")))
    t.append(("object:final_report",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("modifier:methodology_grievance"
              if False else "motive:methodology_grievance",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:silence_holds",
                            "revelation:motive_emerges",
                            "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:pursued_suspicion")))
    t.append(("travel:to_research_lab",
              return_to_examine("location:research_lab",
                                "object:research_notebook",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                cause="cause:revisiting_scene")))
    t.append(("modifier:walk_routine_documented",
              cold_examine("location:research_lab",
                           "object:research_notebook",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:recognized_object")))
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:silence_holds",
                                 "revelation:name_uncovered",
                                 "beat:closing_in",
                                 stance="stance:hostile",
                                 tell="tell:tightened",
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
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:pursued_suspicion")))
    t.append(("object:research_notebook",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:research_notebook",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("modifier:storm_warning_issued",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:weather_log",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:noticed_inconsistency")))
    t.append(("witness:radio_operator",
              cross_to_question("location:research_lab",
                                "presence:with_kestrel_lin",
                                "object:radio_handset",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:closing_in",
                                tidal="tidal_tell:radio_breaks_static")))
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:dawn_approaches",
                                 "revelation:confirmation",
                                 "beat:closing_in",
                                 stance="stance:hostile",
                                 tell="tell:tightened",
                                 cause="cause:pursued_suspicion")))
    t.append(("object:journal_letter",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:journal_letter",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation",
                           "beat:closing_in")))
    t.append(("motive:methodology_grievance",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:journal_letter",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges",
                           "beat:closing_in",
                           cause="cause:pursued_suspicion")))
    t.append(("modifier:storm_warning_issued",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:weather_log",
                           "atmosphere:dawn_approaches",
                           "revelation:partial_match",
                           "beat:closing_in",
                           cause="cause:noticed_inconsistency")))
    t.append(("object:final_report",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:final_report",
                           "atmosphere:dawn_approaches",
                           "revelation:partial_match",
                           "beat:closing_in")))
    t.append(("ACCUSE:suspect:marcus_webb",
              accuse_scene("location:dorms",
                           "presence:with_marcus_webb",
                           obj="object:journal_letter",
                           atmos="atmosphere:dawn_approaches",
                           revel="revelation:confirmation")))
    return trajectory(
        "framed_marcus_webb",
        "The grievance-letter, the absent alibi, the methodology "
        "argument — Webb looks framed by the circumstances. The "
        "detective accuses him. Marker access never closed; the "
        "mechanism layer was missed entirely.",
        "framed_suspect", "wrong_suspect_first",
        ["framed_chain", "webb_circumstantial", "obvious_target_trap",
         "high_apparent_convergence_wrong_suspect"],
        t, ramp="framed",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  FRAMED — framed_mira_callan                                       ║
# ╚════════════════════════════════════════════════════════════════════╝
def framed_mira_callan():
    t = []
    t.append(("witness:boat_skipper",
              S("location:research_lab", "transition:none",
                "cause:following_witness_lead", "presence:alone",
                "stance:none", "action:notices", "object_focus:none",
                "tell:none", "atmosphere:rain_against_glass",
                "revelation:none", "beat:orientation",
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
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:contradiction_surfaces",
                            "beat:orientation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("motive:family_on_the_boats",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object_focus:none",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:pursued_suspicion",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("witness:cook",
              cross_to_question("location:common_room",
                                "presence:with_eira_voss",
                                "object_focus:none",
                                "atmosphere:rain_against_glass",
                                "revelation:partial_match",
                                "beat:orientation")))
    t.append(("travel:to_jetty",
              return_to_question("location:jetty",
                                 "presence:with_mira_callan",
                                 "object:tide_chart",
                                 "atmosphere:waves_against_rock",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:evasive",
                                 tell="tell:hesitated",
                                 tidal="tidal_tell:tide_recedes")))
    t.append(("object:path_marker",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:path_marker",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:examining_evidence",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:tide_recedes")))
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
    t.append(("travel:to_jetty",
              return_to_question("location:jetty",
                                 "presence:with_mira_callan",
                                 "object:path_marker",
                                 "atmosphere:waves_against_rock",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:evasive",
                                 tell="tell:hesitated",
                                 tidal="tidal_tell:tide_recedes")))
    t.append(("motive:family_on_the_boats",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object_focus:none",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:pursued_suspicion",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("object:tide_chart",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:reading_tide_chart",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:tide_chart",
                            "atmosphere:silence_holds",
                            "revelation:name_uncovered", "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:noticed_inconsistency",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("witness:lighthouse_keeper",
              cross_to_question("location:weather_tower",
                                "presence:with_padraic_burne",
                                "object_focus:none",
                                "atmosphere:wind_rises",
                                "revelation:partial_match",
                                "beat:investigation",
                                tidal="tidal_tell:wind_drops")))
    t.append(("travel:to_jetty",
              return_to_question("location:jetty",
                                 "presence:with_mira_callan",
                                 "object:tide_chart",
                                 "atmosphere:waves_against_rock",
                                 "revelation:tidal_window_identified",
                                 "beat:closing_in",
                                 stance="stance:hostile",
                                 tell="tell:tightened",
                                 cause="cause:noticed_inconsistency",
                                 tidal="tidal_tell:tide_recedes")))
    t.append(("object:path_marker",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:path_marker",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:closing_in",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:examining_evidence",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("motive:family_on_the_boats",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object_focus:none",
                            "atmosphere:silence_holds",
                            "revelation:motive_emerges", "beat:closing_in",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:pursued_suspicion",
                            tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              confront_npc("location:jetty",
                           "presence:with_mira_callan",
                           "object:tide_chart",
                           "atmosphere:silence_holds",
                           "revelation:name_uncovered", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:noticed_inconsistency",
                           tidal="tidal_tell:tide_recedes")))
    t.append(("object:tide_chart",
              confront_npc("location:jetty",
                           "presence:with_mira_callan",
                           "object:tide_chart",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened",
                           tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_eastern_path",
              return_to_examine("location:eastern_path", "object:path_marker",
                                "atmosphere:wind_rises",
                                "revelation:partial_match",
                                "beat:closing_in",
                                cause="cause:revisiting_scene",
                                tidal="tidal_tell:tide_floods")))
    t.append(("object:path_marker",
              recall_alone("location:eastern_path", "object:path_marker",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:closing_in",
                           tidal="tidal_tell:tide_floods")))
    t.append(("travel:to_jetty",
              return_to_question("location:jetty",
                                 "presence:with_mira_callan",
                                 "object:path_marker",
                                 "atmosphere:dawn_approaches",
                                 "revelation:confirmation",
                                 "beat:closing_in",
                                 stance="stance:hostile",
                                 tell="tell:tightened",
                                 cause="cause:pursued_suspicion",
                                 tidal="tidal_tell:tide_recedes")))
    t.append(("modifier:tide_data_annotated",
              confront_npc("location:jetty",
                           "presence:with_mira_callan",
                           "object:tide_chart",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:noticed_inconsistency",
                           tidal="tidal_tell:tide_recedes")))
    t.append(("motive:family_on_the_boats",
              confront_npc("location:jetty",
                           "presence:with_mira_callan",
                           "object_focus:none",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:pursued_suspicion",
                           tidal="tidal_tell:tide_recedes")))
    t.append(("object:tide_chart",
              confront_npc("location:jetty",
                           "presence:with_mira_callan",
                           "object:tide_chart",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation", "beat:closing_in",
                           tell="tell:tightened",
                           tidal="tidal_tell:tide_recedes")))
    t.append(("ACCUSE:suspect:mira_callan",
              accuse_scene("location:jetty",
                           "presence:with_mira_callan",
                           obj="object:tide_chart",
                           atmos="atmosphere:dawn_approaches",
                           revel="revelation:confirmation")))
    return trajectory(
        "framed_mira_callan",
        "The skipper's evasion, the annotated tide chart, the family "
        "on the boats — Callan looks framed by the circumstances. The "
        "detective accuses her. The marker is never sourced to her "
        "hand; the mechanism layer is missed.",
        "framed_suspect", "witness_first",
        ["framed_chain", "callan_circumstantial",
         "tide_chart_misread", "high_apparent_convergence_wrong_suspect"],
        t, ramp="framed",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  LATE REVELATION — late_revelation_after_webb                      ║
# ║  Player pursues Webb deep into mid-game, then surge to Piers       ║
# ╚════════════════════════════════════════════════════════════════════╝
def late_revelation_after_webb():
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
    t.append(("motive:methodology_grievance",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:pursued_suspicion")))
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
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:silence_holds",
                                 "revelation:alibi_holds",
                                 "beat:orientation",
                                 stance="stance:defensive",
                                 tell="tell:over_explained")))
    t.append(("object:research_notebook",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:research_notebook",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("travel:to_research_lab",
              return_to_examine("location:research_lab",
                                "object:research_notebook",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                cause="cause:revisiting_scene")))
    t.append(("object:final_report",
              cold_examine("location:research_lab", "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:examining_evidence")))
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:silence_holds",
                                 "revelation:dead_end",
                                 "beat:investigation",
                                 stance="stance:cooperative",
                                 tell="tell:softened")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:weather_log",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:cooperative", tell="tell:softened",
                            cause="cause:recognized_object")))
    t.append(("witness:radio_operator",
              cross_to_question("location:research_lab",
                                "presence:with_kestrel_lin",
                                "object:radio_handset",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation",
                                tidal="tidal_tell:radio_breaks_static")))
    # Late surge starts here (around turn 13)
    t.append(("modifier:radio_log_blank",
              stay_question("location:research_lab",
                            "presence:with_kestrel_lin",
                            "object:radio_handset",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            cause="cause:noticed_inconsistency")))
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
                           "revelation:confirmation",
                           "beat:closing_in")))
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
        "late_revelation_after_webb",
        "The detective burns the first eleven turns on Webb. His alibi "
        "softens, the mechanism shifts visibly toward logistics around "
        "turn 13, and the closing chain lands on Piers via the marker. "
        "Late surge from confusion to verdict.",
        "late_revelation", "wrong_suspect_first",
        ["late_revelation", "webb_first_then_redirect",
         "slow_start_fast_close"],
        t, ramp="late",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  MOTIVE-ONLY CONFESSION — motive_only_via_fishing_economy          ║
# ║  Player anchors on the motive layer first, then closes on suspect  ║
# ╚════════════════════════════════════════════════════════════════════╝
def motive_only_via_fishing_economy():
    t = []
    t.append(("object:final_report",
              cold_examine("location:research_lab", "object:final_report",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none")))
    t.append(("motive:fishing_economy",
              cold_examine("location:research_lab", "object:final_report",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           cause="cause:pursued_suspicion")))
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
    t.append(("motive:fishing_economy",
              stay_question("location:common_room",
                            "presence:with_eira_voss",
                            "object:final_report",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            cause="cause:pursued_suspicion")))
    t.append(("travel:to_jetty",
              cross_to_question("location:jetty",
                                "presence:with_mira_callan",
                                "object_focus:none",
                                "atmosphere:waves_against_rock",
                                "revelation:partial_match",
                                "beat:orientation",
                                stance="stance:evasive",
                                tell="tell:hesitated",
                                tidal="tidal_tell:wind_drops")))
    t.append(("motive:family_on_the_boats",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object_focus:none",
                            "atmosphere:waves_against_rock",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:pursued_suspicion",
                            tidal="tidal_tell:wind_drops")))
    t.append(("motive:fishing_economy",
              stay_question("location:jetty",
                            "presence:with_mira_callan",
                            "object:final_report",
                            "atmosphere:waves_against_rock",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:evasive", tell="tell:hesitated",
                            cause="cause:pursued_suspicion",
                            tidal="tidal_tell:wind_drops")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object_focus:none",
                                "atmosphere:silence_holds",
                                "revelation:partial_match",
                                "beat:investigation")))
    t.append(("motive:fishing_economy",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:pursued_suspicion")))
    t.append(("modifier:processing_facility_loan_due",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("motive:father_legacy",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:pursued_suspicion")))
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
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:tide_chart",
                               "atmosphere:wind_rises",
                               "revelation:tidal_window_identified",
                               "beat:investigation",
                               cause="cause:reading_tide_chart",
                               tidal="tidal_tell:tide_recedes")))
    t.append(("travel:to_common_room",
              return_to_question("location:common_room",
                                 "presence:with_piers_dunne",
                                 "object:resupply_schedule",
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
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("motive:fishing_economy",
              stay_question("location:common_room",
                            "presence:with_piers_dunne",
                            "object:final_report",
                            "atmosphere:silence_holds",
                            "revelation:motive_emerges", "beat:closing_in",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:pursued_suspicion")))
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
                           "revelation:confirmation",
                           "beat:closing_in")))
    t.append(("motive:fishing_economy",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
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
    t.append(("object:resupply_schedule",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:resupply_schedule",
                           "atmosphere:silence_holds",
                           "revelation:name_uncovered", "beat:closing_in",
                           tell="tell:paled")))
    t.append(("travel:to_common_room",
              cross_to_question("location:common_room",
                                "presence:with_piers_dunne",
                                "object:final_report",
                                "atmosphere:dawn_approaches",
                                "revelation:motive_emerges",
                                "beat:closing_in",
                                stance="stance:hostile",
                                tell="tell:tightened",
                                cause="cause:pursued_suspicion")))
    t.append(("motive:fishing_economy",
              confront_npc("location:common_room",
                           "presence:with_piers_dunne",
                           "object:final_report",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges",
                           "beat:closing_in",
                           tell="tell:silent",
                           cause="cause:pursued_suspicion")))
    t.append(("ACCUSE:suspect:piers_dunne",
              accuse_scene("location:common_room",
                           "presence:with_piers_dunne",
                           obj="object:final_report",
                           atmos="atmosphere:dawn_approaches",
                           revel="revelation:motive_emerges")))
    return trajectory(
        "motive_only_via_fishing_economy",
        "Motive-anchored chain. The detective opens with the fishing "
        "economy weight — the loan papers, the processing facility, "
        "the family on the boats — and lets the mechanism close last. "
        "Piers confesses under motive pressure.",
        "motive_only_confession", "object_first",
        ["motive_first_chain", "fishing_economy_anchored",
         "loan_papers_first", "confession_under_motive"],
        t, ramp="motive_only",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  RED HERRING TRAP — red_herring_trap_storm_alibi                   ║
# ║  Player builds case on Webb's storm alibi, accuses wrong            ║
# ╚════════════════════════════════════════════════════════════════════╝
def red_herring_trap_storm_alibi():
    t = []
    t.append(("object:weather_log",
              cold_examine("location:research_lab", "object:weather_log",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           trans="transition:none",
                           cause="cause:reading_tide_chart")))
    t.append(("modifier:storm_warning_issued",
              cold_examine("location:research_lab", "object:weather_log",
                           "atmosphere:rain_against_glass",
                           "revelation:partial_match", "beat:orientation",
                           cause="cause:recognized_object")))
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
    t.append(("modifier:storm_warning_issued",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:weather_log",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:recognized_object")))
    t.append(("motive:methodology_grievance",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:rain_against_glass",
                            "revelation:partial_match", "beat:orientation",
                            stance="stance:defensive", tell="tell:tightened",
                            cause="cause:pursued_suspicion")))
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
                            "revelation:partial_match", "beat:investigation",
                            cause="cause:recognized_object")))
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:defensive",
                                 tell="tell:over_explained")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:weather_log",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:defensive",
                            tell="tell:over_explained",
                            cause="cause:noticed_inconsistency")))
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
                            "revelation:partial_match", "beat:investigation",
                            cause="cause:recognized_object")))
    t.append(("travel:to_weather_tower",
              cross_to_examine("location:weather_tower", "object:weather_log",
                               "atmosphere:wind_rises",
                               "revelation:partial_match",
                               "beat:investigation",
                               cause="cause:reading_tide_chart",
                               tidal="tidal_tell:storm_intensifies")))
    t.append(("modifier:storm_warning_issued",
              cold_examine("location:weather_tower", "object:weather_log",
                           "atmosphere:wind_rises",
                           "revelation:partial_match", "beat:investigation",
                           cause="cause:recognized_object",
                           tidal="tidal_tell:storm_intensifies")))
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:silence_holds",
                                 "revelation:partial_match",
                                 "beat:investigation",
                                 stance="stance:hostile",
                                 tell="tell:tightened")))
    t.append(("object:journal_letter",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:examining_evidence")))
    t.append(("motive:methodology_grievance",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:journal_letter",
                            "atmosphere:silence_holds",
                            "revelation:contradiction_surfaces",
                            "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:pursued_suspicion")))
    t.append(("modifier:storm_warning_issued",
              stay_question("location:dorms",
                            "presence:with_marcus_webb",
                            "object:weather_log",
                            "atmosphere:silence_holds",
                            "revelation:partial_match", "beat:investigation",
                            stance="stance:hostile", tell="tell:tightened",
                            cause="cause:recognized_object")))
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
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:silence_holds",
                                 "revelation:name_uncovered",
                                 "beat:closing_in",
                                 stance="stance:hostile",
                                 tell="tell:tightened")))
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
                           "atmosphere:silence_holds",
                           "revelation:motive_emerges", "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:pursued_suspicion")))
    t.append(("modifier:storm_warning_issued",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:weather_log",
                           "atmosphere:silence_holds",
                           "revelation:confirmation",
                           "beat:closing_in",
                           tell="tell:tightened",
                           cause="cause:noticed_inconsistency")))
    t.append(("object:final_report",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:final_report",
                           "atmosphere:silence_holds",
                           "revelation:partial_match", "beat:closing_in",
                           tell="tell:tightened")))
    t.append(("witness:radio_operator",
              cross_to_question("location:research_lab",
                                "presence:with_kestrel_lin",
                                "object:radio_handset",
                                "atmosphere:silence_holds",
                                "revelation:confirmation",
                                "beat:closing_in",
                                tidal="tidal_tell:radio_breaks_static")))
    t.append(("travel:to_dorms",
              return_to_question("location:dorms",
                                 "presence:with_marcus_webb",
                                 "object:journal_letter",
                                 "atmosphere:dawn_approaches",
                                 "revelation:confirmation",
                                 "beat:closing_in",
                                 stance="stance:hostile",
                                 tell="tell:tightened",
                                 cause="cause:pursued_suspicion")))
    t.append(("object:journal_letter",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:journal_letter",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation",
                           "beat:closing_in")))
    t.append(("motive:methodology_grievance",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:journal_letter",
                           "atmosphere:dawn_approaches",
                           "revelation:motive_emerges",
                           "beat:closing_in",
                           cause="cause:pursued_suspicion")))
    t.append(("modifier:storm_warning_issued",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:weather_log",
                           "atmosphere:dawn_approaches",
                           "revelation:confirmation",
                           "beat:closing_in",
                           cause="cause:noticed_inconsistency")))
    t.append(("object:research_notebook",
              confront_npc("location:dorms",
                           "presence:with_marcus_webb",
                           "object:research_notebook",
                           "atmosphere:dawn_approaches",
                           "revelation:partial_match",
                           "beat:closing_in")))
    t.append(("ACCUSE:suspect:marcus_webb",
              accuse_scene("location:dorms",
                           "presence:with_marcus_webb",
                           obj="object:journal_letter",
                           atmos="atmosphere:dawn_approaches",
                           revel="revelation:confirmation")))
    return trajectory(
        "red_herring_trap_storm_alibi",
        "Convergence climbs steadily on Webb — the storm warning, the "
        "absent alibi, the grievance letter all read like a closing "
        "chain. The detective accuses with confidence. Mechanism layer "
        "was never anchored; the trap held.",
        "red_herring_trap", "wrong_suspect_first",
        ["red_herring_trap", "webb_storm_alibi", "high_apparent_convergence",
         "wrong_accusation_with_confidence"],
        t, ramp="red_herring",
        accused="suspect:marcus_webb",
    )


# ╔════════════════════════════════════════════════════════════════════╗
# ║  MAIN WRITER                                                       ║
# ╚════════════════════════════════════════════════════════════════════╝
def main():
    builders = [
        # Correct accusations of piers_dunne (6)
        dunne_via_path_marker,
        dunne_via_tidal_window,
        dunne_via_radio_log,
        dunne_via_callan_corroboration,
        dunne_via_webb_alibi_collapse,
        dunne_via_research_notebook,
        # Wrong accusations (6)
        wrong_marcus_webb,
        wrong_mira_callan,
        wrong_oren_halloway,
        wrong_tovi_ansgar,
        wrong_niall_brackett,
        wrong_kestrel_lin,
        # Cold trails (3)
        cold_trail_circular,
        cold_trail_storm_loop,
        cold_trail_radio_silence,
        # Partial correct (3)
        partial_dunne_misread_motive_a,
        partial_dunne_misread_motive_b,
        partial_dunne_wrong_window,
        # Accomplice found (2)
        accomplice_via_callan,
        accomplice_via_webb,
        # Framed suspect (2)
        framed_marcus_webb,
        framed_mira_callan,
        # Late revelation (1)
        late_revelation_after_webb,
        # Motive-only confession (1)
        motive_only_via_fishing_economy,
        # Red herring trap (1)
        red_herring_trap_storm_alibi,
    ]
    assert len(builders) == 25, f"expected 25 builders, got {len(builders)}"

    out_dir = HERE
    manifest_entries = []
    for build in builders:
        traj = build()
        traj_id = traj["trajectory_id"]
        path = out_dir / f"{traj_id}.json"
        with open(path, "w") as f:
            json.dump(traj, f, indent=2)
        manifest_entries.append({
            "id": traj_id,
            "outcome": traj["outcome"],
            "length": len(traj["turns"]),
            "starting_hypothesis": traj["starting_hypothesis"],
            "tags": traj["tags"],
        })
        print(f"  wrote {traj_id}  ({len(traj['turns'])} turns)")

    manifest = {
        "schema_version": 1,
        "case_id": "tidal_interval",
        "_comment": ("Index of hand-authored trajectories for The Tidal "
                     "Interval. Wave 1 of 2 (target 50 total). The trainer "
                     "loads the manifest first, then reads each listed "
                     "trajectory file."),
        "trajectories": manifest_entries,
    }
    with open(out_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nWrote manifest.json with {len(manifest_entries)} entries")


if __name__ == "__main__":
    main()
