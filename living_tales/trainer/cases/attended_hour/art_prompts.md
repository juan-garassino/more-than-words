# attended_hour — Diffusion Prompt Sheet (lt-art)

Case: **The Attended Hour** — Harold Stroud found unresponsive in bed three of
Briar Clinic's private cardiac ward; monitor silenced, IV disconnected, two
drugs given within the same hour. Generated 2026-06-13 from `cases/attended_hour.json`,
`trainer/cases/attended_hour/{dimensions.json,VOICES.md,phrases.json}` and the
`art/attended_hour/` inventory.

**Asset status legend** — EXISTS: a v01 file is already on disk at the canonical
path (re-roll only as v02 if quality demands). MISSING: net-new commission.

---

## Style Spine

Briar Clinic is **a converted Victorian house refitted as a private cardiac
ward in the slow, fluorescent style of a 1970s clinical conversion**. The
visual identity of this case is that collision: gas-era architecture under
strip lighting — ceiling roses above fluorescent battens, linoleum laid over
creaking Victorian boards, enamel and chrome trolleys parked against walnut
wainscoting, a coded dispensary door cut into a panelled wall. Note: this
deliberately swaps the "pure Victorian infirmary / candlelight" default for
what the briefing actually describes; keep era props capped at **circa 1978**
(CRT-green cardiac monitors, carbonless prescription pads, magnetic-stripe
keycards are all in-world — anything later is not).

Every prompt below shares this treatment:

- **Render painterly first, pixel second**: generate as a painterly, lightly
  textured illustration, then downscale to crisp 16-bit pixel art
  (nearest-neighbor; see Generation Notes). Obra Dinn's forensic stillness ×
  Kentucky Route Zero's institutional melancholy.
- **Lighting**: cold fluorescent pallor in clinical zones, with one warm
  counterpoint per scene (a desk lamp, a corridor sconce, the amber of a
  streetlamp through a sash window). The hour is 21:00–dawn; the unattended
  half of the night should feel longer than the attended hour.
- **Camera**: medium-wide detective POV, eye height, slightly off-axis —
  the view of someone who has just stepped in and stopped.
- **Composition rule for backdrops**: no people in frame, ever. Rooms hold
  the evidence of occupation (a chart left open, a cooling cup of tea, a
  curtain still swaying) but never the occupant.
- **Palette discipline**: ward greens, bleached linen, iodine browns,
  night-shift shadow, with phosphor green and crash-crimson as rationed
  accents. Hexes locked in the Palette table below.

**Shared NEGATIVE (append to every prompt):**
`text, lettering, readable writing, watermark, signature, logo, contemporary hospital equipment, flatscreen displays, computers, LED panels, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic faces, lens flare`
(For backdrops and hero objects additionally append: `people, figures, hands, faces`.)

---

## Palette

| Role | Name | Hex | Usage |
|---|---|---|---|
| Deepest shadow | Night-Shift Black | `#13181A` | unattended corridors, window glass, under-bed dark |
| Dark structure | Ward Green Deep | `#2C463C` | lower-wall paint, door frames, shadowed linoleum |
| Mid structure | Ward Green | `#4F6F5E` | upper walls, screens, painted radiators |
| Cold light | Fluorescent Pallor | `#D8E3D2` | strip-light falloff, lit linoleum, chart paper under tube light |
| Warm paper/cloth | Bleached Linen | `#EAE3CF` | bedsheets, coats, ledger pages, lampshades |
| Warm accent | Iodine Brown | `#8A572A` | walnut wainscoting, antiseptic stains, leather chairs, tea |
| Metal | Surgical Chrome | `#9FB0AE` | trolleys, kidney dishes, IV stands, lift doors |
| Period brass | Briar Brass | `#B08A3F` | door furniture, bell-pull fittings, plaque, watch chain |
| Rationed accent 1 | Phosphor Green | `#3FA86B` | cardiac monitor trace, dispensary keypad glow — one element per scene max |
| Rationed accent 2 | Crash Crimson | `#7E2B2B` | crash-trolley stripe, wax seal, complaint stamp — one element per scene max |

Quantize final pixel passes to ≤48 colors built from ramps of these ten.

---

## 1. Location Backdrops

One per LOCATION token (10; `location:none` excluded). Target filename:
`art/attended_hour/direct_pixel_art_v1/pixel_320x320/attended_hour_<loc>_pixel_320x320_v01.png`.
320×320, **no people in frame**, varied composition per room. All ten v01
files are already on disk — prompts here are the canonical re-roll source.

### 1.1 — cardiac_ward_crime_space — **EXISTS**

