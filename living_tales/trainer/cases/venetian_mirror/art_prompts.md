# The Venetian Mirror — Diffusion Prompt Sheet

Case: `venetian_mirror` · Authored 2026-06-13 by lt-art agent
Output targets follow the IMAGES.md catalogue conventions. Every block below is
a complete paste-able prompt for SDXL / Flux / Midjourney. Asset status is
audited against `art/venetian_mirror/` and `art/ui/` as of this date.

**Audit note:** `art/venetian_mirror/direct_pixel_art_v1/` contains 10 finished
320×320 backdrops, but they use descriptive scene names
(`grand_gallery`, `balcony_fall_zone`, `restoration_chamber`, …), not the
canonical LOCATION-token filenames. Every canonical filename below is therefore
MISSING; where a near-equivalent proxy exists it is named so you can either
rename/re-crop the proxy or regenerate from the prompt. All portrait, briefing,
verdict, and hero-object assets are MISSING (`art/ui/portraits/`,
`art/ui/cinematics/`, `art/ui/ornaments/` contain no venetian_mirror files).

---

## Style Spine

Every prompt in this sheet inherits this spine. Paste it after the
scene-specific text of each block (it is already inlined in each block; this
section is the reference of record).

> Venice on the last night of Carnevale, circa 1900. Palazzo Contarini: pink
> Istrian stone over black canal water, carnival lanterns burned low, gilt
> frames and clouded mirrors, aged plaster, velvet and silk, wet flagstone.
> Light sources are always diegetic — candle, oil lantern, moonlight on water —
> never electric. Painterly composition first, then rendered down to crisp
> 16-bit pixel art: hard 1-px edges, dithered gradients, limited palette,
> no anti-aliasing. Medium-wide detective POV, eye height, as if the
> investigator just stepped into the room. Mood: Return of the Obra Dinn ×
> Kentucky Route Zero — forensic stillness with theatrical shadow.

**Shared NEGATIVE prompt (append to every generation):**

> text, letters, captions, signage, watermark, signature, UI elements, modern
> objects, electric lights, wristwatches, cars, plastic, anime, cel shading,
> chibi, anti-aliasing, soft blur, bokeh, depth of field, photorealism, neon
> colors, oversaturation, lens flare, frame border

## Palette

Lock these hexes with an indexed-color pass after generation.

| Role | Hex | Notes |
|---|---|---|
| Deep canal night | `#0E1B26` | darkest value; water, shadow mass, sky |
| Lagoon teal | `#1F5C5B` | mid-shadow on water, mirror glass, mist |
| Tarnished gold | `#B08A3F` | gilt frames, lantern brass, project-wide BRASS |
| Candle ivory | `#E8DCC0` | highlights, candlelight, mask silk, project CREAM |
| Oxblood | `#6E2430` | velvet drapes, wax seals, carnival domino cloaks |
| Faded rose stone | `#C08E7E` | palazzo facade, aged plaster interiors |
| Varnish amber | `#C9913B` | lantern glow falloff, fresh varnish, candle halos |
| Mirror silver-grey | `#93A8AA` | clouded mirror glass, moonlit stone, fog |

Accent rule: oxblood and tarnished gold never exceed ~15% of any frame; the
image should read teal-and-night first, gold second, blood last.

---

## 1. Location Backdrops

One per LOCATION token in `dimensions.json`. 320×320, **no people in frame**
(the picture is sacred; presence is narrated, not drawn). Generate at
1280×1280, nearest-neighbor downscale to 320×320.
Target path: `art/venetian_mirror/direct_pixel_art_v1/pixel_320x320/`

### 1.1 — bd_palazzo_contarini — `location:palazzo_contarini`

**File:** `venetian_mirror_palazzo_contarini_pixel_320x320_v01.png` — **MISSING**
(proxy EXISTS: `venetian_mirror_palazzo_canal_exterior_pixel_320x320_v01.png`)

> 16-bit pixel art, 320x320, Venetian palazzo facade of pink Istrian stone
> rising directly from black canal water at night, three tiers of pointed
> Gothic arch windows, a few lit amber from within, carnival paper lanterns
> strung along the piano nobile burned down to stubs, striped mooring poles
> leaning in the foreground water, an empty gondola tied at the water-gate,
> reflections of lantern light broken into horizontal dithered ribbons on the
> canal, thin mist at the waterline, no people, medium-wide view from across
> the canal at gondola height, palette of deep canal night #0E1B26, lagoon
> teal #1F5C5B, faded rose stone #C08E7E, tarnished gold #B08A3F, candle ivory
> #E8DCC0, hard pixel edges, dithered gradients, Obra Dinn × Kentucky Route
> Zero mood, no text

