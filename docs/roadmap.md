# Switchable Glasses Roadmap

Last updated October 19, 2026. Live version kept in the project's roadmap document.

## How to read this roadmap

The roadmap gets the glasses working first, then miniaturizes them, and only then orders lens-shaped cells. No prescription lenses are involved at any point. "Custom lenses" means liquid crystal cells cut to an eyeglass shape, because the Adafruit cells are 36 mm squares.

- Each phase ends at a gate. Move on only when every criterion in that gate passes.
- Every number is a proposed target, not a measured result. Change any target you disagree with before you test, not after.
- "Unpolarized transmission" means how much ordinary scene light the lens passes in the same mode, measured with the same sensor.

## At a glance

Seven phases in three stages, with three gates (A, B, C).

The first working pair uses the Adafruit squares and a clip-on electronics box. Everything after phase 3 is about making it smaller and better looking.

## Phases and success criteria

### Stage 1: Make it work

### Phase 1: Glare-cut on the bench (test 1, today)

This phase answers one question: does an unpowered stand-in cell cut polarized glare as well as real polarized sunglasses?

| Criterion | Pass mark |
| --- | --- |
| Glare let through, white screen | 5% or less |
| Glare let through, red and blue screens | 10% or less |
| Scene light let through | 70% or more |
| Versus your polarized sunglasses | No more than 2 points worse on glare |

Tools: [`firmware/bench-test-1/code.py`](../firmware/bench-test-1/code.py) and its README. Optional and free: look at your screens through circular cinema 3D glasses to preview the best possible screen mode.

### Phase 2: Screen mode and drive on the bench

This phase is the main go/no-go test: can the cell pass screen light evenly at every angle?

| Criterion | Pass mark |
| --- | --- |
| Portrait versus landscape at the setpoint | Within 5%, recorded as measured voltage, not duty |
| Worst angle over a full rotation, straight on | At least two-thirds of unpolarized transmission (dimmest at least half the brightest), each color |
| Worst angle, 15° left, 15° right, 20° down | Dimmest at least 0.4 of the brightest |
| Color change as the screen rotates | Blue-to-red ratio within ±15%; no tint shift you can see on a white screen |
| Real screens (phone, laptop, car display), shade and sun | Readable at every orientation wherever non-polarized sunglasses of similar darkness are readable |
| Drive waveform | Average voltage across the cell under 20 mV; voltage within 3% of target |
| Power loss | Back to glare-cut in under 1 s |
| Two cells on one drive | Within 10% brightness of each other; no color difference you can see |
| Temperature (5, 25, 40 °C) | Setpoint follows a smooth curve; screen-mode marks still pass |

**Gate A passes** when glare-cut, the angle sweep, color and real-screen readability all pass, with the bare cell or with a stock quarter-wave film added.

### Phase 3: Wearable first version

A printed frame holds the two Adafruit squares (front polarizer peeled), a world-side shield and an eye-side polycarbonate window. The QT Py, battery and a tactile button sit in a clip-on box with a thin cable to the frame.

| Criterion | Pass mark |
| --- | --- |
| Shield scrap rotated between crossed polarizers, in a printed rim | No visible stress rainbows |
| Glare outdoors (road, water, car hood) | Cut as well as your polarized sunglasses, judged side by side |
| Screens outdoors in screen mode | Phone, laptop and car display readable at every orientation |
| Button | 199 of 200 long presses switch; 0 of 200 taps switch |
| 2 hours of wear | No unintended switches; nothing loose |
| Battery | Runs 4 hours or more |
| Unplug the cable | Lenses fall back to glare-cut in under 1 s |

**Gate B passes** when both modes work on your face outdoors. This is the working prototype.

### Stage 2: Miniaturize

### Phase 4: Electronics into the frame

The board, battery, button and charge pins move into the right temple, with two wires through the hinge. Test fit and comfort with dummy lenses of the final weight (about 11 g per side) while the board is designed.

| Criterion | Pass mark |
| --- | --- |
| Temple board with three-level drive, series capacitor and watchdog | Phase 2 drive and fail-safe marks pass at 3.0 V |
| Stuck pin | Back to glare-cut within 15 s; watchdog resets within 2 s |
| Battery current | 250 µA or less in screen mode, 10 µA or less in glare-cut standby |
| Hinge, 10,000 open/close cycles with wires logged | No dropout longer than 1 ms; resistance change under 10%; no exposed strands |
| 4 hours of wear with dummy lenses | No more than one push-up per hour; no soreness; sits level (add a 2.5 g left counterweight if needed) |
| Battery life | A full day of screen mode on one charge |

### Stage 3: Final lenses

### Phase 5: Quotes and order for lens-shaped cells

Send the quote request during phase 4, because cell makers take weeks to answer and build. **Gate C passes** when the price is under your ceiling, the vendor's drawing matches the outline (glass at most 54 × 44.5 mm) and the transmission data is offered.

### Phase 6: Final build

| Criterion | Pass mark |
| --- | --- |
| Custom cells on arrival | Phase 1 and 2 marks repeated on the real lenses |
| Frame twisted 1,000 times, cells watched between polarizers | No pressure marks in the liquid crystal |
| Impact: 16 mm steel ball dropped 127 cm onto each lens in the frame | Lens stays in; nothing reaches the eye side; the world shield may crack, the eye-side window may not |
| Whole glasses dropped 1.5 m onto a hard floor, six orientations | Lenses stay in; both modes still work |

### Phase 7: Full-day wear

| Criterion | Pass mark |
| --- | --- |
| Morning to night in public | Comfortable all day; no unintended mode switches |
| Glare and screens in real use | Glare-cut works on roads and water; screens readable in screen mode |
| Battery | Lasts the day with charge to spare |
| Shield recheck after wear | Still no stress rainbows |

**Done** means prototype v1 is complete.

## If a gate fails

| Failure | Next step |
| --- | --- |
| Weak glare-cut on the stand-in cell (phase 1) | Recheck rotation and peeling residue; try a second cell |
| Screen mode uneven with the bare cell (gate A) | Use the sweep data to size an aligned retarder film on the world side, try a stock quarter-wave film, then retest both modes |
| Still uneven with a film (gate A) | Stop before building anything wearable. Look at a variable retarder cell, a guest-host cell, or making them variable-darkness glasses |
| Cells don't match (phase 2) | Separate drive per lens: two more pins, four wires to the frame |
| False switches or short battery life (phase 3) | Longer press, better button spot, bigger battery in the clip-on box |
| Hinge wires fail (phase 4) | Route through a hollow hinge pin or use a flexible circuit loop |
| Quote over the ceiling (gate C) | Ask about 0.4 mm glass, a simpler outline or a stock round cell; otherwise keep a frame designed around square cells |

## Open decisions

- [ ] Shield tint for the wearable first version
- [ ] Price ceiling for lens-shaped cells, needed before phase 5
- [ ] Glass thickness, 0.55 mm or 0.4 mm, at phase 5