> 16-bit pixel art, 320x320, painterly rendered then pixel-crisp. A private
> cardiac ward at night inside a converted Victorian house: bed three in the
> foreground, sheets pulled flat and empty, a folding ward screen half-drawn
> beside it. A CRT cardiac monitor on a chrome stand, screen dark and dead, a
> single phosphor-green standby dot. Disconnected IV line hanging from its
> stand, taped end loose. Three other beds recede behind drawn curtains. One
> fluorescent batten lit at the far end of the room, a Victorian ceiling rose
> above it in shadow. Cold green-white light on linoleum, ward-green walls,
> bleached linen, deep night shadow under the beds. Medium-wide detective
> POV from the ward doorway, slightly off-axis. Obra Dinn x Kentucky Route
> Zero mood, forensic stillness, no people.
> **Negative:** text, lettering, readable writing, watermark, signature, logo, contemporary hospital equipment, flatscreen displays, computers, LED panels, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic faces, lens flare, people, figures, hands, faces

### 1.2 — doctor_office — **EXISTS**

> 16-bit pixel art, 320x320, painterly rendered then pixel-crisp. A
> consultant's office in a Victorian front room: tall sash window with
> streetlamp amber bleeding through half-closed venetian blinds, walnut desk
> with a green-shaded lamp lit. On the blotter, a thick drug interaction
> manual lying open, one page dog-eared, a pencil resting in the gutter. A
> fountain pen uncapped beside an ink-stained white coat hung on the door.
> Framed qualifications on iodine-brown panelled walls, a locked glass
> cabinet of instruments, a rotary telephone. Warm lamp pool against cold
> dark, the only warm room in the building. Medium-wide detective POV from
> just inside the door. Obra Dinn x Kentucky Route Zero mood, no people.
> **Negative:** text, lettering, readable writing, watermark, signature, logo, contemporary hospital equipment, flatscreen displays, computers, LED panels, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic faces, lens flare, people, figures, hands, faces

### 1.3 — family_waiting_room — **EXISTS**

> 16-bit pixel art, 320x320, painterly rendered then pixel-crisp. A family
> waiting room in a converted Victorian parlour: a row of mismatched vinyl
> and leather chairs along a wainscoted wall, a low table with out-of-date
> magazines squared too neatly, an ashtray with a single stubbed cigarette.
> A cold tea cup on the windowsill. Heavy curtains parted on black night
> glass. One wall sconce lit warm; a fluorescent tube dark overhead. A
> visitor-log lectern by the inner door, pen on a chain, one page corner
> folded. Dropped staff badge half-visible under a chair. The room of people
> who wait for news. Wide composition, frontal symmetry slightly broken,
> detective POV. Obra Dinn x Kentucky Route Zero mood, no people.
> **Negative:** text, lettering, readable writing, watermark, signature, logo, contemporary hospital equipment, flatscreen displays, computers, LED panels, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic faces, lens flare, people, figures, hands, faces

### 1.4 — hospital_exterior — **EXISTS**

> 16-bit pixel art, 320x320, painterly rendered then pixel-crisp. The
> forecourt of Briar Clinic just before dawn: a tall Victorian villa, bay
> windows and slate gables, refitted as a private clinic — a discreet brass
> plaque beside the door, an electric porch light replacing the old gas
> bracket. Gravel forecourt with a small car park to one side: three parked
> cars, frost on two windscreens, none on the third. An ambulance bay
> marked in faded paint, empty. One upstairs window lit cold fluorescent
> green-white against the warm porch lamp. Dark hedges, a quiet road, the
> first grey of dawn behind the chimney stacks. Medium-wide composition from
> the gate, low three-quarter angle. Obra Dinn x Kentucky Route Zero mood,
> no people.
> **Negative:** text, lettering, readable writing, watermark, signature, logo, contemporary hospital equipment, flatscreen displays, computers, LED panels, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic faces, lens flare, people, figures, hands, faces

### 1.5 — medication_charting_area — **EXISTS**

> 16-bit pixel art, 320x320, painterly rendered then pixel-crisp. The
> medication charting alcove of a 1970s private ward: a long enamel-topped
> counter under a humming fluorescent tube, wall racks of clipboarded dosage
> charts hanging in numbered rows, one clipboard missing from its hook. A
> chrome syringe tray with kidney dishes and swab pots, two empty slots in
> the vial rack. The coded dispensary door behind the counter — a panelled
> Victorian door retro-fitted with a keypad, one phosphor-green indicator
> lit. A carbonless prescription pad askew on the counter, a biro without
> its cap. Tight medium shot, counter diagonal across frame, detective POV
> leaning in. Obra Dinn x Kentucky Route Zero mood, no people.
> **Negative:** text, lettering, readable writing, watermark, signature, logo, contemporary hospital equipment, flatscreen displays, computers, LED panels, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic faces, lens flare, people, figures, hands, faces