### 1.2 — bd_main_balcony — `location:main_balcony`

**File:** `venetian_mirror_main_balcony_pixel_320x320_v01.png` — **MISSING**
(partial proxy EXISTS: `venetian_mirror_balcony_fall_zone_pixel_320x320_v02.png`,
which frames the courtyard below rather than the balcony itself)

> 16-bit pixel art, 320x320, stone balcony of a Venetian palazzo at night seen
> from just inside the open balcony door, carved stone balustrade with one
> baluster section visibly scored and cracked near its base, deep chisel marks
> in the stone, a single guttering oil lantern hooked on the door frame
> casting long amber light across the balcony floor, beyond the railing the
> dark drop to a courtyard and the far rooftops of Venice under a thin moon,
> a scrap of pale silk caught on the broken stone, no people, composition
> looking outward and slightly down so the damaged railing sits at lower
> third, palette deep canal night #0E1B26, mirror silver-grey #93A8AA,
> tarnished gold #B08A3F, candle ivory #E8DCC0, oxblood #6E2430 accent,
> hard 1-px edges, dithering, no anti-aliasing, no text

### 1.3 — bd_mirror_gallery — `location:mirror_gallery`

**File:** `venetian_mirror_mirror_gallery_pixel_320x320_v01.png` — **MISSING**
(proxy EXISTS: `venetian_mirror_grand_gallery_pixel_320x320_v02.png`)

> 16-bit pixel art, 320x320, long mirror gallery on the piano nobile of a
> Venetian palazzo at night, east wall hung with a receding row of oil
> paintings in heavy tarnished gilt frames, each with a small ivory provenance
> card beneath it, west wall lined with tall clouded Murano mirrors reflecting
> the paintings and the candlelight back in dimmer teal-grey, a single
> candelabrum burning halfway down the room, terrazzo floor catching the
> candle glow in dithered pools, one mirror near the foreground bearing a long
> diagonal crack, no people, one-point perspective straight down the gallery,
> vanishing point slightly off-centre, palette deep canal night #0E1B26,
> lagoon teal #1F5C5B, tarnished gold #B08A3F, candle ivory #E8DCC0, mirror
> silver-grey #93A8AA, crisp pixel edges, 16-bit dithering, Obra Dinn
> forensic stillness, no text on the cards, no legible writing

### 1.4 — bd_canal_entrance — `location:canal_entrance`

**File:** `venetian_mirror_canal_entrance_pixel_320x320_v01.png` — **MISSING**
(proxy EXISTS: `venetian_mirror_bridge_and_canal_approach_pixel_320x320_v02.png`;
second candidate: `venetian_mirror_service_landing_or_canal_side_rear_edge_pixel_320x320_v02.png`)

> 16-bit pixel art, 320x320, water-gate entrance of a Venetian palazzo at
> night seen from the canal steps, low stone arch opening directly onto black
> water, green algae line at the waterline, wrought-iron gate standing half
> open, a moored gondola nosing against worn wooden mooring posts, one oil
> lantern in a glass cage above the arch throwing amber light down wet stone
> steps, a white silk carnival mask abandoned face-up on the lowest dry step,
> mist drifting in from the canal, no people, medium-wide composition with the
> arch framing deep darkness beyond, palette deep canal night #0E1B26, lagoon
> teal #1F5C5B, varnish amber #C9913B, candle ivory #E8DCC0, faded rose stone
> #C08E7E, hard pixel edges, heavy dithered water reflections, no text

### 1.5 — bd_studio_room — `location:studio_room`

**File:** `venetian_mirror_studio_room_pixel_320x320_v01.png` — **MISSING**
(proxy EXISTS: `venetian_mirror_restoration_chamber_pixel_320x320_v02.png`)

