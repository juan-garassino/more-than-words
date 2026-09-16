# Living Tales — Visual Asset Catalogue

This document inventories the diffusion-generated images we want to commission
to push the pygame UI from "atmospheric" to "beautiful". Each asset is scoped
with an exact filename, size, count, style direction, and a starter diffusion
prompt you can adapt for SDXL/Flux/Midjourney.

The ground rule is the same as the engine's: the **picture is sacred**. The
backdrop image is never overlaid. All UI ornaments must compose around it,
not on it. Every asset listed here is meant to live in the chrome of the
window — the title strip, the location subtitle, the narration panel, the
evidence cards, the briefing/ending screens — never on the active scene.

Existing assets are listed in the "Already have" sections so you don't
re-commission them.

Folder convention:

```
art/
├── <case_id>/                      # per-case scene art (existing)
│   ├── direct_pixel_art_v1/
│   │   ├── pixel_320x320/          # primary scene backdrops (current default)
│   │   ├── pixel_240x240/          # smaller-screen alternative
│   │   └── masters_square_320/     # painterly hi-res sources for cinematics
│   └── scene_backdrops_v2/
└── ui/                             # NEW — shared UI ornaments (this doc's scope)
    ├── frames/
    ├── ornaments/
    ├── icons/
    ├── textures/
    ├── portraits/
    └── cinematics/
```

## Priorities

- **P0** — Massive aesthetic lift, small asset count. Ship first.
- **P1** — Per-case visual identity (portraits, missing scenes).
- **P2** — Atmospheric cinematics (briefings, endings, transitions).
- **P3** — Animated effects (particle sprites, scanlines, rain).

---

## P0 — UI ornaments (ship first)

These transform the chrome immediately. All transparent PNG, pixel art style,
limited palette: warm sepia + brass + ink-blue + cream.

### P0.1 — Parchment texture

| | |
|---|---|
| Path | `art/ui/textures/parchment_dark_tile.png` |
| Size | 256×256, **tileable** (seamless edges) |
| Count | 1 |
| Use | Background fill for narration panel and evidence cards. |

Style: dark warm parchment, subtle grain and water-stains, tobacco-stained
edges. Must read as "old paper" but stay dark enough that cream text pops.
Avoid heavy text/sigils — it tiles, so any feature repeats.

> **Prompt seed:** *"seamless tileable texture, aged parchment, deep tobacco
> brown, faint ink stains, subtle paper grain, gas-lamp lit, no text, no
> drawings, pixel art, 16-bit era, 256x256, edges seamless"*

### P0.2 — Class icons

| | |
|---|---|
| Path | `art/ui/icons/class_<NAME>.png` |
| Size | 32×32, transparent background |
| Count | 11 (one per token class) |
| Filenames | `class_suspect.png`, `class_witness.png`, `class_object.png`, `class_motive.png`, `class_event.png`, `class_location.png`, `class_action.png`, `class_emotion.png`, `class_modifier.png`, `class_time.png`, `class_accomplice.png` |

Each is a single-color (cream `#E8DCC0` over transparent) ink illustration
in the style of a Victorian field-notebook glyph. They replace the current
Unicode symbols on evidence cards.

Suggested glyphs:
- **suspect** — silhouetted bust in profile
- **witness** — single eye, deco frame
- **object** — magnifying glass over a tag
- **motive** — heart pierced by a coin
- **event** — pocket-watch face
- **location** — compass rose / signpost
- **action** — running boot or hand
- **emotion** — theatrical mask
- **modifier** — small wax seal
- **time** — clock pendulum
- **accomplice** — two silhouettes overlapping

> **Prompt seed:** *"32x32 pixel art icon, single cream color on transparent,
> Victorian engraving style, [GLYPH], minimalist line work, period-appropriate,
> clean silhouette, no shading, sharp 1-px line work"*

### P0.3 — Decorative dividers

| | |
|---|---|
| Path | `art/ui/ornaments/divider_<NAME>.png` |
| Size | 480×16, transparent background |
| Count | 3 (`divider_thin.png`, `divider_fleuron.png`, `divider_double.png`) |

Horizontal rule replacements for the location subtitle bar and panel breaks.
`fleuron` has a centered ornamental flourish (Art Nouveau leaf or wax seal),
the others are stylized rules. Brass/gold tone (`#B08A3F`).

> **Prompt seed:** *"horizontal divider ornament, brass color on transparent
> background, Art Nouveau, single fleuron centered, 480x16 pixel art, 16-bit
> era, fine engraving, period decorative element, no text"*

### P0.4 — Card corner ornaments

| | |
|---|---|
| Path | `art/ui/ornaments/corner_tl.png` (+ tr, bl, br) |
| Size | 16×16 each, transparent |
| Count | 4 (one per corner — they mirror) |

Replace the current 2×2 gold pixel ticks at evidence-card corners with
proper ornamental brackets — small Art Nouveau flourishes that frame the card.
Brass `#B08A3F`.

> **Prompt seed:** *"16x16 pixel art corner ornament, brass on transparent,
> Art Nouveau frame bracket, single corner only, top-left orientation,
> minimalist Victorian filigree, sharp pixel edges"*

### P0.5 — Title strip emblem

| | |
|---|---|
| Path | `art/ui/ornaments/emblem.png` |
| Size | 24×24, transparent |
| Count | 1 |

A small wax-seal / monogram-style emblem to sit beside the case title in the
top strip. Reads as the imprint of the detective agency. Deep crimson over
brass.

> **Prompt seed:** *"24x24 pixel art wax seal, deep red wax with brass
> impression of a magnifying glass over an eye, Victorian detective agency
> sigil, transparent background, single object centered, no shadow"*

### P0.6 — Vignette overlay

| | |
|---|---|
| Path | `art/ui/textures/vignette.png` |
| Size | 480×800, partially transparent |
| Count | 1 |

A full-window overlay with a soft black vignette in the corners and slight
chromatic aberration that gives the entire window a "lantern-lit" feel.
Centre is fully transparent, corners fade to black at ~30% alpha.

> **Prompt seed:** *"480x800 vignette overlay, transparent center fading to
> 30% black at corners, slight blue-cyan chromatic aberration at edges, gas
> lamp atmosphere, pure overlay layer, no detail in center"*

### P0.7 — Title-screen background

| | |
|---|---|
| Path | `art/ui/cinematics/title_screen.png` |
| Size | 480×800 |
| Count | 1 |

The image behind the case-select menu. A painterly Victorian detective's
desk: pocket watch, magnifying glass, cipher pages, tobacco pipe, brass
oil lamp. Warm, dim, filling the entire portrait frame. Used as backdrop
when no case is loaded.

> **Prompt seed:** *"painterly Victorian detective's desk overhead view,
> pocket watch, magnifying glass over cipher page, tobacco pipe, brass oil
> lamp, scattered evidence photographs, leather-bound notebook, deep amber
> chiaroscuro lighting, painterly oil-paint look, 480x800 portrait, no text"*

### P0.8 — Case-select thumbnails

| | |
|---|---|
| Path | `art/ui/thumbnails/<case_id>.png` |
| Size | 64×64 |
| Count | 20 (one per case) |

Small icon for each case in the case-select list. A miniature crest or
emblem keyed to the case — e.g. *amber_cipher* = stopped clock, *attended_hour*
= a heart-rate trace, *orchard_at_dusk* = boot prints. Distinguishable at
a glance even when the model is not yet trained (then rendered desaturated).

> **Prompt seed:** *"64x64 pixel art emblem, [CASE-SPECIFIC OBJECT], on
> transparent background, brass + cream colors, single iconic object centered,
> period engraving style, no text, no border"*

---

## P1 — Per-case identity

### P1.1 — Suspect & witness portraits

| | |
|---|---|
| Path | `art/ui/portraits/<case_id>/<role>_<name>.png` |
| Size | 96×96 |
| Count | ~12 per case (7 suspects + 5 witnesses for amber_cipher) |

Square pixel-art portraits framed like a tintype photograph. Used as a small
overlay beside the clue panel when the model emits a SUSPECT or WITNESS
token. Should match the case's pixel-art style (existing scene backdrops
in `art/<case_id>/direct_pixel_art_v1/`).

For amber_cipher, the IDs are:
- suspects: `stationmaster, railway_clerk, estranged_daughter, renard_voss,
  night_porter, platform_guard, travelling_broker`
- witnesses: `ticket_clerk, porter, signalman, carriage_cleaner,
  telegraph_operator`

> **Prompt seed:** *"96x96 pixel art portrait, [CHARACTER DESCRIPTION FROM
> CASE BRIEFING], tintype photograph framing, sepia tones, period costume
> 1890s railway station, dim gas-lamp lighting, 16-bit era, head and
> shoulders, looking slightly off camera, no text"*

The 8 generic UUID-named PNGs already in `living_tales_sprites/final_set/`
need a manual mapping to suspect/witness IDs before they can be used. Until
that's done, treat this as net-new commissions per case.

### P1.2 — Missing scene backdrops

13 cases currently ship with only **1 backdrop** — usually a placeholder/concept
piece. Each needs N backdrops where N = number of LOCATION tokens in that case.

| Case | Locations needed | Existing backdrops |
|---|---|---|
| amber_silence | TBD | 1 (concept only) |
| burning_glass | TBD | 1 |
| covenant_garden | TBD | 1 |
| dead_calm | TBD | 1 |
| endgame | TBD | 1 |
| glass_cartographer | TBD | 1 |
| instrument_landing | TBD | 1 |
| iron_cartridge | TBD | 1 |
| monsoon_ledger | TBD | 1 |
| mountain_exchange | TBD | 1 |
| observatory_clock | TBD | 1 |
| signal_fire | TBD | 1 |
| thirteenth_tide | TBD | 1 |

For each missing case, run `living_tales/trainer/cases/<case_id>/spec.json`
to extract the LOCATION tokens, then commission one 320×320 PNG per token at
`art/<case_id>/direct_pixel_art_v1/pixel_320x320/<case_id>_<location_id>_pixel_320x320_v01.png`.

Style must match the case's existing concept piece (palette, era, mood).

### P1.3 — amber_cipher — `signal_box`

The only LOCATION in a "complete" case that has no art (we currently proxy
to `station_office_doorway`). One 320×320 PNG named
`amber_cipher_signal_box_pixel_320x320_v01.png` would close the gap.

> **Prompt seed:** *"signal box interior at night, brass levers, oil lamp,
> rain-streaked window, Victorian railway, pixel art 320x320 16-bit era,
> matches Living Tales amber_cipher palette: deep blue night, amber lamps,
> wet cobblestones outside"*

---

## P2 — Cinematics

### P2.1 — Briefing card

| | |
|---|---|
| Path | `art/ui/cinematics/briefing_<case_id>.png` |
| Size | 480×480 |
| Count | 20 |

A wide painterly establishing shot for the briefing screen — same scene as
the opening location, but rendered painterly (oil-paint look) rather than
pixel-art. Sets a cinematic tone before the pixel-art game proper starts.

For amber_cipher this would be Thornfield Crossing rendered as an oil
painting at twilight, foggy, atmospheric.

> **Prompt seed:** *"painterly oil painting, [CASE'S OPENING LOCATION],
> dramatic chiaroscuro, narrative cinematic, 480x480, atmospheric,
> period-appropriate, no text overlay"*

### P2.2 — Verdict cards