### 1.6 — nurse_station_vantage — **EXISTS**

> 16-bit pixel art, 320x320, painterly rendered then pixel-crisp. The nurse
> station of Briar Clinic seen as a vantage point: a curved wooden counter
> commanding the junction of two corridors, a banker's lamp lit warm over an
> open observations ledger, a fob watch on a ribbon laid beside it. A wall
> clock reading a little past nine. A board of brass bell-pull indicators —
> the old servant bells re-labelled for the four ward beds, one flag dropped.
> A cardiac monitor repeater unit with a steady phosphor-green trace. Down
> each corridor: one lit fluorescent, then darkness. Composition from behind
> the counter looking outward — the view of the person on watch. Obra Dinn x
> Kentucky Route Zero mood, no people.
> **Negative:** text, lettering, readable writing, watermark, signature, logo, contemporary hospital equipment, flatscreen displays, computers, LED panels, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic faces, lens flare, people, figures, hands, faces

### 1.7 — rear_clinical_corridor — **EXISTS**

> 16-bit pixel art, 320x320, painterly rendered then pixel-crisp. A long
> rear service corridor in a converted Victorian house: linoleum floor laid
> over uneven boards, ward-green dado below bleached-linen plaster, exposed
> conduit stapled along the cornice. Every second fluorescent tube switched
> off — pools of cold light alternating with true dark, the far end
> swallowed entirely. A parked wheelchair folded against the wall, an oxygen
> cylinder on a trolley, a fire bucket of sand. A keycard reader beside an
> unmarked door, its small light unlit. One-point perspective straight down
> the corridor, vanishing into shadow, detective POV. Obra Dinn x Kentucky
> Route Zero mood, dread by geometry, no people.
> **Negative:** text, lettering, readable writing, watermark, signature, logo, contemporary hospital equipment, flatscreen displays, computers, LED panels, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic faces, lens flare, people, figures, hands, faces

### 1.8 — reception_threshold — **EXISTS**

> 16-bit pixel art, 320x320, painterly rendered then pixel-crisp. The
> reception threshold of Briar Clinic: the original Victorian entrance hall
> — encaustic tiled floor, dark stair newel, stained-glass fanlight over the
> front door black with night — refitted with a reception desk, a perspex
> sign bracket left empty, and a wall-mounted keycard time-clock by the
> inner double doors. On the desk: a closed appointment book, a bell, a
> telephone with a coiled cord. Coat hooks with one abandoned umbrella. Cold
> fluorescent spill from the clinical wing through the inner doors' wired
> glass meets the warm dark of the old hallway. Medium-wide composition
> across the threshold line, both worlds in frame. Obra Dinn x Kentucky
> Route Zero mood, no people.
> **Negative:** text, lettering, readable writing, watermark, signature, logo, contemporary hospital equipment, flatscreen displays, computers, LED panels, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic faces, lens flare, people, figures, hands, faces

### 1.9 — service_elevator_zone — **EXISTS**

> 16-bit pixel art, 320x320, painterly rendered then pixel-crisp. The
> service-elevator alcove at the back of the clinic: a 1970s goods lift with
> scuffed chrome doors and a worn brass call button, set into a Victorian
> rear landing — bare plaster, a small high window, an old dumbwaiter hatch
> painted shut beside it. The lift's floor indicator dial glowing faint
> phosphor green, needle resting between floors. A hospital gurney parked at
> an angle, sheet folded at its foot, one wheel turned out. A mop and bucket
> drying in the corner, a caged bulkhead lamp giving the only light. Tight
> claustrophobic composition, slightly low angle, detective POV. Obra Dinn x
> Kentucky Route Zero mood, no people.
> **Negative:** text, lettering, readable writing, watermark, signature, logo, contemporary hospital equipment, flatscreen displays, computers, LED panels, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic faces, lens flare, people, figures, hands, faces

### 1.10 — staff_break_or_overnight_desk_area — **EXISTS**