> 16-bit pixel art, 320x320, art restorer's studio on the third floor of a
> Venetian palazzo at night, a canvas on a wooden easel turned three-quarters
> away from the viewer, work table crowded with glass jars of pigment, rags,
> a brass-handled magnifier and a row of brushes still wet and dark at the
> tips, an open notebook on the desk with its pages turned away, a small
> spirit lamp burning low, one tall window showing rooftops and a sliver of
> canal far below, sharp smell of varnish suggested by amber haze around the
> lamp, no people, composition from the doorway at eye height with the easel
> dominating the left third, palette deep canal night #0E1B26, varnish amber
> #C9913B, tarnished gold #B08A3F, candle ivory #E8DCC0, oxblood #6E2430
> accent in a pigment jar, crisp 1-px edges, dithering, no legible writing,
> no text

### 1.6 — bd_servants_stair — `location:servants_stair`

**File:** `venetian_mirror_servants_stair_pixel_320x320_v01.png` — **MISSING**
(proxy EXISTS: `venetian_mirror_private_corridor_or_stair_pixel_320x320_v02.png`)

> 16-bit pixel art, 320x320, narrow servants' staircase inside a Venetian
> palazzo at night, steep worn stone steps spiraling down between rough
> plaster walls stained with damp, a heavy wooden door at the landing bolted
> from the inside with a thrown iron bolt clearly visible, a single tallow
> candle in a wall niche throwing the bannister shadow long up the stair,
> a ring of old keys hanging from a nail by the door, scuffed footprints in
> the dust on the third step, no people, claustrophobic vertical composition
> looking down the stairwell from the upper landing, palette deep canal night
> #0E1B26, faded rose stone #C08E7E, mirror silver-grey #93A8AA, candle ivory
> #E8DCC0, varnish amber #C9913B, hard pixel edges, coarse dithering for the
> plaster, no text

### 1.7 — bd_courtyard — `location:courtyard`

**File:** `venetian_mirror_courtyard_pixel_320x320_v01.png` — **MISSING**
(proxy EXISTS: `venetian_mirror_balcony_fall_zone_pixel_320x320_v02.png`)

> 16-bit pixel art, 320x320, enclosed courtyard of a Venetian palazzo at first
> grey light before dawn, wet flagstones, a carved stone wellhead at centre,
> the main balcony visible three floors above with its balustrade broken at
> one point, a chalk outline-free bare patch of flagstone where something
> recently lay, an open leather notebook resting on the stones beside it with
> pages stirring, burned-out carnival lanterns sagging on a line strung
> across the courtyard, one lit window high up, no people, composition from
> the courtyard corner looking up so both flagstones and broken railing read
> in one frame, palette deep canal night #0E1B26 giving way to mirror
> silver-grey #93A8AA dawn, faded rose stone #C08E7E, tarnished gold #B08A3F,
> candle ivory #E8DCC0, crisp pixel edges, dithered dawn gradient in the sky,
> no text, no body in frame

### 1.8 — bd_private_salon — `location:private_salon`

**File:** `venetian_mirror_private_salon_pixel_320x320_v01.png` — **MISSING**
(proxy EXISTS: `venetian_mirror_reception_salon_pixel_320x320_v02.png`)

> 16-bit pixel art, 320x320, small private salon off the mirror gallery of a
> Venetian palazzo at night, two oxblood velvet armchairs angled toward each
> other beside a marble console table, a leather-bound auction catalogue and
> two empty coffee cups on the console, heavy brocade curtains drawn over the
> window with a thin line of moonlight escaping, a small Murano glass
> chandelier unlit, one candle burning in a silver stick, a discarded white
> carnival domino mask on the seat of one chair, no people, intimate
> medium-wide composition from the doorway, conversation just ended, palette
> deep canal night #0E1B26, oxblood #6E2430, tarnished gold #B08A3F, candle
> ivory #E8DCC0, lagoon teal #1F5C5B in the shadowed corners, hard 1-px
> edges, fine dithering on velvet, no legible writing, no text

---

## 2. NPC Portraits

One per PRESENCE NPC (7 suspects + 5 witnesses). Deliver at **96×96** and
**192×192** (generate once at 768×768, downscale to both). Tintype/albumen
plate framing: head and shoulders, subject looking slightly off camera,
sepia-toward-teal toning to sit in the case palette, vignetted plate edges,
period costume circa 1900 Venice. Visual character is taken from VOICES.md.
Target path: `art/ui/portraits/venetian_mirror/`

**Shared portrait spine (append to each):**