| | |
|---|---|
| Path | `art/ui/cinematics/verdict_<TYPE>.png` |
| Size | 480×480 |
| Count | 5 (one per ending type) |

Painterly cards for each ending category, used as the ending-screen
backdrop:
- `verdict_all_strong.png` — courtroom, gavel, light streaming through
- `verdict_lucky_guess.png` — accusation, half-shadowed face, "is it him?"
- `verdict_wrong_accusation.png` — empty prison cell, key on floor
- `verdict_cold_case.png` — fog, abandoned street, file folder closing
- `verdict_partial.png` — newspaper clipping, words half-covered

These replace the per-case ending backdrop currently keyed by `_ending` in
`scene_map.json`.

> **Prompt seed:** *"[VERDICT THEME], painterly Victorian noir, dramatic
> lighting, no text, 480x480, oil painting, atmospheric"*

### P2.3 — Accusation screen

| | |
|---|---|
| Path | `art/ui/cinematics/accusation_board.png` |
| Size | 480×640 |
| Count | 1 |

A "detective's evidence board" backdrop — corkboard with photos, red string,
pinned notes — used during the accusation modal. Suspects' portraits will
be overlaid programmatically.

> **Prompt seed:** *"detective's evidence board, corkboard with red string
> connecting photographs, pinned notes, magnifying glass, dim gas lamp,
> Victorian noir, painterly, 480x640 portrait, no text on notes"*

---

## P3 — Atmospheric effects (lowest priority)

### P3.1 — Particle sprite sheets

| | |
|---|---|
| Path | `art/ui/effects/<TYPE>_sheet.png` |
| Size | 256×256, 4×4 grid of 64×64 frames |
| Count | 4 (`rain`, `fog`, `dust_motes`, `embers`) |

For optional weather/atmosphere overlays drawn on top of the backdrop
(NOT on the picture — we'd composite them as faint translucent layers
inside the backdrop area only, never over text).

### P3.2 — CRT scanline overlay

| | |
|---|---|
| Path | `art/ui/textures/scanlines.png` |
| Size | 480×480, alpha at ~10% |
| Count | 1 |

Subtle horizontal scanlines to give the backdrop a "memory recalled" feel.
Toggle via a `--crt` flag.

---

## Implementation hooks

When a P0 asset lands, the corresponding hook in `pygame_play.py` is:

| Asset | Wire-up location |
|---|---|
| Parchment texture | `Renderer._draw_narration` — replace `pygame.draw.rect(... PARCHMENT ...)` with `screen.blit(self._parchment_tile, …)` looped to fill `NARRATION_RECT`. Same in `_draw_hand` for card backgrounds. |
| Class icons | `Renderer._draw_hand` — replace the `CLASS` text with `screen.blit(self._class_icons[cls], …)`. |
| Dividers | `Renderer._draw_location_bar` — replace the two `pygame.draw.line` calls with `screen.blit(self._divider, …)`. |
| Card corners | `Renderer._draw_hand` — replace the 4 `pygame.draw.rect` corner ticks with `screen.blit(self._corner_tl, …)` etc. |
| Vignette | `Renderer._draw_frame` — final blit after everything else. |
| Title-screen bg | New `case_select_screen()` — `screen.blit(self._title_bg, (0, 0))` before drawing the menu. |
| Thumbnails | `case_select_screen()` — small thumbnail next to each case row. |
| Suspect portraits | `Renderer._draw_narration` — when last clue is SUSPECT/WITNESS, blit a 96×96 portrait in the panel's right gutter. |

Each P0 asset should be loaded once in `Renderer.__init__` with graceful
fallback to the current programmatic rendering when the file is absent —
that way the catalogue can be filled incrementally without breaking the
build.

## Generation logistics

- **Resolution:** generate at 4× the target, then nearest-neighbor downscale
  to keep crisp pixel edges. SDXL/Flux at native pixel-art resolutions
  produces softer results than scale-down.
- **Palette lock:** export the project palette (the `INK / GOLD / BRASS /
  CREAM / PARCHMENT / SEPIA` constants in `pygame_play.py:54-78`) as a
  16-color palette and run an indexed-color pass after generation. This
  enforces visual consistency across cases.
- **Naming:** stick to `lowercase_with_underscores.png`. Generate v01, v02,
  v03 candidates per asset; pick the best, drop into the canonical name.
- **License:** if using a hosted diffusion service, capture each prompt and
  seed in `art/ui/<asset>/PROVENANCE.txt` so we can re-roll deterministically.

---

## Per-case prompt sheets (lt-art skill output)

These are full diffusion-ready prompt sheets, one per case, generated by the
`lt-art` skill. Each sheet covers locations + portraits + briefing + verdicts +
UI ornaments grounded in the case's palette + motif. Pasteable into SDXL/Flux/
Midjourney without further authoring.

| Case | Prompt sheet | Status |
|---|---|---|
| venetian_mirror | `art/venetian_mirror/art_prompts.md` | authored 2026-06-05 (35 prompts: 8 backdrops + 12 portraits + 1 briefing + 10 verdicts + 3 UI; wrong-suspect template fans to 5 instances) |

### venetian_mirror — asset rows

| ID | Category | Filename target | Dimensions | Priority |
|---|---|---|---|---|
| bd_palazzo_contarini | location_backdrop | `art/venetian_mirror/direct_pixel_art_v1/pixel_320x320/venetian_mirror_palazzo_contarini_pixel_320x320_v01.png` | 320x320 | P1 |
| bd_main_balcony | location_backdrop | `.../venetian_mirror_main_balcony_pixel_320x320_v01.png` | 320x320 | P1 |
| bd_mirror_gallery | location_backdrop | `.../venetian_mirror_mirror_gallery_pixel_320x320_v01.png` | 320x320 | P1 |
| bd_canal_entrance | location_backdrop | `.../venetian_mirror_canal_entrance_pixel_320x320_v01.png` | 320x320 | P1 |
| bd_studio_room | location_backdrop | `.../venetian_mirror_studio_room_pixel_320x320_v01.png` | 320x320 | P1 |
| bd_servants_stair | location_backdrop | `.../venetian_mirror_servants_stair_pixel_320x320_v01.png` | 320x320 | P1 |
| bd_courtyard | location_backdrop | `.../venetian_mirror_courtyard_pixel_320x320_v01.png` | 320x320 | P1 |
| bd_private_salon | location_backdrop | `.../venetian_mirror_private_salon_pixel_320x320_v01.png` | 320x320 | P1 |
| pt_morvaine | suspect_portrait | `art/ui/portraits/venetian_mirror/suspect_morvaine.png` | 96x96 + 192x192 | P1 |
| pt_bassi | suspect_portrait | `art/ui/portraits/venetian_mirror/suspect_bassi.png` | 96x96 + 192x192 | P1 |
| pt_winter | suspect_portrait | `art/ui/portraits/venetian_mirror/suspect_winter.png` | 96x96 + 192x192 | P1 |
| pt_rizzoli | suspect_portrait | `art/ui/portraits/venetian_mirror/suspect_rizzoli.png` | 96x96 + 192x192 | P1 |
| pt_dandolo | suspect_portrait | `art/ui/portraits/venetian_mirror/suspect_dandolo.png` | 96x96 + 192x192 | P1 |
| pt_pelosi | suspect_portrait | `art/ui/portraits/venetian_mirror/suspect_pelosi.png` | 96x96 + 192x192 | P1 |
| pt_bruno | suspect_portrait | `art/ui/portraits/venetian_mirror/suspect_bruno.png` | 96x96 + 192x192 | P1 |
| pt_gondolier | witness_portrait | `art/ui/portraits/venetian_mirror/witness_gondolier.png` | 96x96 + 192x192 | P1 |
| pt_maid | witness_portrait | `art/ui/portraits/venetian_mirror/witness_palazzo_maid.png` | 96x96 + 192x192 | P1 |
| pt_nightguard | witness_portrait | `art/ui/portraits/venetian_mirror/witness_night_guard.png` | 96x96 + 192x192 | P1 |
| pt_artdealer | witness_portrait | `art/ui/portraits/venetian_mirror/witness_art_dealer.png` | 96x96 + 192x192 | P1 |
| pt_canalboatman | witness_portrait | `art/ui/portraits/venetian_mirror/witness_canal_boatman.png` | 96x96 + 192x192 | P1 |
| br_venetian_mirror | briefing_card | `art/ui/cinematics/briefing_venetian_mirror.png` | 480x480 | P2 |
| vc_correct | verdict_card | `art/ui/cinematics/venetian_mirror_verdict_correct.png` | 480x480 | P2 |
| vc_partial_correct | verdict_card | `art/ui/cinematics/venetian_mirror_verdict_partial_correct.png` | 480x480 | P2 |
| vc_accomplice_found | verdict_card | `art/ui/cinematics/venetian_mirror_verdict_accomplice_found.png` | 480x480 | P2 |
| vc_framed_suspect | verdict_card | `art/ui/cinematics/venetian_mirror_verdict_framed_suspect.png` | 480x480 | P2 |
| vc_motive_only_confession | verdict_card | `art/ui/cinematics/venetian_mirror_verdict_motive_only_confession.png` | 480x480 | P2 |
| vc_late_revelation | verdict_card | `art/ui/cinematics/venetian_mirror_verdict_late_revelation.png` | 480x480 | P2 |
| vc_near_miss | verdict_card | `art/ui/cinematics/venetian_mirror_verdict_near_miss.png` | 480x480 | P2 |
| vc_cold_trail | verdict_card | `art/ui/cinematics/venetian_mirror_verdict_cold_trail.png` | 480x480 | P2 |
| vc_red_herring_trap | verdict_card | `art/ui/cinematics/venetian_mirror_verdict_red_herring_trap.png` | 480x480 | P2 |
| vc_wrong_suspect_template | verdict_card (template) | `art/ui/cinematics/venetian_mirror_verdict_wrong_<id>.png` | 480x480 (x5 instances) | P2 |
| ui_mirror_shards | ui_ornament | `art/ui/ornaments/venetian_mirror_mirror_shards.png` | 64x64 | P0 |
| ui_carnival_mask_silhouette | ui_ornament | `art/ui/ornaments/venetian_mirror_carnival_mask_emblem.png` | 32x32 | P0 |
| ui_gold_filigree_divider | ui_ornament | `art/ui/ornaments/venetian_mirror_filigree_divider.png` | 480x16 | P0 |

---

## Per-case prompt sheets — amber_cipher (2026-06-05)

Prompts authored by `lt-art` skill. See `art/amber_cipher/art_prompts.md` for
the full diffusion-ready prompt blocks (style spine, palette, negative prompts,
en/es captions).