> 16-bit pixel art, 320x320, painterly rendered then pixel-crisp. The staff
> break room and overnight desk of Briar Clinic: a converted Victorian back
> kitchen — old range alcove now holding a small electric kettle and a tea
> tray with three mismatched cups, one still steaming. A worn armchair with
> a folded blanket, a paraffin-era wall clock ticking past two. The night
> porter's desk by the side entrance: a handwritten entry log open under an
> anglepoise lamp, a ring of keys on a nail, a small wire-glass window onto
> the dark car park. A rota board with sliding name tiles, one tile slid to
> the wrong column. Warm pocket of lamplight in institutional dark. Cosy and
> wrong at the same time. Medium shot from the doorway. Obra Dinn x Kentucky
> Route Zero mood, no people.
> **Negative:** text, lettering, readable writing, watermark, signature, logo, contemporary hospital equipment, flatscreen displays, computers, LED panels, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic faces, lens flare, people, figures, hands, faces

---

## 2. NPC Portraits

One per PRESENCE NPC (12). Tintype-style square portraits, generate at
**192×192 master** then derive **96×96** (both shipped). Target filenames:
`art/ui/portraits/attended_hour/suspect_<id>.png` and
`art/ui/portraits/attended_hour/witness_<id>.png` (suffix `_192` for the
large size). Pose = interview demeanor from VOICES.md. Visual era: 1970s
clinical, tintype/ambrotype plate finish for cross-case consistency.
**The `art/ui/portraits/` tree does not exist yet — all 12 MISSING.**

Shared portrait treatment line (already baked into each block): *16-bit pixel
art portrait, tintype photograph framing with darkened plate edges, head and
shoulders, three-quarter view, cold fluorescent key light with warm fill,
ward-green and linen palette, 1970s British clinic, looking slightly off
camera, no text.*

### 2.1 — suspect_callum_dray (attending physician) — **MISSING**

> 16-bit pixel art portrait, tintype photograph framing with darkened plate
> edges, head and shoulders, three-quarter view. A senior consultant in his
> fifties: silver-grey hair combed exactly, half-rim spectacles, white coat
> over a knitted tie, a fountain pen clipped to the breast pocket above a
> dark ink stain spreading in the lining. Expression of rehearsed academic
> calm — jaw very slightly tightened, eyes flat and patient, the look of a
> man answering an easier version of the question. Holding a folded chart
> like a recital text. Cold fluorescent key light, warm desk-lamp fill,
> ward-green backdrop. Looking slightly off camera, no text.
> **Negative:** text, lettering, watermark, signature, logo, contemporary hospital equipment, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic skin, lens flare

### 2.2 — suspect_nurse_aldworth (evening medication round) — **MISSING**

> 16-bit pixel art portrait, tintype photograph framing with darkened plate
> edges, head and shoulders, three-quarter view. A ward nurse near sixty in
> a 1970s British uniform: starched cap, dark cape over pale blue dress, a
> fob watch pinned at the chest, hair pinned back with strands escaping
> after a fourteen-hour day. Gentle apologetic face trained on the dying,
> eyes tired and kind, a visible faint tremor suggested in the hand raised
> toward her watch. Soft, careful, never once having questioned a doctor's
> chart. Cold fluorescent key, warm fill, ward-green backdrop. Looking
> slightly off camera, no text.
> **Negative:** text, lettering, watermark, signature, logo, contemporary hospital equipment, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic skin, lens flare

### 2.3 — suspect_dr_parris (night shift) — **MISSING**

> 16-bit pixel art portrait, tintype photograph framing with darkened plate
> edges, head and shoulders, three-quarter view. A junior doctor in his
> thirties hollowed by night shifts: unshaven, dark crescents under the
> eyes, collar open beneath a creased white coat, a stethoscope still hung
> around his neck long after it was needed. Gaze angled down and held —
> fixed on the floor, not the camera — fragments of a man whose every
> sentence costs something. Posture slightly stooped, hands out of frame.
> Cold fluorescent key from above, almost no fill, corridor shadow backdrop.
> No text.
> **Negative:** text, lettering, watermark, signature, logo, contemporary hospital equipment, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic skin, lens flare

### 2.4 — suspect_owen_stroud (nephew, beneficiary) — **MISSING**

> 16-bit pixel art portrait, tintype photograph framing with darkened plate
> edges, head and shoulders, three-quarter view. A man in his late thirties
> performing grief: good wide-lapel 1970s suit a little too sharp for a
> hospital, dark tie knotted carefully, hair oiled. Smooth rehearsed
> expression of devastation that does not reach the eyes; one thumb working
> a small fold into a paper slip held at chest height — the visitor-log
> slip. Bright, over-ready, lottery-ticket nervousness underneath the
> polish. Warm waiting-room sconce key light, cold fill, leather-chair
> backdrop. Looking slightly off camera, no text.
> **Negative:** text, lettering, watermark, signature, logo, contemporary hospital equipment, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic skin, lens flare

### 2.5 — suspect_records_clerk — **MISSING**