> tintype photograph framing, head and shoulders, 16-bit pixel art portrait,
> dark plate vignette at corners, sepia shifted toward lagoon teal #1F5C5B
> and candle ivory #E8DCC0, single lantern key light, hard pixel edges, no
> anti-aliasing, circa 1900 Venetian dress, looking slightly off camera,
> plain dark background, no text

### 2.1 — pt_morvaine — `presence:with_countess_morvaine`

**Files:** `suspect_morvaine.png` (96×96 + 192×192) — **MISSING**

> portrait of an aristocratic European countess in her late fifties, silver
> hair dressed high, long pale kid gloves drawn straight at the wrist, jet
> choker, dark watered-silk gown, composure absolute, the faint held smile of
> a woman who has rehearsed her innocence, eyes cold and appraising as if
> reading a provenance card, one gloved hand just visible adjusting the
> opposite cuff + portrait spine above

### 2.2 — pt_bassi — `presence:with_carlo_bassi`

**Files:** `suspect_bassi.png` (96×96 + 192×192) — **MISSING**

> portrait of a handsome Italian man in his late thirties, dark oiled hair,
> theatrical half-smile arriving before the question does, white silk
> carnival mask pushed up onto his forehead, evening tailcoat with a gardenia
> wilting in the buttonhole, one glove on and the bare hand holding its torn
> twin loosely, charm thickened into performance, eyes flicking just past the
> viewer toward a door + portrait spine above

### 2.3 — pt_winter — `presence:with_dr_klaus_winter`

**Files:** `suspect_winter.png` (96×96 + 192×192) — **MISSING**

> portrait of a precise German-Austrian appraiser in his fifties, wire
> spectacles, close-trimmed grey beard, high stiff collar and sober dark coat,
> a small black notebook held against the heel of one hand mid-tap, expression
> of clinical patience with no warmth and no malice, faint smell of varnish
> almost visible in the amber rim light, the face of a man who reads pigment
> the way others read faces + portrait spine above

### 2.4 — pt_rizzoli — `presence:with_elena_rizzoli`

**Files:** `suspect_rizzoli.png` (96×96 + 192×192) — **MISSING**

> portrait of a polished Italian gallery manager in her late thirties, dark
> hair pinned with a tortoiseshell comb, tailored dove-grey jacket over a
> high lace collar, the bright accommodating smile of someone who has sold
> the same painting three times, a slim leather catalogue held against her
> chest like a shield, eyes that brighten under pressure instead of cracking
> + portrait spine above

### 2.5 — pt_dandolo — `presence:with_marco_dandolo`

**Files:** `suspect_dandolo.png` (96×96 + 192×192) — **MISSING**

> portrait of a guarded Venetian man in his forties, weathered face, heavy
> brows, working man's dark wool coat with the collar up against the night
> damp, shoulders squared and closed, jaw set hard at the end of a short
> sentence, one hand jammed in a coat pocket concealing something soft,
> the defensive stillness of a man caught where he should not be and
> refusing to say why + portrait spine above

### 2.6 — pt_pelosi — `presence:with_signora_pelosi`

**Files:** `suspect_pelosi.png` (96×96 + 192×192) — **MISSING**

> portrait of an elderly Venetian housekeeper, grey hair under a plain dark
> cap, black household dress with a white apron, hands clasped flat at the
> apron pocket where a heavy bronze key makes a small visible weight against
> the cloth, expression gone deliberately still, thirty years of household
> discretion behind the eyes, the patient gravity of a woman who knows every
> door and has not unlocked them all + portrait spine above

### 2.7 — pt_bruno — `presence:with_inspector_bruno`

**Files:** `suspect_bruno.png` (96×96 + 192×192) — **MISSING**

> portrait of a weary Italian police inspector in his fifties, cultural
> crimes division, rumpled overcoat over a correct dark suit, heavy
> moustache, deep-set eyes with procedural courtesy and a slow professional
> satisfaction underneath, a thin closed folder tucked under one arm, the
> face of a man who has waited six years for a single mistake and arrived
> at dawn to collect it + portrait spine above

### 2.8 — pt_gondolier — `presence:with_gondolier`

**Files:** `witness_gondolier.png` (96×96 + 192×192) — **MISSING**