| id | category | filename | dimensions | priority | prompt sheet |
|---|---|---|---|---|---|
| bd_thornfield_crossing | backdrop | `art/amber_cipher/direct_pixel_art_v1/pixel_320x320/amber_cipher_thornfield_crossing_pixel_320x320_v01.png` | 320x320 | P1.2 | art/amber_cipher/art_prompts.md#11--bd_thornfield_crossing |
| bd_platform_two | backdrop | `art/amber_cipher/direct_pixel_art_v1/pixel_320x320/amber_cipher_platform_two_pixel_320x320_v01.png` | 320x320 | P1.2 | art/amber_cipher/art_prompts.md#12--bd_platform_two |
| bd_platform_one | backdrop | `art/amber_cipher/direct_pixel_art_v1/pixel_320x320/amber_cipher_platform_one_pixel_320x320_v01.png` | 320x320 | P1.2 | art/amber_cipher/art_prompts.md#13--bd_platform_one |
| bd_station_office | backdrop | `art/amber_cipher/direct_pixel_art_v1/pixel_320x320/amber_cipher_station_office_pixel_320x320_v01.png` | 320x320 | P1.2 | art/amber_cipher/art_prompts.md#14--bd_station_office |
| bd_signal_box | backdrop | `art/amber_cipher/direct_pixel_art_v1/pixel_320x320/amber_cipher_signal_box_pixel_320x320_v01.png` | 320x320 | P1.3 | art/amber_cipher/art_prompts.md#15--bd_signal_box |
| bd_waiting_room | backdrop | `art/amber_cipher/direct_pixel_art_v1/pixel_320x320/amber_cipher_waiting_room_pixel_320x320_v01.png` | 320x320 | P1.2 | art/amber_cipher/art_prompts.md#16--bd_waiting_room |
| bd_goods_shed | backdrop | `art/amber_cipher/direct_pixel_art_v1/pixel_320x320/amber_cipher_goods_shed_pixel_320x320_v01.png` | 320x320 | P1.2 | art/amber_cipher/art_prompts.md#17--bd_goods_shed |
| bd_carriage_siding | backdrop | `art/amber_cipher/direct_pixel_art_v1/pixel_320x320/amber_cipher_carriage_siding_pixel_320x320_v01.png` | 320x320 | P1.2 | art/amber_cipher/art_prompts.md#18--bd_carriage_siding |
| pt_stationmaster | portrait | `art/ui/portraits/amber_cipher/suspect_stationmaster.png` | 96x96 (+192x192) | P1.1 | art/amber_cipher/art_prompts.md#21--pt_stationmaster |
| pt_railway_clerk | portrait | `art/ui/portraits/amber_cipher/suspect_railway_clerk.png` | 96x96 (+192x192) | P1.1 | art/amber_cipher/art_prompts.md#22--pt_railway_clerk |
| pt_estranged_daughter | portrait | `art/ui/portraits/amber_cipher/suspect_estranged_daughter.png` | 96x96 (+192x192) | P1.1 | art/amber_cipher/art_prompts.md#23--pt_estranged_daughter |
| pt_renard_voss | portrait | `art/ui/portraits/amber_cipher/suspect_renard_voss.png` | 96x96 (+192x192) | P1.1 | art/amber_cipher/art_prompts.md#24--pt_renard_voss |
| pt_night_porter | portrait | `art/ui/portraits/amber_cipher/suspect_night_porter.png` | 96x96 (+192x192) | P1.1 | art/amber_cipher/art_prompts.md#25--pt_night_porter |
| pt_platform_guard | portrait | `art/ui/portraits/amber_cipher/suspect_platform_guard.png` | 96x96 (+192x192) | P1.1 | art/amber_cipher/art_prompts.md#26--pt_platform_guard |
| pt_travelling_broker | portrait | `art/ui/portraits/amber_cipher/suspect_travelling_broker.png` | 96x96 (+192x192) | P1.1 | art/amber_cipher/art_prompts.md#27--pt_travelling_broker |
| pt_ticket_clerk | portrait | `art/ui/portraits/amber_cipher/witness_ticket_clerk.png` | 96x96 (+192x192) | P1.1 | art/amber_cipher/art_prompts.md#28--pt_ticket_clerk |
| pt_porter | portrait | `art/ui/portraits/amber_cipher/witness_porter.png` | 96x96 (+192x192) | P1.1 | art/amber_cipher/art_prompts.md#29--pt_porter |
| pt_signalman | portrait | `art/ui/portraits/amber_cipher/witness_signalman.png` | 96x96 (+192x192) | P1.1 | art/amber_cipher/art_prompts.md#210--pt_signalman |
| pt_carriage_cleaner | portrait | `art/ui/portraits/amber_cipher/witness_carriage_cleaner.png` | 96x96 (+192x192) | P1.1 | art/amber_cipher/art_prompts.md#211--pt_carriage_cleaner |
| pt_telegraph_operator | portrait | `art/ui/portraits/amber_cipher/witness_telegraph_operator.png` | 96x96 (+192x192) | P1.1 | art/amber_cipher/art_prompts.md#212--pt_telegraph_operator |
| bf_amber_cipher | briefing | `art/ui/cinematics/briefing_amber_cipher.png` | 480x480 | P2.1 | art/amber_cipher/art_prompts.md#31--bf_amber_cipher |
| vc_correct_voss | verdict_card | `art/ui/cinematics/amber_cipher_verdict_correct_voss.png` | 480x480 | P2.2 | art/amber_cipher/art_prompts.md#41--vc_correct_voss |
| vc_partial_correct | verdict_card | `art/ui/cinematics/amber_cipher_verdict_partial_correct.png` | 480x480 | P2.2 | art/amber_cipher/art_prompts.md#42--vc_partial_correct |
| vc_accomplice_found | verdict_card | `art/ui/cinematics/amber_cipher_verdict_accomplice_found.png` | 480x480 | P2.2 | art/amber_cipher/art_prompts.md#43--vc_accomplice_found |
| vc_framed_suspect | verdict_card | `art/ui/cinematics/amber_cipher_verdict_framed_suspect.png` | 480x480 | P2.2 | art/amber_cipher/art_prompts.md#44--vc_framed_suspect |
| vc_motive_only_confession | verdict_card | `art/ui/cinematics/amber_cipher_verdict_motive_only_confession.png` | 480x480 | P2.2 | art/amber_cipher/art_prompts.md#45--vc_motive_only_confession |
| vc_late_revelation | verdict_card | `art/ui/cinematics/amber_cipher_verdict_late_revelation.png` | 480x480 | P2.2 | art/amber_cipher/art_prompts.md#46--vc_late_revelation |
| vc_near_miss | verdict_card | `art/ui/cinematics/amber_cipher_verdict_near_miss.png` | 480x480 | P2.2 | art/amber_cipher/art_prompts.md#47--vc_near_miss |
| vc_cold_trail | verdict_card | `art/ui/cinematics/amber_cipher_verdict_cold_trail.png` | 480x480 | P2.2 | art/amber_cipher/art_prompts.md#48--vc_cold_trail |
| vc_red_herring_trap | verdict_card | `art/ui/cinematics/amber_cipher_verdict_red_herring_trap.png` | 480x480 | P2.2 | art/amber_cipher/art_prompts.md#49--vc_red_herring_trap |
| vc_wrong_template | verdict_card | `art/ui/cinematics/amber_cipher_verdict_wrong_<suspect>.png` (6 renders) | 480x480 | P2.2 | art/amber_cipher/art_prompts.md#410--vc_wrong_template |
| ui_divider | ui_ornament | `art/ui/ornaments/divider_amber_cipher.png` | 480x16 | P0.3 | art/amber_cipher/art_prompts.md#51--ui_divider |

---

## Per-case prompt sheets — attended_hour (2026-06-05)