> 16-bit pixel art portrait, tintype photograph framing with darkened plate
> edges, head and shoulders, three-quarter view. A woman in her forties in
> precise civilian office dress: high-collared blouse, cardigan, reading
> glasses on a chain, hair in an exact bun. Expression of practised
> stillness — composure gone rigid rather than calm, the rehearsed face of
> someone who has prepared for this conversation in mirrors. One hand flat
> on the steel handle of a filing cabinet at the frame's edge, knuckles
> pale. A clinic badge clipped at her breast, its signature line blank.
> Flat fluorescent office light, grey-green cabinet backdrop. Looking
> slightly off camera, no text.
> **Negative:** text, lettering, watermark, signature, logo, contemporary hospital equipment, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic skin, lens flare

### 2.6 — suspect_pharmacist_lin — **MISSING**

> 16-bit pixel art portrait, tintype photograph framing with darkened plate
> edges, head and shoulders, three-quarter view. A pharmacist in her
> thirties, methodical and quietly frightened: white dispensary coat
> buttoned to the throat, hair tied back severely, a propelling pencil
> behind one ear. She holds an inventory sheet in both hands like a
> handhold, slightly too tight, paper edge beginning to crease. Expression
> precise and apologetic at once — someone determined not to let the fear
> into her voice. Behind her, out-of-focus dispensary shelving and the
> phosphor-green dot of a keypad. Cold even fluorescent light. Looking
> slightly off camera, no text.
> **Negative:** text, lettering, watermark, signature, logo, contemporary hospital equipment, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic skin, lens flare

### 2.7 — suspect_solicitor_pike — **MISSING**

> 16-bit pixel art portrait, tintype photograph framing with darkened plate
> edges, head and shoulders, three-quarter view. A litigation solicitor in
> his fifties: charcoal three-piece suit, watch chain across the waistcoat,
> silver at the temples, a heavy leather briefcase held upright against his
> chest with one hand rotating the handle a quarter turn. Smooth
> professional charm thickened under pressure — a small, lawyerly,
> unhurried half-smile, eyes resting a half-second too long past the
> camera. Immaculate, hedged, calibrated. Warm reception lamplight key,
> stained-glass fanlight glow in the dark backdrop. No text.
> **Negative:** text, lettering, watermark, signature, logo, contemporary hospital equipment, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic skin, lens flare

### 2.8 — witness_night_porter — **MISSING**

> 16-bit pixel art portrait, tintype photograph framing with darkened plate
> edges, head and shoulders, three-quarter view. A night porter in his
> sixties at the slow end of a long shift: heavy navy porter's jacket with
> worn brass buttons, flat cap pushed back, deep seamed face, white
> stubble. Eyes sliding sideways toward an unseen car-park door rather than
> the camera — not evasive, just tired. A ring of keys on his chest, an
> anglepoise lamp's warm light from below, the wire-glass window's dark
> behind him. The face of a man with nothing to hide and no hurry to say
> so. No text.
> **Negative:** text, lettering, watermark, signature, logo, contemporary hospital equipment, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic skin, lens flare

### 2.9 — witness_ward_orderly — **MISSING**

> 16-bit pixel art portrait, tintype photograph framing with darkened plate
> edges, head and shoulders, three-quarter view. A ward orderly in his
> forties, built for moving beds and bodies: short-sleeved grey-green
> orderly's tunic, thick forearms crossed low in frame, cropped hair, a
> plain wristwatch. Expression flat and uninflected — the man who found the
> patient and reported it the same way both times he was asked. One hand's
> heel resting against his thigh. Even cold fluorescent light, ward
> curtain-track backdrop. Direct, unflinching, slightly off camera. No
> text.
> **Negative:** text, lettering, watermark, signature, logo, contemporary hospital equipment, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic skin, lens flare

### 2.10 — witness_lab_assistant (on-call resident) — **MISSING**

> 16-bit pixel art portrait, tintype photograph framing with darkened plate
> edges, head and shoulders, three-quarter view. A brisk junior clinician
> in her late twenties: short practical hair, white lab coat over a
> roll-neck, a manila file held edge-on in one hand, mid-tap against an
> unseen bench. Expression efficient and faintly impatient, consonants
> tightened — a night shaped by paperwork, an enzyme sample that never
> arrived. Eyes sharp, chin slightly raised. Cold fluorescent bench light
> from one side, lab shelving shadow backdrop. Looking slightly off camera,
> no text.
> **Negative:** text, lettering, watermark, signature, logo, contemporary hospital equipment, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic skin, lens flare

### 2.11 — witness_duty_nurse — **MISSING**