> portrait of a Venetian gondolier in his fifties, sun-creased face, dark
> ribboned straw hat, striped jersey under a short wool jacket, oar resting
> across visible at the frame edge, the easy unhurried gaze of a man who has
> brought guests to the same water-gate for twenty years and remembers every
> face that paid and every one that did not, nothing to hide and nothing to
> volunteer + portrait spine above

### 2.9 — pt_maid — `presence:with_palazzo_maid`

**Files:** `witness_palazzo_maid.png` (96×96 + 192×192) — **MISSING**

> portrait of a young Venetian maid barely twenty, pale and tired, plain
> grey service dress with white collar, hair escaping its pins after a night
> on her feet, eyes slightly displaced as if still seeing the courtyard at
> dawn, fingers caught mid-gesture folding the corner of her apron, the
> quiet shock of the one who found the body not yet settled + portrait spine
> above

### 2.10 — pt_nightguard — `presence:with_night_guard`

**Files:** `witness_night_guard.png` (96×96 + 192×192) — **MISSING**

> portrait of a stolid night watchman in his sixties, heavy dark uniform
> coat with dull brass buttons, lantern hook at his belt, flat uninflected
> expression of a man whose job is to walk a circuit and report nothing,
> eyes fixed level and deliberately not upward, weather-reddened cheeks,
> the unshakeable calm of a man who, by his own admission, never looked at
> the balcony + portrait spine above

### 2.11 — pt_artdealer — `presence:with_art_dealer`

**Files:** `witness_art_dealer.png` (96×96 + 192×192) — **MISSING**

> portrait of a Zurich art dealer in his late forties, impeccable charcoal
> travelling suit, neutral transactional expression, pale eyes that price
> what they rest on, one hand raised mid-gesture adjusting a gold cufflink
> as though resetting a mechanism before answering, lawyer-careful mouth,
> a man who flew in for carnival and intends to leave with the matter quietly
> closed + portrait spine above

### 2.12 — pt_canalboatman — `presence:with_canal_boatman`

**Files:** `witness_canal_boatman.png` (96×96 + 192×192) — **MISSING**

> portrait of a Venetian cargo boatman in his forties, oilskin cape over a
> rough jumper, knit cap, faint amused half-smile of a man who passes the
> palazzo on the water at all hours and notices what the household does not,
> eyes crinkled with the patience of someone who has been waiting to be
> asked, lantern light off black water reflected under his chin + portrait
> spine above

---

## 3. Briefing Card

### 3.1 — br_venetian_mirror

**File:** `art/ui/cinematics/briefing_venetian_mirror.png` (480×480) — **MISSING**

Painterly, NOT pixel art — this is the cinematic establishing shot shown
before the pixel-art game begins.

> oil painting, painterly impasto, Palazzo Contarini on the Grand Canal on
> the night of Carnevale circa 1900, pink stone facade rising from black
> water, carnival lanterns strung along the piano nobile burning low, masked
> guests arriving by gondola at the water-gate, their lanterns doubling in
> the canal, one high window lit amber on the third floor where a restorer
> works late, thin mist on the water, a moonless sky pressing down, dramatic
> chiaroscuro, the palazzo beautiful and false as a painted backdrop, palette
> of deep canal night #0E1B26, lagoon teal #1F5C5B, tarnished gold #B08A3F,
> candle ivory #E8DCC0, oxblood #6E2430 in the gondola felze and guest
> cloaks, 480x480, cinematic, atmospheric, no text, no watermark

---

## 4. Verdict Cards

Painterly 480×480, one per ending type, used as ending-screen backdrops.
Venetian metaphor language: masks, mirrors, water. No figures' faces
identifiable; these are emblematic, not narrative.
Target path: `art/ui/cinematics/`

### 4.1 — vc_all_strong — `verdict_all_strong.png` — **MISSING**

> oil painting, painterly, a Venetian carnival mask of white silk lying
> face-up on a long table in the mirror gallery at dawn, removed at last,
> behind it a tall Murano mirror reflecting the room truly for the first
> time — paintings, candlestubs, the open balcony door — cold honest morning
> light flooding the gallery and washing the candle glow out, every gilt
> frame casting a precise shadow, the moment a six-year lie loses its
> reflection, dramatic but resolved, palette lagoon teal #1F5C5B, candle
> ivory #E8DCC0, tarnished gold #B08A3F, mirror silver-grey #93A8AA, 480x480,
> no text, no faces