Prompts authored by `lt-art` skill. See `art/attended_hour/art_prompts.md` for
the full diffusion-ready prompt blocks (style spine, palette, negative prompts,
en/es captions). Case accent: pale clinical_yellow (#E8D77A) + clinical_blue
(#9CB8C6). Defining motif: clock hand swept across the unattended hour.

| id | category | filename | dimensions | priority | prompt sheet |
|---|---|---|---|---|---|
| bd_cardiac_ward_crime_space | backdrop | `art/attended_hour/direct_pixel_art_v1/pixel_320x320/attended_hour_cardiac_ward_crime_space_pixel_320x320_v01.png` | 320x320 | P1.2 | art/attended_hour/art_prompts.md#bd_cardiac_ward_crime_space |
| bd_doctor_office | backdrop | `art/attended_hour/direct_pixel_art_v1/pixel_320x320/attended_hour_doctor_office_pixel_320x320_v01.png` | 320x320 | P1.2 | art/attended_hour/art_prompts.md#bd_doctor_office |
| bd_family_waiting_room | backdrop | `art/attended_hour/direct_pixel_art_v1/pixel_320x320/attended_hour_family_waiting_room_pixel_320x320_v01.png` | 320x320 | P1.2 | art/attended_hour/art_prompts.md#bd_family_waiting_room |
| bd_hospital_exterior | backdrop | `art/attended_hour/direct_pixel_art_v1/pixel_320x320/attended_hour_hospital_exterior_pixel_320x320_v01.png` | 320x320 | P1.2 | art/attended_hour/art_prompts.md#bd_hospital_exterior |
| bd_medication_charting_area | backdrop | `art/attended_hour/direct_pixel_art_v1/pixel_320x320/attended_hour_medication_charting_area_pixel_320x320_v01.png` | 320x320 | P1.2 | art/attended_hour/art_prompts.md#bd_medication_charting_area |
| bd_nurse_station_vantage | backdrop | `art/attended_hour/direct_pixel_art_v1/pixel_320x320/attended_hour_nurse_station_vantage_pixel_320x320_v01.png` | 320x320 | P1.2 | art/attended_hour/art_prompts.md#bd_nurse_station_vantage |
| bd_rear_clinical_corridor | backdrop | `art/attended_hour/direct_pixel_art_v1/pixel_320x320/attended_hour_rear_clinical_corridor_pixel_320x320_v01.png` | 320x320 | P1.2 | art/attended_hour/art_prompts.md#bd_rear_clinical_corridor |
| bd_reception_threshold | backdrop | `art/attended_hour/direct_pixel_art_v1/pixel_320x320/attended_hour_reception_threshold_pixel_320x320_v01.png` | 320x320 | P1.2 | art/attended_hour/art_prompts.md#bd_reception_threshold |
| bd_service_elevator_zone | backdrop | `art/attended_hour/direct_pixel_art_v1/pixel_320x320/attended_hour_service_elevator_zone_pixel_320x320_v01.png` | 320x320 | P1.2 | art/attended_hour/art_prompts.md#bd_service_elevator_zone |
| bd_staff_break_or_overnight_desk_area | backdrop | `art/attended_hour/direct_pixel_art_v1/pixel_320x320/attended_hour_staff_break_or_overnight_desk_area_pixel_320x320_v01.png` | 320x320 | P1.2 | art/attended_hour/art_prompts.md#bd_staff_break_or_overnight_desk_area |
| pt_callum_dray | portrait | `art/ui/portraits/attended_hour/suspect_callum_dray.png` | 96x96 (+192x192) | P1.1 | art/attended_hour/art_prompts.md#pt_callum_dray |
| pt_aldworth | portrait | `art/ui/portraits/attended_hour/suspect_nurse_aldworth.png` | 96x96 (+192x192) | P1.1 | art/attended_hour/art_prompts.md#pt_aldworth |
| pt_pharmacist_lin | portrait | `art/ui/portraits/attended_hour/suspect_pharmacist_lin.png` | 96x96 (+192x192) | P1.1 | art/attended_hour/art_prompts.md#pt_pharmacist_lin |
| pt_owen_stroud | portrait | `art/ui/portraits/attended_hour/suspect_owen_stroud.png` | 96x96 (+192x192) | P1.1 | art/attended_hour/art_prompts.md#pt_owen_stroud |
| pt_parris | portrait | `art/ui/portraits/attended_hour/suspect_dr_parris.png` | 96x96 (+192x192) | P1.1 | art/attended_hour/art_prompts.md#pt_parris |
| pt_records_clerk | portrait | `art/ui/portraits/attended_hour/suspect_records_clerk.png` | 96x96 (+192x192) | P1.1 | art/attended_hour/art_prompts.md#pt_records_clerk |
| pt_solicitor_pike | portrait | `art/ui/portraits/attended_hour/suspect_solicitor_pike.png` | 96x96 (+192x192) | P1.1 | art/attended_hour/art_prompts.md#pt_solicitor_pike |
| pt_night_porter | portrait | `art/ui/portraits/attended_hour/witness_night_porter.png` | 96x96 (+192x192) | P1.1 | art/attended_hour/art_prompts.md#pt_night_porter |
| pt_ward_orderly | portrait | `art/ui/portraits/attended_hour/witness_ward_orderly.png` | 96x96 (+192x192) | P1.1 | art/attended_hour/art_prompts.md#pt_ward_orderly |
| pt_lab_assistant | portrait | `art/ui/portraits/attended_hour/witness_lab_assistant.png` | 96x96 (+192x192) | P1.1 | art/attended_hour/art_prompts.md#pt_lab_assistant |
| pt_duty_nurse | portrait | `art/ui/portraits/attended_hour/witness_duty_nurse.png` | 96x96 (+192x192) | P1.1 | art/attended_hour/art_prompts.md#pt_duty_nurse |
| pt_ambulance_driver | portrait | `art/ui/portraits/attended_hour/witness_ambulance_driver.png` | 96x96 (+192x192) | P1.1 | art/attended_hour/art_prompts.md#pt_ambulance_driver |
| br_briefing | briefing | `art/ui/cinematics/briefing_attended_hour.png` | 480x480 | P2.1 | art/attended_hour/art_prompts.md#br_briefing |
| vc_correct | verdict_card | `art/ui/cinematics/attended_hour_verdict_correct.png` | 480x480 | P2.2 | art/attended_hour/art_prompts.md#vc_correct |
| vc_partial | verdict_card | `art/ui/cinematics/attended_hour_verdict_partial.png` | 480x480 | P2.2 | art/attended_hour/art_prompts.md#vc_partial |
| vc_accomplice | verdict_card | `art/ui/cinematics/attended_hour_verdict_accomplice.png` | 480x480 | P2.2 | art/attended_hour/art_prompts.md#vc_accomplice |
| vc_framed | verdict_card | `art/ui/cinematics/attended_hour_verdict_framed.png` | 480x480 | P2.2 | art/attended_hour/art_prompts.md#vc_framed |
| vc_motive_only | verdict_card | `art/ui/cinematics/attended_hour_verdict_motive_only.png` | 480x480 | P2.2 | art/attended_hour/art_prompts.md#vc_motive_only |
| vc_late_revelation | verdict_card | `art/ui/cinematics/attended_hour_verdict_late_revelation.png` | 480x480 | P2.2 | art/attended_hour/art_prompts.md#vc_late_revelation |
| vc_near_miss | verdict_card | `art/ui/cinematics/attended_hour_verdict_near_miss.png` | 480x480 | P2.2 | art/attended_hour/art_prompts.md#vc_near_miss |
| vc_cold_trail | verdict_card | `art/ui/cinematics/attended_hour_verdict_cold_trail.png` | 480x480 | P2.2 | art/attended_hour/art_prompts.md#vc_cold_trail |
| vc_red_herring | verdict_card | `art/ui/cinematics/attended_hour_verdict_red_herring.png` | 480x480 | P2.2 | art/attended_hour/art_prompts.md#vc_red_herring |
| vc_wrong_template | verdict_card | `art/ui/cinematics/attended_hour_verdict_wrong_<suspect>.png` (11 renders) | 480x480 | P2.2 | art/attended_hour/art_prompts.md#vc_wrong_template |
| ui_clock_hands | ui_ornament | `art/ui/ornaments/attended_hour_clock_hands.png` | 64x64 | P0 | art/attended_hour/art_prompts.md#ui_clock_hands |
| ui_medical_cross | ui_ornament | `art/ui/ornaments/attended_hour_medical_cross.png` | 32x32 | P0 | art/attended_hour/art_prompts.md#ui_medical_cross |
| ui_ward_bell | ui_ornament | `art/ui/ornaments/attended_hour_ward_bell.png` | 32x32 | P0 | art/attended_hour/art_prompts.md#ui_ward_bell |
| ui_thumbnail_attended_hour | ui_thumbnail | `art/ui/thumbnails/attended_hour.png` | 64x64 | P0.8 | art/attended_hour/art_prompts.md#ui_thumbnail_attended_hour |

---

## Per-case prompt sheets — fog_over_brussels (2026-06-05)

Prompts authored by `lt-art` skill. See `art/fog_over_brussels/art_prompts.md` for
the full diffusion-ready prompt blocks (style spine, palette, negative prompts,
en/es captions). Case accent: cold-corridor blue (`#16203A`) + amber chandelier
(`#C49A4F`) + fog grey (`#9CB0C8`). Defining motif: the signet ring on the
right hand, turned once.

| id | category | filename | dimensions | priority | prompt sheet |
|---|---|---|---|---|---|
| bd_embassy_entrance | backdrop | `art/fog_over_brussels/direct_pixel_art_v1/pixel_320x320/fog_over_brussels_embassy_entrance_pixel_320x320_v01.png` | 320x320 | P1.2 | art/fog_over_brussels/art_prompts.md#11--bd_embassy_entrance |
| bd_rue_de_la_loi | backdrop | `art/fog_over_brussels/direct_pixel_art_v1/pixel_320x320/fog_over_brussels_rue_de_la_loi_pixel_320x320_v01.png` | 320x320 | P1.2 | art/fog_over_brussels/art_prompts.md#12--bd_rue_de_la_loi |
| bd_reception_room | backdrop | `art/fog_over_brussels/direct_pixel_art_v1/pixel_320x320/fog_over_brussels_reception_room_pixel_320x320_v01.png` | 320x320 | P1.2 | art/fog_over_brussels/art_prompts.md#13--bd_reception_room |
| bd_kitchen_corridor | backdrop | `art/fog_over_brussels/direct_pixel_art_v1/pixel_320x320/fog_over_brussels_kitchen_corridor_pixel_320x320_v01.png` | 320x320 | P1.2 | art/fog_over_brussels/art_prompts.md#14--bd_kitchen_corridor |
| bd_embassy_kitchen | backdrop | `art/fog_over_brussels/direct_pixel_art_v1/pixel_320x320/fog_over_brussels_embassy_kitchen_pixel_320x320_v01.png` | 320x320 | P1.2 | art/fog_over_brussels/art_prompts.md#15--bd_embassy_kitchen |
| bd_cipher_room | backdrop | `art/fog_over_brussels/direct_pixel_art_v1/pixel_320x320/fog_over_brussels_cipher_room_pixel_320x320_v01.png` | 320x320 | P1.2 | art/fog_over_brussels/art_prompts.md#16--bd_cipher_room |
| bd_document_room | backdrop | `art/fog_over_brussels/direct_pixel_art_v1/pixel_320x320/fog_over_brussels_document_room_pixel_320x320_v01.png` | 320x320 | P1.2 | art/fog_over_brussels/art_prompts.md#17--bd_document_room |
| bd_ambassadors_office | backdrop | `art/fog_over_brussels/direct_pixel_art_v1/pixel_320x320/fog_over_brussels_ambassadors_office_pixel_320x320_v01.png` | 320x320 | P1.2 | art/fog_over_brussels/art_prompts.md#18--bd_ambassadors_office |
| bd_east_wing_landing | backdrop | `art/fog_over_brussels/direct_pixel_art_v1/pixel_320x320/fog_over_brussels_east_wing_landing_pixel_320x320_v01.png` | 320x320 | P1.2 | art/fog_over_brussels/art_prompts.md#19--bd_east_wing_landing |
| bd_west_wing_stairwell | backdrop | `art/fog_over_brussels/direct_pixel_art_v1/pixel_320x320/fog_over_brussels_west_wing_stairwell_pixel_320x320_v01.png` | 320x320 | P1.2 | art/fog_over_brussels/art_prompts.md#110--bd_west_wing_stairwell |
| pt_brennan | portrait | `art/ui/portraits/fog_over_brussels/suspect_brennan.png` | 96x96 (+192x192) | P1.1 | art/fog_over_brussels/art_prompts.md#21--pt_brennan |
| pt_helena_voss | portrait | `art/ui/portraits/fog_over_brussels/suspect_helena_voss.png` | 96x96 (+192x192) | P1.1 | art/fog_over_brussels/art_prompts.md#22--pt_helena_voss |
| pt_catering_supervisor | portrait | `art/ui/portraits/fog_over_brussels/suspect_catering_supervisor.png` | 96x96 (+192x192) | P1.1 | art/fog_over_brussels/art_prompts.md#23--pt_catering_supervisor |
| pt_ambassador_voss | portrait | `art/ui/portraits/fog_over_brussels/suspect_ambassador_voss.png` | 96x96 (+192x192) | P1.1 | art/fog_over_brussels/art_prompts.md#24--pt_ambassador_voss |
| pt_cipher_supervisor | portrait | `art/ui/portraits/fog_over_brussels/suspect_cipher_supervisor.png` | 96x96 (+192x192) | P1.1 | art/fog_over_brussels/art_prompts.md#25--pt_cipher_supervisor |
| pt_embassy_doctor | portrait | `art/ui/portraits/fog_over_brussels/suspect_embassy_doctor.png` | 96x96 (+192x192) | P1.1 | art/fog_over_brussels/art_prompts.md#26--pt_embassy_doctor |
| pt_chief_of_security | portrait | `art/ui/portraits/fog_over_brussels/suspect_chief_of_security.png` | 96x96 (+192x192) | P1.1 | art/fog_over_brussels/art_prompts.md#27--pt_chief_of_security |
| pt_press_attache | portrait | `art/ui/portraits/fog_over_brussels/witness_press_attache.png` | 96x96 (+192x192) | P1.1 | art/fog_over_brussels/art_prompts.md#28--pt_press_attache |
| pt_catering_runner | portrait | `art/ui/portraits/fog_over_brussels/witness_catering_runner.png` | 96x96 (+192x192) | P1.1 | art/fog_over_brussels/art_prompts.md#29--pt_catering_runner |
| pt_kitchen_porter | portrait | `art/ui/portraits/fog_over_brussels/witness_kitchen_porter.png` | 96x96 (+192x192) | P1.1 | art/fog_over_brussels/art_prompts.md#210--pt_kitchen_porter |
| pt_ilse_brenner | portrait | `art/ui/portraits/fog_over_brussels/victim_ilse_brenner.png` | 96x96 (+192x192) | P1.1 | art/fog_over_brussels/art_prompts.md#211--pt_ilse_brenner |
| pt_chief_butler | portrait | `art/ui/portraits/fog_over_brussels/witness_chief_butler.png` | 96x96 (+192x192) | P1.1 | art/fog_over_brussels/art_prompts.md#212--pt_chief_butler |
| bf_fog_over_brussels | briefing | `art/ui/cinematics/briefing_fog_over_brussels.png` | 480x480 | P2.1 | art/fog_over_brussels/art_prompts.md#31--bf_fog_over_brussels |
| vc_correct_brennan | verdict_card | `art/ui/cinematics/fog_over_brussels_verdict_correct_brennan.png` | 480x480 | P2.2 | art/fog_over_brussels/art_prompts.md#41--vc_correct_brennan |
| vc_partial_correct | verdict_card | `art/ui/cinematics/fog_over_brussels_verdict_partial_correct.png` | 480x480 | P2.2 | art/fog_over_brussels/art_prompts.md#42--vc_partial_correct |
| vc_accomplice_found | verdict_card | `art/ui/cinematics/fog_over_brussels_verdict_accomplice_found.png` | 480x480 | P2.2 | art/fog_over_brussels/art_prompts.md#43--vc_accomplice_found |
| vc_framed_suspect | verdict_card | `art/ui/cinematics/fog_over_brussels_verdict_framed_suspect.png` | 480x480 | P2.2 | art/fog_over_brussels/art_prompts.md#44--vc_framed_suspect |
| vc_motive_only_confession | verdict_card | `art/ui/cinematics/fog_over_brussels_verdict_motive_only_confession.png` | 480x480 | P2.2 | art/fog_over_brussels/art_prompts.md#45--vc_motive_only_confession |
| vc_late_revelation | verdict_card | `art/ui/cinematics/fog_over_brussels_verdict_late_revelation.png` | 480x480 | P2.2 | art/fog_over_brussels/art_prompts.md#46--vc_late_revelation |
| vc_near_miss | verdict_card | `art/ui/cinematics/fog_over_brussels_verdict_near_miss.png` | 480x480 | P2.2 | art/fog_over_brussels/art_prompts.md#47--vc_near_miss |
| vc_cold_trail | verdict_card | `art/ui/cinematics/fog_over_brussels_verdict_cold_trail.png` | 480x480 | P2.2 | art/fog_over_brussels/art_prompts.md#48--vc_cold_trail |
| vc_red_herring_trap | verdict_card | `art/ui/cinematics/fog_over_brussels_verdict_red_herring_trap.png` | 480x480 | P2.2 | art/fog_over_brussels/art_prompts.md#49--vc_red_herring_trap |
| vc_wrong_template | verdict_card | `art/ui/cinematics/fog_over_brussels_verdict_wrong_<suspect>.png` (8 renders) | 480x480 | P2.2 | art/fog_over_brussels/art_prompts.md#410--vc_wrong_template |
| ui_divider | ui_ornament | `art/ui/ornaments/divider_fog_over_brussels.png` | 480x16 | P0.3 | art/fog_over_brussels/art_prompts.md#51--ui_divider |

---

## Per-case prompt sheets — tidal_interval (2026-06-05)

Prompts authored by `lt-art` skill. See `art/tidal_interval/art_prompts.md` for
the full diffusion-ready prompt blocks (style spine, palette, negative prompts,
en/es captions). Case accent: storm grey (#4A5563) + sea blue (#2D4A66) +
lamp amber (#D9963F). Defining motif: tide-marker chevron / wave-shadow.
Setting is present-day but rendered in the same 16-bit JRPG Victorian-pixel-art
spine for catalogue cohesion.

| id | category | filename | dimensions | priority | prompt sheet |
|---|---|---|---|---|---|
| bd_research_lab | backdrop | `art/tidal_interval/direct_pixel_art_v1/pixel_320x320/tidal_interval_research_lab_pixel_320x320_v01.png` | 320x320 | P1.2 | art/tidal_interval/art_prompts.md#bd_research_lab |
| bd_dorms | backdrop | `art/tidal_interval/direct_pixel_art_v1/pixel_320x320/tidal_interval_dorms_pixel_320x320_v01.png` | 320x320 | P1.2 | art/tidal_interval/art_prompts.md#bd_dorms |
| bd_weather_tower | backdrop | `art/tidal_interval/direct_pixel_art_v1/pixel_320x320/tidal_interval_weather_tower_pixel_320x320_v01.png` | 320x320 | P1.2 | art/tidal_interval/art_prompts.md#bd_weather_tower |
| bd_jetty | backdrop | `art/tidal_interval/direct_pixel_art_v1/pixel_320x320/tidal_interval_jetty_pixel_320x320_v01.png` | 320x320 | P1.2 | art/tidal_interval/art_prompts.md#bd_jetty |
| bd_sea_cave | backdrop | `art/tidal_interval/direct_pixel_art_v1/pixel_320x320/tidal_interval_sea_cave_pixel_320x320_v01.png` | 320x320 | P1.2 | art/tidal_interval/art_prompts.md#bd_sea_cave |
| bd_generator_room | backdrop | `art/tidal_interval/direct_pixel_art_v1/pixel_320x320/tidal_interval_generator_room_pixel_320x320_v01.png` | 320x320 | P1.2 | art/tidal_interval/art_prompts.md#bd_generator_room |
| bd_common_room | backdrop | `art/tidal_interval/direct_pixel_art_v1/pixel_320x320/tidal_interval_common_room_pixel_320x320_v01.png` | 320x320 | P1.2 | art/tidal_interval/art_prompts.md#bd_common_room |
| bd_eastern_path | backdrop | `art/tidal_interval/direct_pixel_art_v1/pixel_320x320/tidal_interval_eastern_path_pixel_320x320_v01.png` | 320x320 | P1.2 | art/tidal_interval/art_prompts.md#bd_eastern_path |
| pt_piers_dunne | portrait | `art/ui/portraits/tidal_interval/suspect_piers_dunne.png` | 96x96 (+192x192) | P1.1 | art/tidal_interval/art_prompts.md#pt_piers_dunne |
| pt_marcus_webb | portrait | `art/ui/portraits/tidal_interval/suspect_marcus_webb.png` | 96x96 (+192x192) | P1.1 | art/tidal_interval/art_prompts.md#pt_marcus_webb |
| pt_oren_halloway | portrait | `art/ui/portraits/tidal_interval/suspect_oren_halloway.png` | 96x96 (+192x192) | P1.1 | art/tidal_interval/art_prompts.md#pt_oren_halloway |
| pt_mira_callan | portrait | `art/ui/portraits/tidal_interval/suspect_mira_callan.png` | 96x96 (+192x192) | P1.1 | art/tidal_interval/art_prompts.md#pt_mira_callan |
| pt_tovi_ansgar | portrait | `art/ui/portraits/tidal_interval/suspect_tovi_ansgar.png` | 96x96 (+192x192) | P1.1 | art/tidal_interval/art_prompts.md#pt_tovi_ansgar |
| pt_kestrel_lin | portrait | `art/ui/portraits/tidal_interval/witness_kestrel_lin.png` | 96x96 (+192x192) | P1.1 | art/tidal_interval/art_prompts.md#pt_kestrel_lin |
| pt_niall_brackett | portrait | `art/ui/portraits/tidal_interval/witness_niall_brackett.png` | 96x96 (+192x192) | P1.1 | art/tidal_interval/art_prompts.md#pt_niall_brackett |
| pt_eira_voss | portrait | `art/ui/portraits/tidal_interval/witness_eira_voss.png` | 96x96 (+192x192) | P1.1 | art/tidal_interval/art_prompts.md#pt_eira_voss |
| pt_padraic_burne | portrait | `art/ui/portraits/tidal_interval/witness_padraic_burne.png` | 96x96 (+192x192) | P1.1 | art/tidal_interval/art_prompts.md#pt_padraic_burne |
| br_briefing | briefing | `art/ui/cinematics/briefing_tidal_interval.png` | 480x480 | P2.1 | art/tidal_interval/art_prompts.md#br_briefing |
| vc_correct_dunne | verdict_card | `art/ui/cinematics/tidal_interval_verdict_correct_dunne.png` | 480x480 | P2.2 | art/tidal_interval/art_prompts.md#vc_correct_dunne |
| vc_partial_correct | verdict_card | `art/ui/cinematics/tidal_interval_verdict_partial_correct.png` | 480x480 | P2.2 | art/tidal_interval/art_prompts.md#vc_partial_correct |
| vc_accomplice_found | verdict_card | `art/ui/cinematics/tidal_interval_verdict_accomplice_found.png` | 480x480 | P2.2 | art/tidal_interval/art_prompts.md#vc_accomplice_found |
| vc_framed_suspect | verdict_card | `art/ui/cinematics/tidal_interval_verdict_framed_suspect.png` | 480x480 | P2.2 | art/tidal_interval/art_prompts.md#vc_framed_suspect |
| vc_motive_only_confession | verdict_card | `art/ui/cinematics/tidal_interval_verdict_motive_only_confession.png` | 480x480 | P2.2 | art/tidal_interval/art_prompts.md#vc_motive_only_confession |
| vc_late_revelation | verdict_card | `art/ui/cinematics/tidal_interval_verdict_late_revelation.png` | 480x480 | P2.2 | art/tidal_interval/art_prompts.md#vc_late_revelation |
| vc_near_miss | verdict_card | `art/ui/cinematics/tidal_interval_verdict_near_miss.png` | 480x480 | P2.2 | art/tidal_interval/art_prompts.md#vc_near_miss |
| vc_cold_trail | verdict_card | `art/ui/cinematics/tidal_interval_verdict_cold_trail.png` | 480x480 | P2.2 | art/tidal_interval/art_prompts.md#vc_cold_trail |
| vc_red_herring_trap | verdict_card | `art/ui/cinematics/tidal_interval_verdict_red_herring_trap.png` | 480x480 | P2.2 | art/tidal_interval/art_prompts.md#vc_red_herring_trap |
| vc_wrong_template | verdict_card | `art/ui/cinematics/tidal_interval_verdict_wrong_<suspect>.png` (6 renders) | 480x480 | P2.2 | art/tidal_interval/art_prompts.md#vc_wrong_template |
| ui_tide_chevron | ui_ornament | `art/ui/ornaments/tidal_interval_tide_chevron.png` | 64x64 | P0 | art/tidal_interval/art_prompts.md#ui_tide_chevron |
| ui_wave_shadow | ui_ornament | `art/ui/ornaments/tidal_interval_wave_shadow.png` | 480x16 | P0.3 | art/tidal_interval/art_prompts.md#ui_wave_shadow |
| ui_thumbnail_tidal_interval | ui_thumbnail | `art/ui/thumbnails/tidal_interval.png` | 64x64 | P0.8 | art/tidal_interval/art_prompts.md#ui_thumbnail_tidal_interval |

## hollow_season — full prompt sheet

Generated via `lt-art` skill on 2026-06-05. Total 39 prompts (10 location
backdrops + 10 portraits + 1 briefing + 15 verdict cards + 3 UI ornaments, all
en/es captioned). Case accent: late-summer green (#7A8A4E) + dust-cream (#E8DCC0)
+ lawn-amber (#C9A24E) + mahogany (#4A2E1C). Defining motif:
croquet-mallet-and-hoop crossed with dovecote-silhouette, framed-portrait corners.
Setting is Edwardian August 1907; pixel-art spine renders the country house in
late-summer slanting light, paraffin-lamp interiors, slate-blue cool dawns.

| id | category | filename | dimensions | priority | prompt sheet |
|---|---|---|---|---|---|
| bd_library | backdrop | `art/hollow_season/direct_pixel_art_v1/pixel_320x320/hollow_season_library_pixel_320x320_v01.png` | 320x320 | P1.2 | art/hollow_season/art_prompts.md#bd_library |
| bd_drawing_room | backdrop | `art/hollow_season/direct_pixel_art_v1/pixel_320x320/hollow_season_drawing_room_pixel_320x320_v01.png` | 320x320 | P1.2 | art/hollow_season/art_prompts.md#bd_drawing_room |
| bd_dining_room | backdrop | `art/hollow_season/direct_pixel_art_v1/pixel_320x320/hollow_season_dining_room_pixel_320x320_v01.png` | 320x320 | P1.2 | art/hollow_season/art_prompts.md#bd_dining_room |
| bd_gun_room | backdrop | `art/hollow_season/direct_pixel_art_v1/pixel_320x320/hollow_season_gun_room_pixel_320x320_v01.png` | 320x320 | P1.2 | art/hollow_season/art_prompts.md#bd_gun_room |
| bd_summer_house | backdrop | `art/hollow_season/direct_pixel_art_v1/pixel_320x320/hollow_season_summer_house_pixel_320x320_v01.png` | 320x320 | P1.2 | art/hollow_season/art_prompts.md#bd_summer_house |
| bd_walled_garden | backdrop | `art/hollow_season/direct_pixel_art_v1/pixel_320x320/hollow_season_walled_garden_pixel_320x320_v01.png` | 320x320 | P1.2 | art/hollow_season/art_prompts.md#bd_walled_garden |
| bd_gatehouse_lodge | backdrop | `art/hollow_season/direct_pixel_art_v1/pixel_320x320/hollow_season_gatehouse_lodge_pixel_320x320_v01.png` | 320x320 | P1.2 | art/hollow_season/art_prompts.md#bd_gatehouse_lodge |
| bd_servants_hall | backdrop | `art/hollow_season/direct_pixel_art_v1/pixel_320x320/hollow_season_servants_hall_pixel_320x320_v01.png` | 320x320 | P1.2 | art/hollow_season/art_prompts.md#bd_servants_hall |
| bd_estate_office | backdrop | `art/hollow_season/direct_pixel_art_v1/pixel_320x320/hollow_season_estate_office_pixel_320x320_v01.png` | 320x320 | P1.2 | art/hollow_season/art_prompts.md#bd_estate_office |
| bd_village_rooms | backdrop | `art/hollow_season/direct_pixel_art_v1/pixel_320x320/hollow_season_village_rooms_pixel_320x320_v01.png` | 320x320 | P1.2 | art/hollow_season/art_prompts.md#bd_village_rooms |
| pt_edmund_carrow | portrait | `art/ui/portraits/hollow_season/suspect_edmund_carrow.png` | 96x96 (+192x192) | P1.1 | art/hollow_season/art_prompts.md#pt_edmund_carrow |
| pt_hector_finch | portrait | `art/ui/portraits/hollow_season/suspect_hector_finch.png` | 96x96 (+192x192) | P1.1 | art/hollow_season/art_prompts.md#pt_hector_finch |
| pt_mrs_lyle | portrait | `art/ui/portraits/hollow_season/witness_mrs_lyle.png` | 96x96 (+192x192) | P1.1 | art/hollow_season/art_prompts.md#pt_mrs_lyle |
| pt_mr_croft | portrait | `art/ui/portraits/hollow_season/suspect_mr_croft.png` | 96x96 (+192x192) | P1.1 | art/hollow_season/art_prompts.md#pt_mr_croft |
| pt_mrs_penrose | portrait | `art/ui/portraits/hollow_season/suspect_mrs_penrose.png` | 96x96 (+192x192) | P1.1 | art/hollow_season/art_prompts.md#pt_mrs_penrose |
| pt_butler_hadley | portrait | `art/ui/portraits/hollow_season/witness_butler_hadley.png` | 96x96 (+192x192) | P1.1 | art/hollow_season/art_prompts.md#pt_butler_hadley |
| pt_under_gardener | portrait | `art/ui/portraits/hollow_season/witness_under_gardener.png` | 96x96 (+192x192) | P1.1 | art/hollow_season/art_prompts.md#pt_under_gardener |
| pt_ladies_maid | portrait | `art/ui/portraits/hollow_season/witness_ladies_maid.png` | 96x96 (+192x192) | P1.1 | art/hollow_season/art_prompts.md#pt_ladies_maid |
| pt_village_chemist | portrait | `art/ui/portraits/hollow_season/witness_village_chemist.png` | 96x96 (+192x192) | P1.1 | art/hollow_season/art_prompts.md#pt_village_chemist |
| pt_solicitor_aldhurst | portrait | `art/ui/portraits/hollow_season/witness_solicitor_aldhurst.png` | 96x96 (+192x192) | P1.1 | art/hollow_season/art_prompts.md#pt_solicitor_aldhurst |
| br_briefing | briefing | `art/ui/cinematics/briefing_hollow_season.png` | 480x480 | P2.1 | art/hollow_season/art_prompts.md#br_briefing |
| vc_correct_edmund | verdict_card | `art/ui/cinematics/hollow_season_verdict_correct_edmund.png` | 480x480 | P2.2 | art/hollow_season/art_prompts.md#vc_correct_edmund |
| vc_partial_correct | verdict_card | `art/ui/cinematics/hollow_season_verdict_partial_correct.png` | 480x480 | P2.2 | art/hollow_season/art_prompts.md#vc_partial_correct |
| vc_accomplice_found | verdict_card | `art/ui/cinematics/hollow_season_verdict_accomplice_found.png` | 480x480 | P2.2 | art/hollow_season/art_prompts.md#vc_accomplice_found |
| vc_framed_suspect | verdict_card | `art/ui/cinematics/hollow_season_verdict_framed_suspect.png` | 480x480 | P2.2 | art/hollow_season/art_prompts.md#vc_framed_suspect |
| vc_motive_only_confession | verdict_card | `art/ui/cinematics/hollow_season_verdict_motive_only_confession.png` | 480x480 | P2.2 | art/hollow_season/art_prompts.md#vc_motive_only_confession |
| vc_late_revelation | verdict_card | `art/ui/cinematics/hollow_season_verdict_late_revelation.png` | 480x480 | P2.2 | art/hollow_season/art_prompts.md#vc_late_revelation |
| vc_near_miss | verdict_card | `art/ui/cinematics/hollow_season_verdict_near_miss.png` | 480x480 | P2.2 | art/hollow_season/art_prompts.md#vc_near_miss |
| vc_cold_trail | verdict_card | `art/ui/cinematics/hollow_season_verdict_cold_trail.png` | 480x480 | P2.2 | art/hollow_season/art_prompts.md#vc_cold_trail |
| vc_red_herring_trap | verdict_card | `art/ui/cinematics/hollow_season_verdict_red_herring_trap.png` | 480x480 | P2.2 | art/hollow_season/art_prompts.md#vc_red_herring_trap |
| vc_wrong_template | verdict_card | `art/ui/cinematics/hollow_season_verdict_wrong_<suspect>.png` (6 renders) | 480x480 | P2.2 | art/hollow_season/art_prompts.md#vc_wrong_template |
| ui_croquet_dovecote | ui_ornament | `art/ui/ornaments/hollow_season_croquet_dovecote.png` | 64x64 | P0 | art/hollow_season/art_prompts.md#ui_croquet_dovecote |
| ui_portrait_corner | ui_ornament | `art/ui/ornaments/hollow_season_portrait_corner.png` | 480x16 | P0.3 | art/hollow_season/art_prompts.md#ui_portrait_corner |
| ui_thumbnail_hollow_season | ui_thumbnail | `art/ui/thumbnails/hollow_season.png` | 64x64 | P0.8 | art/hollow_season/art_prompts.md#ui_thumbnail_hollow_season |

---

## Per-case prompt sheets — resonance_test (2026-06-05)

Prompts authored by `lt-art` skill. See `art/resonance_test/art_prompts.md`
for the full diffusion-ready prompt blocks (style spine, palette, negative
prompts, en/es captions). Case accent: 1974 tan (#C9A56C) + dust-rose
(#B47E78) + conservatory-amber (#C49640) + cassette-reel green (#4A5C4D)
against the canonical ink-blue/charcoal catalogue. Defining motif: tuning-fork
+ staff-line + cassette-reel divider; the resonance test is the case
about listening.

| id | category | filename | dimensions | priority | prompt sheet |
|---|---|---|---|---|---|
| bd_practice_room_a | backdrop | `art/resonance_test/direct_pixel_art_v1/pixel_320x320/resonance_test_practice_room_a_pixel_320x320_v01.png` | 320x320 | P1.2 | art/resonance_test/art_prompts.md#11--bd_practice_room_a |
| bd_practice_wing_basement | backdrop | `art/resonance_test/direct_pixel_art_v1/pixel_320x320/resonance_test_practice_wing_basement_pixel_320x320_v01.png` | 320x320 | P1.2 | art/resonance_test/art_prompts.md#12--bd_practice_wing_basement |
| bd_recital_hall | backdrop | `art/resonance_test/direct_pixel_art_v1/pixel_320x320/resonance_test_recital_hall_pixel_320x320_v01.png` | 320x320 | P1.2 | art/resonance_test/art_prompts.md#13--bd_recital_hall |
| bd_faculty_lounge | backdrop | `art/resonance_test/direct_pixel_art_v1/pixel_320x320/resonance_test_faculty_lounge_pixel_320x320_v01.png` | 320x320 | P1.2 | art/resonance_test/art_prompts.md#14--bd_faculty_lounge |
| bd_ashby_office | backdrop | `art/resonance_test/direct_pixel_art_v1/pixel_320x320/resonance_test_ashby_office_pixel_320x320_v01.png` | 320x320 | P1.2 | art/resonance_test/art_prompts.md#15--bd_ashby_office |
| bd_archive_basement | backdrop | `art/resonance_test/direct_pixel_art_v1/pixel_320x320/resonance_test_archive_basement_pixel_320x320_v01.png` | 320x320 | P1.2 | art/resonance_test/art_prompts.md#16--bd_archive_basement |
| bd_library_periodicals | backdrop | `art/resonance_test/direct_pixel_art_v1/pixel_320x320/resonance_test_library_periodicals_pixel_320x320_v01.png` | 320x320 | P1.2 | art/resonance_test/art_prompts.md#17--bd_library_periodicals |
| bd_porters_lodge | backdrop | `art/resonance_test/direct_pixel_art_v1/pixel_320x320/resonance_test_porters_lodge_pixel_320x320_v01.png` | 320x320 | P1.2 | art/resonance_test/art_prompts.md#18--bd_porters_lodge |
| bd_harmony_classroom | backdrop | `art/resonance_test/direct_pixel_art_v1/pixel_320x320/resonance_test_harmony_classroom_pixel_320x320_v01.png` | 320x320 | P1.2 | art/resonance_test/art_prompts.md#19--bd_harmony_classroom |
| bd_courtyard | backdrop | `art/resonance_test/direct_pixel_art_v1/pixel_320x320/resonance_test_courtyard_pixel_320x320_v01.png` | 320x320 | P1.2 | art/resonance_test/art_prompts.md#110--bd_courtyard |
| pt_marta_solis | portrait | `art/ui/portraits/resonance_test/suspect_marta_solis.png` | 96x96 (+192x192) | P1.1 | art/resonance_test/art_prompts.md#21--pt_marta_solis |
| pt_james_okafor | portrait | `art/ui/portraits/resonance_test/suspect_james_okafor.png` | 96x96 (+192x192) | P1.1 | art/resonance_test/art_prompts.md#22--pt_james_okafor |
| pt_peter_haldane | portrait | `art/ui/portraits/resonance_test/suspect_peter_haldane.png` | 96x96 (+192x192) | P1.1 | art/resonance_test/art_prompts.md#23--pt_peter_haldane |
| pt_nikolai_renko | portrait | `art/ui/portraits/resonance_test/suspect_nikolai_renko.png` | 96x96 (+192x192) | P1.1 | art/resonance_test/art_prompts.md#24--pt_nikolai_renko |
| pt_eleanor_fairchild | portrait | `art/ui/portraits/resonance_test/witness_eleanor_fairchild.png` | 96x96 (+192x192) | P1.1 | art/resonance_test/art_prompts.md#25--pt_eleanor_fairchild |
| pt_archive_clerk_norwood | portrait | `art/ui/portraits/resonance_test/witness_archive_clerk_norwood.png` | 96x96 (+192x192) | P1.1 | art/resonance_test/art_prompts.md#26--pt_archive_clerk_norwood |
| pt_practice_room_attendant | portrait | `art/ui/portraits/resonance_test/witness_practice_room_attendant.png` | 96x96 (+192x192) | P1.1 | art/resonance_test/art_prompts.md#27--pt_practice_room_attendant |
| pt_ensemble_leader_pryce | portrait | `art/ui/portraits/resonance_test/witness_ensemble_leader_pryce.png` | 96x96 (+192x192) | P1.1 | art/resonance_test/art_prompts.md#28--pt_ensemble_leader_pryce |
| pt_neighbour_thirsk | portrait | `art/ui/portraits/resonance_test/witness_neighbour_thirsk.png` | 96x96 (+192x192) | P1.1 | art/resonance_test/art_prompts.md#29--pt_neighbour_thirsk |
| pt_night_porter_keaveney | portrait | `art/ui/portraits/resonance_test/witness_night_porter_keaveney.png` | 96x96 (+192x192) | P1.1 | art/resonance_test/art_prompts.md#210--pt_night_porter_keaveney |
| pt_records_clerk_aldgate | portrait | `art/ui/portraits/resonance_test/witness_records_clerk_aldgate.png` | 96x96 (+192x192) | P1.1 | art/resonance_test/art_prompts.md#211--pt_records_clerk_aldgate |
| bf_resonance_test | briefing | `art/ui/cinematics/briefing_resonance_test.png` | 480x480 | P2.1 | art/resonance_test/art_prompts.md#31--bf_resonance_test |
| vc_correct_marta_solis | verdict_card | `art/ui/cinematics/resonance_test_verdict_correct_marta_solis.png` | 480x480 | P2.2 | art/resonance_test/art_prompts.md#41--vc_correct_marta_solis |
| vc_partial_correct | verdict_card | `art/ui/cinematics/resonance_test_verdict_partial_correct.png` | 480x480 | P2.2 | art/resonance_test/art_prompts.md#42--vc_partial_correct |
| vc_accomplice_found | verdict_card | `art/ui/cinematics/resonance_test_verdict_accomplice_found.png` | 480x480 | P2.2 | art/resonance_test/art_prompts.md#43--vc_accomplice_found |
| vc_framed_suspect | verdict_card | `art/ui/cinematics/resonance_test_verdict_framed_suspect.png` | 480x480 | P2.2 | art/resonance_test/art_prompts.md#44--vc_framed_suspect |
| vc_motive_only_confession | verdict_card | `art/ui/cinematics/resonance_test_verdict_motive_only_confession.png` | 480x480 | P2.2 | art/resonance_test/art_prompts.md#45--vc_motive_only_confession |
| vc_late_revelation | verdict_card | `art/ui/cinematics/resonance_test_verdict_late_revelation.png` | 480x480 | P2.2 | art/resonance_test/art_prompts.md#46--vc_late_revelation |
| vc_near_miss | verdict_card | `art/ui/cinematics/resonance_test_verdict_near_miss.png` | 480x480 | P2.2 | art/resonance_test/art_prompts.md#47--vc_near_miss |
| vc_cold_trail | verdict_card | `art/ui/cinematics/resonance_test_verdict_cold_trail.png` | 480x480 | P2.2 | art/resonance_test/art_prompts.md#48--vc_cold_trail |
| vc_red_herring_trap | verdict_card | `art/ui/cinematics/resonance_test_verdict_red_herring_trap.png` | 480x480 | P2.2 | art/resonance_test/art_prompts.md#49--vc_red_herring_trap |
| vc_wrong_template | verdict_card | `art/ui/cinematics/resonance_test_verdict_wrong_<suspect>.png` (8 renders) | 480x480 | P2.2 | art/resonance_test/art_prompts.md#410--vc_wrong_template |
| ui_divider | ui_ornament | `art/ui/ornaments/divider_resonance_test.png` | 480x16 | P0.3 | art/resonance_test/art_prompts.md#51--ui_divider |

---

## Per-case prompt sheets — third_signature (2026-06-05)

Prompts authored by `lt-art` skill. See `art/third_signature/art_prompts.md` for
the full diffusion-ready prompt blocks (style spine, palette, negative prompts,
en/es captions). Case accent: mahogany red-brown (#5B2E1F) + club-green (#2F4A38)
+ fog-grey (#A3A6A0) + brass (#B08A3F). Defining motif: quill-and-ink-blot /
club-shield / leather-bound-book-spine. Setting is the Aldgate Club, Bloomsbury,
Wednesday evening in winter 1935. SIGNATURE_TELL is the case-specific
extension dimension — handwriting, leftward slope, dedication-page match.

| id | category | filename | dimensions | priority | prompt sheet |
|---|---|---|---|---|---|
| bd_club_steps | backdrop | `art/third_signature/direct_pixel_art_v1/pixel_320x320/third_signature_club_steps_pixel_320x320_v01.png` | 320x320 | P1.2 | art/third_signature/art_prompts.md#bd_club_steps |
| bd_porters_lodge | backdrop | `art/third_signature/direct_pixel_art_v1/pixel_320x320/third_signature_porters_lodge_pixel_320x320_v01.png` | 320x320 | P1.2 | art/third_signature/art_prompts.md#bd_porters_lodge |
| bd_smoking_room | backdrop | `art/third_signature/direct_pixel_art_v1/pixel_320x320/third_signature_smoking_room_pixel_320x320_v01.png` | 320x320 | P1.2 | art/third_signature/art_prompts.md#bd_smoking_room |
| bd_reading_room | backdrop | `art/third_signature/direct_pixel_art_v1/pixel_320x320/third_signature_reading_room_pixel_320x320_v01.png` | 320x320 | P1.2 | art/third_signature/art_prompts.md#bd_reading_room |
| bd_library | backdrop | `art/third_signature/direct_pixel_art_v1/pixel_320x320/third_signature_library_pixel_320x320_v01.png` | 320x320 | P1.2 | art/third_signature/art_prompts.md#bd_library |
| bd_dining_room | backdrop | `art/third_signature/direct_pixel_art_v1/pixel_320x320/third_signature_dining_room_pixel_320x320_v01.png` | 320x320 | P1.2 | art/third_signature/art_prompts.md#bd_dining_room |
| bd_manuscript_archive | backdrop | `art/third_signature/direct_pixel_art_v1/pixel_320x320/third_signature_manuscript_archive_pixel_320x320_v01.png` | 320x320 | P1.2 | art/third_signature/art_prompts.md#bd_manuscript_archive |
| bd_members_snug | backdrop | `art/third_signature/direct_pixel_art_v1/pixel_320x320/third_signature_members_snug_pixel_320x320_v01.png` | 320x320 | P1.2 | art/third_signature/art_prompts.md#bd_members_snug |
| bd_basement_records | backdrop | `art/third_signature/direct_pixel_art_v1/pixel_320x320/third_signature_basement_records_pixel_320x320_v01.png` | 320x320 | P1.2 | art/third_signature/art_prompts.md#bd_basement_records |
| bd_club_corridor | backdrop | `art/third_signature/direct_pixel_art_v1/pixel_320x320/third_signature_club_corridor_pixel_320x320_v01.png` | 320x320 | P1.2 | art/third_signature/art_prompts.md#bd_club_corridor |
| pt_agnes_vail | portrait | `art/ui/portraits/third_signature/suspect_agnes_vail.png` | 96x96 (+192x192) | P1.1 | art/third_signature/art_prompts.md#pt_agnes_vail |
| pt_carey | portrait | `art/ui/portraits/third_signature/suspect_carey.png` | 96x96 (+192x192) | P1.1 | art/third_signature/art_prompts.md#pt_carey |
| pt_publisher_dent | portrait | `art/ui/portraits/third_signature/suspect_publisher_dent.png` | 96x96 (+192x192) | P1.1 | art/third_signature/art_prompts.md#pt_publisher_dent |
| pt_lillian_march | portrait | `art/ui/portraits/third_signature/suspect_lillian_march.png` | 96x96 (+192x192) | P1.1 | art/third_signature/art_prompts.md#pt_lillian_march |
| pt_colonel_norris | portrait | `art/ui/portraits/third_signature/suspect_colonel_norris.png` | 96x96 (+192x192) | P1.1 | art/third_signature/art_prompts.md#pt_colonel_norris |
| pt_archivist_kemp | portrait | `art/ui/portraits/third_signature/suspect_archivist_kemp.png` | 96x96 (+192x192) | P1.1 | art/third_signature/art_prompts.md#pt_archivist_kemp |
| pt_dining_steward | portrait | `art/ui/portraits/third_signature/suspect_dining_steward.png` | 96x96 (+192x192) | P1.1 | art/third_signature/art_prompts.md#pt_dining_steward |
| pt_wills | portrait | `art/ui/portraits/third_signature/witness_wills.png` | 96x96 (+192x192) | P1.1 | art/third_signature/art_prompts.md#pt_wills |
| pt_hugh_emberly | portrait | `art/ui/portraits/third_signature/witness_hugh_emberly.png` | 96x96 (+192x192) | P1.1 | art/third_signature/art_prompts.md#pt_hugh_emberly |
| pt_dr_pryce | portrait | `art/ui/portraits/third_signature/witness_dr_pryce.png` | 96x96 (+192x192) | P1.1 | art/third_signature/art_prompts.md#pt_dr_pryce |
| pt_club_secretary | portrait | `art/ui/portraits/third_signature/witness_club_secretary.png` | 96x96 (+192x192) | P1.1 | art/third_signature/art_prompts.md#pt_club_secretary |
| pt_biographer_holm | portrait | `art/ui/portraits/third_signature/witness_biographer_holm.png` | 96x96 (+192x192) | P1.1 | art/third_signature/art_prompts.md#pt_biographer_holm |
| br_briefing | briefing | `art/ui/cinematics/briefing_third_signature.png` | 480x480 | P2.1 | art/third_signature/art_prompts.md#br_briefing |
| vc_correct | verdict_card | `art/ui/cinematics/third_signature_verdict_correct.png` | 480x480 | P2.2 | art/third_signature/art_prompts.md#vc_correct |
| vc_partial_correct | verdict_card | `art/ui/cinematics/third_signature_verdict_partial_correct.png` | 480x480 | P2.2 | art/third_signature/art_prompts.md#vc_partial_correct |
| vc_accomplice_found | verdict_card | `art/ui/cinematics/third_signature_verdict_accomplice_found.png` | 480x480 | P2.2 | art/third_signature/art_prompts.md#vc_accomplice_found |
| vc_framed_suspect | verdict_card | `art/ui/cinematics/third_signature_verdict_framed_suspect.png` | 480x480 | P2.2 | art/third_signature/art_prompts.md#vc_framed_suspect |
| vc_motive_only_confession | verdict_card | `art/ui/cinematics/third_signature_verdict_motive_only_confession.png` | 480x480 | P2.2 | art/third_signature/art_prompts.md#vc_motive_only_confession |
| vc_late_revelation | verdict_card | `art/ui/cinematics/third_signature_verdict_late_revelation.png` | 480x480 | P2.2 | art/third_signature/art_prompts.md#vc_late_revelation |
| vc_near_miss | verdict_card | `art/ui/cinematics/third_signature_verdict_near_miss.png` | 480x480 | P2.2 | art/third_signature/art_prompts.md#vc_near_miss |
| vc_cold_trail | verdict_card | `art/ui/cinematics/third_signature_verdict_cold_trail.png` | 480x480 | P2.2 | art/third_signature/art_prompts.md#vc_cold_trail |
| vc_red_herring_trap | verdict_card | `art/ui/cinematics/third_signature_verdict_red_herring_trap.png` | 480x480 | P2.2 | art/third_signature/art_prompts.md#vc_red_herring_trap |
| vc_wrong_template | verdict_card | `art/ui/cinematics/third_signature_verdict_wrong_<suspect>.png` (6 renders) | 480x480 | P2.2 | art/third_signature/art_prompts.md#vc_wrong_template |
| ui_quill_inkblot | ui_ornament | `art/ui/ornaments/third_signature_quill_inkblot.png` | 64x64 | P0 | art/third_signature/art_prompts.md#ui_quill_inkblot |
| ui_club_shield | ui_ornament | `art/ui/ornaments/third_signature_club_shield.png` | 64x64 | P0 | art/third_signature/art_prompts.md#ui_club_shield |
| ui_leatherbook_spine | ui_ornament | `art/ui/ornaments/third_signature_leatherbook_spine.png` | 32x96 | P0 | art/third_signature/art_prompts.md#ui_leatherbook_spine |
| ui_thumbnail_third_signature | ui_thumbnail | `art/ui/thumbnails/third_signature.png` | 64x64 | P0.8 | art/third_signature/art_prompts.md#ui_thumbnail_third_signature |

---

## Per-case prompt sheets — orchard_at_dusk (2026-06-06)

Prompts authored by `lt-art` skill. See `art/orchard_at_dusk/art_prompts.md` for
the full diffusion-ready prompt blocks (style spine, palette, negative prompts,
en/es captions). Case accent: orchard-green + harvest-gold + dusk-rose +
cider-amber + lamplit-cottage warm. Rural Edwardian (Mendip country, September
1903), Obra Dinn cartouche meets countryside-painterly.

| id | category | filename | dimensions | priority | prompt sheet |
|---|---|---|---|---|---|
| bd_crale_orchard | backdrop | `art/orchard_at_dusk/direct_pixel_art_v1/pixel_320x320/orchard_at_dusk_crale_orchard_pixel_320x320_v01.png` | 320x320 | P1.2 | art/orchard_at_dusk/art_prompts.md#11--bd_crale_orchard |
| bd_cider_press | backdrop | `art/orchard_at_dusk/direct_pixel_art_v1/pixel_320x320/orchard_at_dusk_cider_press_pixel_320x320_v01.png` | 320x320 | P1.2 | art/orchard_at_dusk/art_prompts.md#12--bd_cider_press |
| bd_crale_farmhouse_kitchen | backdrop | `art/orchard_at_dusk/direct_pixel_art_v1/pixel_320x320/orchard_at_dusk_crale_farmhouse_kitchen_pixel_320x320_v01.png` | 320x320 | P1.2 | art/orchard_at_dusk/art_prompts.md#13--bd_crale_farmhouse_kitchen |
| bd_orchard_lane | backdrop | `art/orchard_at_dusk/direct_pixel_art_v1/pixel_320x320/orchard_at_dusk_orchard_lane_pixel_320x320_v01.png` | 320x320 | P1.2 | art/orchard_at_dusk/art_prompts.md#14--bd_orchard_lane |
| bd_field_gate | backdrop | `art/orchard_at_dusk/direct_pixel_art_v1/pixel_320x320/orchard_at_dusk_field_gate_in_long_grass_pixel_320x320_v01.png` | 320x320 | P1.2 | art/orchard_at_dusk/art_prompts.md#15--bd_field_gate |
| bd_webb_farm | backdrop | `art/orchard_at_dusk/direct_pixel_art_v1/pixel_320x320/orchard_at_dusk_webb_farm_yard_pixel_320x320_v01.png` | 320x320 | P1.2 | art/orchard_at_dusk/art_prompts.md#16--bd_webb_farm |
| bd_village_inn | backdrop | `art/orchard_at_dusk/direct_pixel_art_v1/pixel_320x320/orchard_at_dusk_hawk_and_shoe_inn_pixel_320x320_v01.png` | 320x320 | P1.2 | art/orchard_at_dusk/art_prompts.md#17--bd_village_inn |
| bd_parish_church | backdrop | `art/orchard_at_dusk/direct_pixel_art_v1/pixel_320x320/orchard_at_dusk_parish_church_pixel_320x320_v01.png` | 320x320 | P1.2 | art/orchard_at_dusk/art_prompts.md#18--bd_parish_church |
| bd_registry_office | backdrop | `art/orchard_at_dusk/direct_pixel_art_v1/pixel_320x320/orchard_at_dusk_bristol_registry_office_pixel_320x320_v01.png` | 320x320 | P1.2 | art/orchard_at_dusk/art_prompts.md#19--bd_registry_office |
| pt_thomas_crale | portrait | `art/ui/portraits/orchard_at_dusk/suspect_thomas_crale.png` | 96x96 (+192x192) | P1.1 | art/orchard_at_dusk/art_prompts.md#21--pt_thomas_crale |
| pt_amos_webb | portrait | `art/ui/portraits/orchard_at_dusk/suspect_amos_webb.png` | 96x96 (+192x192) | P1.1 | art/orchard_at_dusk/art_prompts.md#22--pt_amos_webb |
| pt_eliza_crale | portrait | `art/ui/portraits/orchard_at_dusk/suspect_eliza_crale.png` | 96x96 (+192x192) | P1.1 | art/orchard_at_dusk/art_prompts.md#23--pt_eliza_crale |
| pt_hob_tilling | portrait | `art/ui/portraits/orchard_at_dusk/suspect_hob_tilling.png` | 96x96 (+192x192) | P1.1 | art/orchard_at_dusk/art_prompts.md#24--pt_hob_tilling |
| pt_reverend_caddick | portrait | `art/ui/portraits/orchard_at_dusk/witness_reverend_caddick.png` | 96x96 (+192x192) | P1.1 | art/orchard_at_dusk/art_prompts.md#25--pt_reverend_caddick |
| pt_constable_briggs | portrait | `art/ui/portraits/orchard_at_dusk/witness_constable_briggs.png` | 96x96 (+192x192) | P1.1 | art/orchard_at_dusk/art_prompts.md#26--pt_constable_briggs |
| pt_ned_sowerby | portrait | `art/ui/portraits/orchard_at_dusk/witness_ned_sowerby.png` | 96x96 (+192x192) | P1.1 | art/orchard_at_dusk/art_prompts.md#27--pt_ned_sowerby |
| pt_martha_ainsworth | portrait | `art/ui/portraits/orchard_at_dusk/witness_martha_ainsworth.png` | 96x96 (+192x192) | P1.1 | art/orchard_at_dusk/art_prompts.md#28--pt_martha_ainsworth |
| bf_orchard_at_dusk | briefing | `art/ui/cinematics/briefing_orchard_at_dusk.png` | 480x480 | P2.1 | art/orchard_at_dusk/art_prompts.md#31--bf_orchard_at_dusk |
| vc_correct_thomas_crale | verdict_card | `art/ui/cinematics/orchard_at_dusk_verdict_correct_thomas_crale.png` | 480x480 | P2.2 | art/orchard_at_dusk/art_prompts.md#41--vc_correct_thomas_crale |
| vc_partial_correct | verdict_card | `art/ui/cinematics/orchard_at_dusk_verdict_partial_correct.png` | 480x480 | P2.2 | art/orchard_at_dusk/art_prompts.md#42--vc_partial_correct |
| vc_accomplice_found | verdict_card | `art/ui/cinematics/orchard_at_dusk_verdict_accomplice_found.png` | 480x480 | P2.2 | art/orchard_at_dusk/art_prompts.md#43--vc_accomplice_found |
| vc_framed_suspect | verdict_card | `art/ui/cinematics/orchard_at_dusk_verdict_framed_suspect.png` | 480x480 | P2.2 | art/orchard_at_dusk/art_prompts.md#44--vc_framed_suspect |
| vc_motive_only_confession | verdict_card | `art/ui/cinematics/orchard_at_dusk_verdict_motive_only_confession.png` | 480x480 | P2.2 | art/orchard_at_dusk/art_prompts.md#45--vc_motive_only_confession |
| vc_late_revelation | verdict_card | `art/ui/cinematics/orchard_at_dusk_verdict_late_revelation.png` | 480x480 | P2.2 | art/orchard_at_dusk/art_prompts.md#46--vc_late_revelation |
| vc_near_miss | verdict_card | `art/ui/cinematics/orchard_at_dusk_verdict_near_miss.png` | 480x480 | P2.2 | art/orchard_at_dusk/art_prompts.md#47--vc_near_miss |
| vc_cold_trail | verdict_card | `art/ui/cinematics/orchard_at_dusk_verdict_cold_trail.png` | 480x480 | P2.2 | art/orchard_at_dusk/art_prompts.md#48--vc_cold_trail |
| vc_red_herring_trap | verdict_card | `art/ui/cinematics/orchard_at_dusk_verdict_red_herring_trap.png` | 480x480 | P2.2 | art/orchard_at_dusk/art_prompts.md#49--vc_red_herring_trap |
| vc_wrong_template | verdict_card | `art/ui/cinematics/orchard_at_dusk_verdict_wrong_<suspect>.png` (3 renders) | 480x480 | P2.2 | art/orchard_at_dusk/art_prompts.md#410--vc_wrong_template |
| ui_apple_stalk | ui_ornament | `art/ui/ornaments/orchard_at_dusk_apple_stalk.png` | 32x32 | P0 | art/orchard_at_dusk/art_prompts.md#51--ui_apple_stalk |
| ui_cider_press_cog | ui_ornament | `art/ui/ornaments/orchard_at_dusk_cider_press_cog.png` | 480x16 | P0 | art/orchard_at_dusk/art_prompts.md#52--ui_cider_press_cog |
| ui_parish_register_corner | ui_ornament | `art/ui/ornaments/orchard_at_dusk_parish_register_corner.png` | 16x16 | P0 | art/orchard_at_dusk/art_prompts.md#53--ui_parish_register_corner |