> 16-bit pixel art portrait, tintype photograph framing with darkened plate
> edges, head and shoulders, three-quarter view. A duty nurse in her
> forties: 1970s uniform with a dark cardigan over it against the night
> chill, a clipboard of observation sheets held against her chest, a
> upside-down fob watch pinned over the heart. Expression low and even,
> gone very still rather than pale; her eyes drawn aside toward an absent
> cardiac monitor, one hand making the small involuntary start of reaching
> for a pulse. The rhythm of fifteen-minute intervals in her posture. Cold
> repeater-unit glow as rim light, warm desk lamp fill. No text.
> **Negative:** text, lettering, watermark, signature, logo, contemporary hospital equipment, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic skin, lens flare

### 2.12 — witness_ambulance_driver (junior paramedic) — **MISSING**

> 16-bit pixel art portrait, tintype photograph framing with darkened plate
> edges, head and shoulders, three-quarter view. A young paramedic in his
> mid-twenties on the upward edge of his career: 1970s ambulance crew
> uniform, high-visibility tabard folded open, neat hair, alert open face
> leaning slightly toward the camera rather than away. One hand at his hip
> finding the empty clip where his radio should be. Expression clean and
> precise — call time, road conditions, arrival time — performative
> readiness without bluster. Cold dawn light from a doorway, forecourt grey
> behind him. No text.
> **Negative:** text, lettering, watermark, signature, logo, contemporary hospital equipment, modern scrubs, anime, cel shading, cartoon, anti-aliasing, soft focus blur, neon palette, photorealistic skin, lens flare

---

## 3. Briefing Card

Target: `art/ui/cinematics/briefing_attended_hour.png`, 480×480, painterly
(oil-paint look, NOT pixel art) — the cinematic establishing shot before the
pixel-art game begins. — **MISSING**

### 3.1 — briefing_attended_hour

> Painterly oil painting, 480x480, dramatic chiaroscuro, narrative
> cinematic. Briar Clinic at the attended hour: a tall Victorian villa on a
> quiet road at night, slate gables black against a bruised sky, one
> first-floor ward window glowing cold fluorescent green-white among warm
> amber neighbours — the single wrong note of light in the house. A brass
> plaque catching the porch lamp, an empty ambulance bay, three cars in the
> gravel car park with frost on only two windscreens. In the lit window, the
> faint suggestion of a ward screen and an IV stand, no figures. Wet road
> reflecting the streetlamp, bare tree, absolute stillness. Mood of a
> recovered casebook: clinical pallor inside Victorian dark, the night that
> was attended for one hour and unattended for the rest. Atmospheric,
> period-appropriate, no text overlay.
> **Negative:** text, lettering, watermark, signature, logo, pixel art, contemporary hospital equipment, flatscreen displays, anime, cartoon, neon palette, lens flare, people, figures

---

## 4. Verdict Cards

Target: `art/ui/cinematics/attended_hour_verdict_<type>.png`, 480×480,
painterly oil-paint look. Five cards, each a medical-setting metaphor for
the outcome. **All MISSING** (no `art/ui/cinematics/` tree exists).

### 4.1 — verdict_all_strong — **MISSING**

> Painterly oil painting, 480x480, dramatic chiaroscuro. The complete
> diagnosis: a consultant's desk at dawn under a strong cone of lamplight —
> the medication chart, the dispensary ledger, and the drug interaction
> manual laid out in a clean overlapping row like exhibits, the manual open
> to a pencil-marked page, a leaking fountain pen placed at the centre of
> all three as the connecting instrument. A stethoscope coiled aside,
> superseded. Dawn light breaking through the sash window behind, cold and
> exact. Every object in focus, nothing ambiguous; the composition of an
> airtight case. Victorian clinical noir, ward greens and linen against
> iodine brown, no text.
> **Negative:** text, lettering, watermark, signature, logo, pixel art, contemporary hospital equipment, anime, cartoon, neon palette, lens flare, people, figures, faces

### 4.2 — verdict_lucky_guess — **MISSING**

> Painterly oil painting, 480x480, dramatic chiaroscuro. Diagnosis by
> instinct: a single white coat hanging on a ward door under a flickering
> fluorescent tube, the name plate on the door caught at an angle that
> almost — not quite — resolves. Below it, a medication chart lying on the
> floor where it fell, pages fanned, unreadable. The accusation landed on
> the right hook but the evidence lies scattered. Half the canvas in
> confident cold light, half in unexamined shadow. Victorian clinical noir,
> ward greens and night-shift dark, a single crash-crimson stripe on a
> trolley edge at the frame's corner, no text.
> **Negative:** text, lettering, watermark, signature, logo, pixel art, contemporary hospital equipment, anime, cartoon, neon palette, lens flare, people, figures, faces