### 4.2 — vc_lucky_guess — `verdict_lucky_guess.png` — **MISSING**

> oil painting, painterly, a gloved hand reflected in a cracked Venetian
> mirror at night, the crack splitting the reflection so the hand appears
> twice and neither image quite aligns, candlelight from off-frame, the
> accusation true but the proof divided, a white mask hanging by its ribbon
> from the mirror's gilt frame, unsettled composition slightly off-balance,
> palette deep canal night #0E1B26, varnish amber #C9913B, mirror silver-grey
> #93A8AA, candle ivory #E8DCC0, 480x480, dramatic chiaroscuro, no text, no
> identifiable face

### 4.3 — vc_wrong_accusation — `verdict_wrong_accusation.png` — **MISSING**

> oil painting, painterly, an empty gondola being poled away from the
> palazzo water-gate at night carrying a single white carnival mask on its
> seat, the wrong guest taken, while behind in the lit piano nobile windows
> the reception glitters on undisturbed and fourteen gilt frames glow
> through the glass, the canal water black and smooth, closing over
> everything, palette deep canal night #0E1B26, lagoon teal #1F5C5B,
> tarnished gold #B08A3F glowing in the windows, oxblood #6E2430 in the
> gondola cushion, 480x480, melancholy chiaroscuro, no text, no faces

### 4.4 — vc_cold_case — `verdict_cold_case.png` — **MISSING**

> oil painting, painterly, the mirror gallery of a Venetian palazzo shuttered
> for the season, dust sheets over the furniture like a congregation of
> ghosts, fourteen paintings still hanging in their gilt frames each
> reflecting nothing true, one cracked mirror left unrepaired catching the
> only light — a thin blade of grey day through closed shutters — the single
> honest flaw in a room of beautiful lies, fog pressing at the windows,
> palette mirror silver-grey #93A8AA, deep canal night #0E1B26, faded rose
> stone #C08E7E, muted tarnished gold #B08A3F, 480x480, still, cold,
> atmospheric, no text, no figures

### 4.5 — vc_partial — `verdict_partial.png` — **MISSING**

> oil painting, painterly, a Venetian mirror half-veiled by a fallen drape of
> oxblood velvet, the exposed half reflecting a candlelit gallery wall of
> gilt-framed paintings, the covered half holding back the rest of the room,
> a torn silk glove resting on the marble console beneath the mirror, half
> the truth in the glass and half still under cloth, water-light from the
> canal moving faintly on the ceiling, palette oxblood #6E2430, tarnished
> gold #B08A3F, lagoon teal #1F5C5B, candle ivory #E8DCC0, deep canal night
> #0E1B26, 480x480, dramatic chiaroscuro, no text, no faces

---

## 5. Hero Objects

Six load-bearing OBJECT_FOCUS tokens, chosen for attractor weight and beat
coverage: the title object, the how-evidence chain (railing, pigment, canal
key) and the why-evidence chain (forged canvas, restoration notes). 64×64
transparent-background pixel art, single object centered, evidence-card
inset style. Generate at 512×512, nearest-neighbor downscale.
Target path: `art/ui/ornaments/venetian_mirror/`

### 5.1 — ho_cracked_mirror — `object:cracked_mirror`

**File:** `object_cracked_mirror.png` (64×64) — **MISSING**

> 64x64 pixel art, single object centered on transparent background, an
> ornate Venetian hand mirror with tarnished gold rococo frame, the glass
> split by one long diagonal crack, each half reflecting a slightly
> different teal, 16-bit era, hard 1-px edges, palette tarnished gold
> #B08A3F, mirror silver-grey #93A8AA, lagoon teal #1F5C5B, no shadow,
> no text

### 5.2 — ho_forged_canvas — `object:forged_canvas`

**File:** `object_forged_canvas.png` (64×64) — **MISSING**

> 64x64 pixel art, single object centered on transparent background, a small
> old-master canvas in a heavy gilt frame seen at a slight angle, one corner
> of the canvas lifted to reveal bright new white linen beneath the
> artificially aged surface, craquelure pattern dithered across the paint,
> 16-bit era, hard pixel edges, palette varnish amber #C9913B, tarnished
> gold #B08A3F, candle ivory #E8DCC0, deep canal night #0E1B26, no shadow,
> no text, no legible image inside the painting

### 5.3 — ho_restoration_notes — `object:restoration_notes`

**File:** `object_restoration_notes.png` (64×64) — **MISSING**

> 64x64 pixel art, single object centered on transparent background, a
> restorer's leather field notebook lying open, pages dense with illegible
> pixel-scribble notes and one small pasted pigment swatch, a fine brush
> resting in the gutter with a wet dark tip, corner of one page torn away,
> 16-bit era, hard 1-px edges, palette candle ivory #E8DCC0, oxblood #6E2430
> leather, varnish amber #C9913B, no shadow, no legible letters, no text

### 5.4 — ho_pigment_sample — `object:pigment_sample`

**File:** `object_pigment_sample.png` (64×64) — **MISSING**

> 64x64 pixel art, single object centered on transparent background, a small
> corked glass vial of cadmium yellow pigment powder beside a tiny paint
> flake on a square of white blotting paper, a brass loupe leaning against
> the vial, the yellow conspicuously too bright and too modern against the
> muted case palette, 16-bit era, hard pixel edges, palette varnish amber
> #C9913B, candle ivory #E8DCC0, tarnished gold #B08A3F, deep canal night
> #0E1B26 outline, no shadow, no text

### 5.5 — ho_canal_key — `object:canal_key`

**File:** `object_canal_key.png` (64×64) — **MISSING**

> 64x64 pixel art, single object centered on transparent background, a heavy
> bronze water-gate key with a worn ring bow and double-cut bit, green-black
> verdigris in the recesses, a short loop of apron cord still knotted through
> the bow, faint wet sheen along one edge as if recently carried beside the
> canal, 16-bit era, hard 1-px edges, palette tarnished gold #B08A3F,
> lagoon teal #1F5C5B verdigris, deep canal night #0E1B26, no shadow, no text

### 5.6 — ho_balcony_railing — `object:balcony_railing`

**File:** `object_balcony_railing.png` (64×64) — **MISSING**

> 64x64 pixel art, single object centered on transparent background, a
> broken section of carved stone baluster shown as an evidence fragment,
> deep parallel chisel score marks at the break point, a wisp of pale silk
> fibre caught in the scored groove, raw stone bright against the weathered
> outer surface, 16-bit era, hard pixel edges, palette mirror silver-grey
> #93A8AA, faded rose stone #C08E7E, candle ivory #E8DCC0 silk accent,
> deep canal night #0E1B26 outline, no shadow, no text

---

## Generation Notes

- **Render 4×, downscale nearest-neighbor.** 320×320 backdrops → generate
  1280×1280; portraits → 768×768 down to 192×192 then 96×96; hero objects →
  512×512 down to 64×64; verdict/briefing cards are painterly and may be
  generated at native 960×960 → 480×480 bicubic (painterly assets do not need
  crisp pixel edges).
- **Palette lock.** After generation, run an indexed-color pass against the
  8-hex table above plus pure black; this keeps the case visually coherent
  with the existing `direct_pixel_art_v1` set and the project BRASS/CREAM
  constants.
- **Seeds.** Sweep seeds in blocks per section: backdrops 4100–4199,
  portraits 4200–4299, briefing 4300–4310, verdicts 4320–4360, hero objects
  4400–4450. Generate v01–v03 per asset, pick one, keep the canonical name.
- **PROVENANCE.txt.** Record every kept image as
  `<filename> | <model> | <seed> | <full prompt>` in
  `art/venetian_mirror/PROVENANCE.txt` (and `art/ui/<subdir>/PROVENANCE.txt`
  for UI-side assets) so any asset can be re-rolled deterministically.
- **Model tips.** SDXL: add `pixel art, 16-bit` LoRA if available and keep
  CFG 6–7; Flux: the prompts are long — Flux handles them natively, keep
  guidance ~3.5; Midjourney: append `--style raw --no text,watermark` and
  move the NEGATIVE list into `--no`. For tintype portraits on SDXL, a low
  denoise img2img pass over a plain vignette plate improves frame
  consistency across all 12 NPCs.
- **Existing proxies.** Seven of eight locations have near-equivalent
  finished backdrops under descriptive names (see section 1). Cheapest path
  to a fully wired case: copy/rename the proxy into the canonical filename,
  then regenerate only `main_balcony` (no true balcony-POV proxy exists) and
  any proxy that drifts from the LOCATION token's meaning.