### 4.3 — verdict_wrong_accusation — **MISSING**

> Painterly oil painting, 480x480, dramatic chiaroscuro. The wrong chart
> pulled: a freshly pressed white coat on a stand in morning sunlight,
> fountain pen refilled and gleaming in its pocket — the guilty man dressed
> for rounds — while in the foreground shadow an empty patient bed is
> stripped to the mattress, a clipboard hanging at its foot wiped clean. A
> rewritten page, smooth and new, lies over an older crumpled one in a
> waste basket. Morning light flooding the wrong direction, warm and
> obscene against the cold stripped bed. Victorian clinical noir, linen
> whites against ward-green gloom, no text.
> **Negative:** text, lettering, watermark, signature, logo, pixel art, contemporary hospital equipment, anime, cartoon, neon palette, lens flare, people, figures, faces

### 4.4 — verdict_cold_case — **MISSING**

> Painterly oil painting, 480x480, dramatic chiaroscuro. The file closed: a
> records-office drawer sliding shut on a thick manila file, seen close, a
> rubber stamp and a dry inkpad beside it on the cabinet top. Above, a
> corridor of Briar Clinic receding into dark, every fluorescent tube off,
> a single dead cardiac monitor on a trolley at the corridor's end with a
> flat dark screen. Two small empty vial slots in a dispensary rack in the
> foreground shadow, never accounted for. Dust beginning in the lamplight.
> The clinic resuming its quiet rhythms around an unanswered question.
> Victorian clinical noir, deepest greens and blacks, one faint phosphor
> dot, no text.
> **Negative:** text, lettering, watermark, signature, logo, pixel art, contemporary hospital equipment, anime, cartoon, neon palette, lens flare, people, figures, faces

### 4.5 — verdict_partial — **MISSING**

> Painterly oil painting, 480x480, dramatic chiaroscuro. The incomplete
> diagnosis: an autopsy report lying on a steel bench, top half in a sharp
> cone of lamplight and crisply legible in form, bottom half sliding into
> deep shadow where a second page has slipped out of square and covers the
> conclusion. Beside it, one of two syringes in focus, the other blurred at
> the dark edge of the bench; a kidney dish holding a single vial where the
> rack shows space for two. The truth half-recovered, the mechanism named
> but not the hour. Split lighting straight down the canvas. Victorian
> clinical noir, surgical chrome and linen against night-shift dark, no
> text.
> **Negative:** text, lettering, watermark, signature, logo, pixel art, contemporary hospital equipment, anime, cartoon, neon palette, lens flare, people, figures, faces

---

## 5. Hero Objects

Six load-bearing OBJECT_FOCUS tokens — the evidence spine of the case
(Dray's signature, the marked manual page, the 22:47 keycard entry, the
short vial count, Owen's two visits, the silenced monitor's access). 64×64
pixel art icons on transparent background. Target:
`art/ui/icons/attended_hour_object_<id>.png`. **All MISSING.**

### 5.1 — object_medication_chart — **MISSING**

> 64x64 pixel art icon, transparent background, single object centered. A
> clinical medication chart on a clipboard: metal clip at top, ruled dosage
> grid suggested by abstract line marks (no readable text), two signature
> scrawls implied as looping strokes at two separate time rows, one fresh
> dark ink blot in the margin. Bleached-linen paper, ward-green clip,
> iodine-brown shadow edge. 16-bit era, crisp 1-px outlines, limited
> palette, slight 3/4 tilt, no text.
> **Negative:** readable text, lettering, watermark, anti-aliasing, soft edges, drop shadow on background, anime, photorealism

### 5.2 — object_interaction_manual — **MISSING**

> 64x64 pixel art icon, transparent background, single object centered. A
> thick drug interaction manual lying open: heavy iodine-brown cloth
> binding, dense abstract column marks on both pages (no readable text),
> one page corner visibly dog-eared, a small pencil resting in the gutter,
> a faint graphite line down one column. Bleached-linen pages, deep shadow
> in the spine. 16-bit era, crisp 1-px outlines, limited palette, slight
> overhead 3/4 view, no text.
> **Negative:** readable text, lettering, watermark, anti-aliasing, soft edges, drop shadow on background, anime, photorealism

### 5.3 — object_drug_ledger — **MISSING**

> 64x64 pixel art icon, transparent background, single object centered. A
> tall dispensary drug ledger, closed: dark ward-green board cover with a
> brass corner and a cloth spine, a red ribbon page-marker hanging out at
> one entry, a small paper docket protruding crooked from the pages. A
> tiny phosphor-green keypad dot reflected on the cover's corner as the
> only accent. 16-bit era, crisp 1-px outlines, limited palette, slight
> 3/4 standing tilt, no text.
> **Negative:** readable text, lettering, watermark, anti-aliasing, soft edges, drop shadow on background, anime, photorealism

### 5.4 — object_syringe_tray — **MISSING**

> 64x64 pixel art icon, transparent background, single object centered. A
> chrome syringe tray seen from a high 3/4 angle: an enamel kidney dish, two
> glass syringes laid parallel, a moulded vial rack with most slots filled
> by small stoppered vials and exactly two slots conspicuously empty, one
> cotton swab pot. Surgical chrome highlights against deep shadow,
> bleached-linen liner cloth. 16-bit era, crisp 1-px outlines, limited
> palette, no text.
> **Negative:** readable text, lettering, watermark, anti-aliasing, soft edges, drop shadow on background, anime, photorealism

### 5.5 — object_visitor_log — **MISSING**

> 64x64 pixel art icon, transparent background, single object centered. A
> visitor log book open on its lectern edge: ruled entry lines as abstract
> strokes (no readable text), a pen on a fine chain trailing off-frame, one
> torn-out slip of paper laid diagonally across the page with a folded,
> worried corner — the slip worked by a nervous thumb. Bleached linen and
> iodine brown, warm sconce-light tint. 16-bit era, crisp 1-px outlines,
> limited palette, slight 3/4 view, no text.
> **Negative:** readable text, lettering, watermark, anti-aliasing, soft edges, drop shadow on background, anime, photorealism

### 5.6 — object_ward_keycard — **MISSING**

> 64x64 pixel art icon, transparent background, single object centered. A
> 1970s magnetic-stripe ward keycard lying across a small wall-reader unit:
> the card in bleached linen with a dark stripe and a blank signature
> panel, the boxy reader in ward-green enamel with a single phosphor-green
> indicator lamp lit and a slot mouth in shadow. Brass screw heads at the
> reader's corners. The instrument of after-hours access. 16-bit era, crisp
> 1-px outlines, limited palette, slight 3/4 tilt, no text.
> **Negative:** readable text, lettering, watermark, anti-aliasing, soft edges, drop shadow on background, anime, photorealism

---

## Generation Notes

- **4× render, nearest-neighbor downscale.** Generate every pixel-art asset
  at 4× target (backdrops 1280×1280 → 320×320; portraits 768×768 → 192×192
  → 96×96; hero objects 256×256 → 64×64), then nearest-neighbor downscale.
  Native low-res generation goes soft; scale-down keeps edges crisp.
  Briefing and verdict cards are painterly — generate at 960×960 and
  bicubic-downscale to 480×480, no pixel pass.
- **Palette quantize after downscale**: index pixel assets to ≤48 colors
  built from the ten Palette hexes above (ramps allowed). Keep Phosphor
  Green and Crash Crimson to ≤2% of pixels each.
- **Seed ranges** (deterministic re-rolls, log actual seed used):
  backdrops 4100–4199, portraits 4200–4299, briefing 4300–4309, verdicts
  4310–4349, hero objects 4350–4399. Generate v01–v03 candidates per asset,
  promote the best to the canonical filename.
- **PROVENANCE.txt**: for every committed asset, append a line to
  `art/attended_hour/PROVENANCE.txt` (create if absent):
  `<filename> | <model+version> | seed=<n> | <date> | prompt-sheet 5.x/2.x ref`.
  Hosted-service runs must capture the full final prompt string verbatim.
- **Model tips**: SDXL — lead with "16-bit pixel art" and add
  `(pixel art:1.3)` weighting; the shared negative list matters more than
  positive styling. Flux — drop the weighting syntax, keep prompts as prose,
  it follows the composition clauses well; enforce palette in post. 
  Midjourney — append `--style raw --no text,people` and translate the
  negative list into `--no` terms; MJ fights transparent backgrounds, so
  generate hero objects on flat `#13181A` and key it out in post.
- **Consistency check** before promoting any portrait: line up all 12 at
  96×96 — same plate-edge treatment, same key-light direction (cold from
  upper left, warm fill lower right), same backdrop value range. Re-roll
  outliers rather than adjusting in post.
- **Era guard**: anything that reads later than ~1978 (LED segments, digital
  displays beyond the lift dial, modern scrubs, disposable plastics in
  bulk) fails review. The Victorian shell must survive in every interior:
  at least one period architectural element (ceiling rose, sash, dado,
  panelled door) per backdrop.
