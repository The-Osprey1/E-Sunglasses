# Switchable-polarization glasses: design revision after review

Response to the two advisor reviews of *Polarizing Glasses Prototype*, Rev D (2026-10-11).
Status: proposal for Rev E. Nothing here has been measured yet. Every number marked
"target" is a proposed pass mark you can change; every number marked "estimate" is
arithmetic, not a test result.

---

## 1. Summary

Both reviewers are mostly right, and the main fix is to change what the project
promises, not to abandon it.

1. **Screen mode becomes the feasibility gate, and it now has a precise target.** For
   any lens built from clear liquid crystal and film layers followed by one polarizer,
   the only state that passes screen light equally at every polarization angle is the
   one that behaves like a *circular* polarizer. Your "equal in portrait and landscape"
   test checks one of the two numbers that decide this; a four-angle or full sweep
   measures both. Section 2 explains it and gives a free way to see the ideal result
   on your own screens with cinema 3D glasses before building anything.
2. **The compensation film is reframed as a conditional design step.** There is a
   specific film placement (a retarder on the world side with its axis exactly
   horizontal or vertical) that provably leaves glare-cut unchanged for horizontal and
   vertical light. Whether it can fix screen mode, and which value it needs, comes out
   of the sweep data. It still has to be re-tested in both modes.
3. **The drive waveform is corrected** to a three-level wave (+3 V, 0 V, −3 V, 0 V) with
   equal positive and negative pulses timed by one hardware timer. Your formula
   RMS = 3√D is right for this wave. It also halves the drive current. A series
   capacitor and a watchdog turn "bleed resistor" into an actual fail-safe.
4. **The glass is never the eye-facing layer.** A thin polycarbonate window carries the
   polarizer film on the eye side, the stack floats in a printed elastomer gasket, and
   it seats against an eye-side lip in the frame. Impact is judged with the standard
   sunglass drop-ball test.
5. **Every test now has a numeric pass mark**, including absolute brightness, color,
   uniformity, interocular matching, trial counts and drop conditions (section 6).
6. **Quotes go out now, in parallel with the bench test**, with a price ceiling you set
   before seeing them. A draft quote request is in Appendix B.
7. **Alternatives are weighed honestly** (section 3). The twisted nematic cell stays the
   bench choice because the parts are in hand, but the quote request also asks for an
   untwisted variable retarder, which reaches the ideal screen-mode state by
   construction.

Decision I'd make: approve the bench work and the quote requests; defer the custom-lens
purchase, the temple board and final miniaturization until Gate A (optics) and Gate C
(quotes) pass.

---

## 2. Optics: what screen mode must actually do

### 2.1 Where each review is right, and where it isn't

- **Reviewer 1 is right**: equal brightness for horizontal and vertical screen light
  does not prove orientation-independence. Their 45° example is exactly the failure
  case.
- **Reviewer 2 is right** that a twisted nematic cell at partial voltage is not a clean
  rotator: it becomes an elliptical, wavelength-dependent element, so color tint is a
  real risk.
- **Reviewer 2 has one point backwards.** Ellipticity is not the problem; it is what
  screen mode *needs*. A cell that stayed a pure rotator would be the worst possible
  case (it is Reviewer 1's 45° example). The real problem is that nothing guarantees
  the cell lands on the right ellipticity, at every color, at every viewing angle.
- **"Rainbow fringing across the screen"** needs a cause that varies across the lens
  (uneven cell gap, varying viewing angle). A uniform cell is more likely to give an
  overall tint that changes as you rotate the screen. Both are possible; the bench test
  will show which.

### 2.2 The rule (plain-language version; math in Appendix A)

Every lens of this kind (any clear layers, then one polarizer) has exactly one
polarization state it passes fully and one opposite state it blocks fully. Call the
fully-passed state the lens's **pass state**. For linearly polarized screen light at
angle θ, transmission is

    T(θ) = ½ · Tp · [1 + a·cos 2θ + b·sin 2θ]

where Tp is what the polarizer film passes on its good axis (about 0.85 to 0.9), and
a, b describe the pass state: a measures how "horizontal versus vertical" it is,
b how "diagonal" it is.

- Glare-cut wants the pass state to be vertical (a ≈ −1, so horizontal glare is blocked).
- Screen mode wants a = 0 **and** b = 0. Then every linear screen polarization passes at
  exactly half. The only pass states with a = b = 0 are circular ones.
- Your current tuning step (equal portrait and landscape) sets a = 0 only. b is
  whatever the cell happens to give.
- The worst-to-best ratio over a full rotation is (1 − r)/(1 + r), with r = √(a² + b²).
  Your pass mark "dimmest at least half the brightest" means r ≤ 1/3.

Two consequences worth writing into the proposal:

1. **One knob cannot generally hit two targets.** Voltage moves the pass state along one
   path. You need a = 0 and b = 0 at the same voltage. Whether the path passes near the
   circular state is a property of the specific cell, which is why this is a gate and
   not a tuning detail.
2. **No single-polarizer design is perfect for every screen.** A lens that is ideal for
   linearly polarized screens will dim circularly polarized light of one handedness.
   Most phone and laptop screens emit linear light; a few devices add a film to make
   their output closer to circular so polarized sunglasses work. Test those too.

### 2.3 A free test of the ideal screen mode, before any electronics

Cinema 3D glasses of the circular kind (the type used for RealD screenings) are, as
worn, exactly the ideal screen-mode lens: a quarter-wave layer facing the world, a
linear polarizer facing the eye. Wear a pair and look at your phone, laptop and any
car or appliance displays while rotating them.

- What you see is roughly the best screen mode any single-polarizer design can reach:
  about half brightness at every angle, with some color tint because the layer is only
  quarter-wave at one color.
- If that experience is not good enough, no tuning of the twisted nematic cell will be
  either, and the project should look hard at the guest-host option in section 3.
- The two eyes have opposite handedness. A screen that looks fine in one eye and dark in
  the other is emitting near-circular light; note which devices do that.

### 2.4 Revised bench procedure for screen mode (replaces checks 2 and 3)

1. Find the voltage where horizontal and vertical input match within 5%. Record the
   **measured root-mean-square voltage across the cell**, not the duty (see 4.4 for why).
2. At that voltage, rotate a polarizer over a lamp through 0° to 180° in 15° steps.
   (Four angles, 0°, 45°, 90°, 135°, are enough in theory to get a and b; the full sweep
   checks the model.) Fit the sinusoid and record a, b and r.
3. Repeat in three color bands. Swap the broadband light sensor for, or add, a
   multi-channel spectral sensor (Adafruit sells an AS7341 breakout on the same
   plug-in connector, around $16) so blue, green and red come from one setup.
4. Repeat steps 2 and 3 with the cell tilted 15° left, 15° right and 20° down, and at
   the temperatures in check 6.
5. Measure transmission for circular input of both handednesses (a circular polarizer
   used backwards, linear side toward the lamp, makes circular light).
6. Do the side-by-side readability comparison in 6.2 on real screens.

### 2.5 The compensation film, stated correctly

Replace "a thin compensation film evens out screen mode and leaves glare-cut alone"
with:

> If the sweep shows r is too large, test whether a fixed retarder film on the world
> side, with its axis exactly horizontal or vertical, can bring it down; then
> revalidate both modes, including off-axis and in color.

Why that particular placement:

- Horizontal and vertical light are the natural states of an aligned retarder, so they
  pass through it unchanged. Transmission of horizontal glare and vertical scene light
  is therefore **exactly unchanged, at every wavelength and every voltage**, for light
  arriving straight on. The duty that balanced portrait and landscape stays the same.
- For the other polarizations it shifts the "diagonal" share b into the circular share.
  If the bare cell is close to a pure 45° rotator (the worst case), a quarter-wave film
  (about 138 nm of retardance at 550 nm) turns it into the ideal circular state. Other
  measured values call for other retardances; Appendix A gives the formula.
- It is forgiving of alignment: a 2° axis error adds well under 1% glare leak (estimate).

What it does **not** guarantee: correction at more than one color (the film and cell
disperse differently), correction off-axis (the film's axis appears rotated for tilted
rays), and anything about the shield, which sits in the same position and must itself
be free of birefringence. Stock quarter-wave films are cheap enough (roughly $20 to $60
a sheet, not checked) to try on the bench; a non-stock value, or lamination by the cell
maker, is a design change with its own quote.

---

## 3. Alternatives, weighed honestly

| Option | Glare-cut | Screen mode at every angle | Unpowered state | Availability | Main risk |
|---|---|---|---|---|---|
| **A. Twisted nematic cell, as drawn** | Good. Your model says under 5% leak from blue to red | Unknown; could land anywhere from ideal to worst case | Glare-cut | Custom shape | The gate in section 2 |
| **B. A + aligned retarder film** | Identical to A for horizontal and vertical light | Can be tuned to ideal at one color | Glare-cut | Stock film to try; lamination is custom | Color and off-axis behavior |
| **C. Untwisted variable retarder, axis at 45°** | Half-wave state leaks more at the color extremes: roughly 20% at 450 nm and 8% at 650 nm if half-wave at 550 nm (estimate) | Reaches the circular state by construction; the path never passes the diagonal failure | Can be designed to be glare-cut | Specialist makers sell these in round sizes; custom outline needed | Blue glare leak; residual retardance |
| **D. Ferroelectric quarter-wave switch** | Excellent (acts as a plain polarizer in one state) | Ideal at one color in the other state | Often bistable, so not a defined fail-safe | Rare, costly, thin cell gap | Sensitive to shock and pressure; poor fit for eyewear |
| **E. Single-layer guest-host (dye) cell, no film polarizer** | Weak: the aligned dye is a much less efficient polarizer than film; needs vendor data | Perfect when switched on, since there is no polarizer left in the path; also far less sensitive to viewing angle | Tinted and partly polarizing | Custom; some sunglass and visor products use guest-host cells | Glare-cut may be too weak to justify the project |
| **F. Double-layer or chiral guest-host** | None | Perfect | Clear or tinted, by design | Custom | Gives variable darkness only, no glare-cut |

Reading the table:

- **Reviewer 2's "guest-host instead"** solves screen mode by removing the polarizer, and
  with it most or all of the glare-cut. Option E keeps some glare-cut; F keeps none.
  If the real goal is variable darkness rather than glare-cut, F is the better design
  and most of section 2 disappears.
- **Reviewer 2's "wide-view discotic compensation film"** is the film used inside
  twisted nematic displays. It is matched to a full display stack and is not a stock
  part at quantity four. Ask the cell maker whether they can apply one; don't plan on it.
- **Recommendation:** bench-test A (and B with a stock quarter-wave film) because the
  parts are cheap and in hand. Ask the quote vendors to price A and C side by side. Use
  the section 2.3 cinema-glasses test as the early sanity check on whether the whole
  approach is worth it.

---

## 4. Drive electronics

### 4.1 The corrected waveform

Pins A and B each connect to one side of the cells (both cells in parallel).

| Pin A | Pin B | Voltage across cells |
|---|---|---|
| high | low | +3 V |
| low | high | −3 V |
| low | low | 0 V (cells actively shorted) |

One period T (10 ms at 100 Hz):

    +3 V  ┌──┐
     0 V ─┘  └─────────┐  ┌─────────
    −3 V               └──┘
          |<D·T/2>|    |<D·T/2>|
          0           T/2          T

- Positive pulse: pin A high for D·T/2 starting at 0.
- Negative pulse: pin B high for D·T/2 starting at T/2.
- Both low for the rest.
- RMS voltage = 3√D, so 25% gives 1.5 V, 44% gives 2.0 V, 69% gives 2.5 V, matching the
  numbers already on page 2. D = 100% is the full ±3 V square wave.
- Average voltage is zero because both pulses come from **one hardware timer** with the
  same compare value. Never time them in software.
- The original description (complementary pins with a variable duty) gives either
  +3 V or −3 V at all times; changing its duty adds direct current, not a lower RMS.
  Reviewer 1 is right on this, and Reviewer 2's praise of the drive missed it.

### 4.2 Check it, don't assume it

- Measure the voltage *between* the two cell terminals (two scope probes with the
  difference function, or one differential probe). Target: average under 20 mV, RMS
  within 3% of the setpoint. Ask the cell maker for their actual direct-current limit.
- Most handheld meters do not read RMS correctly on this wave. Use the scope trace, or
  measure the real pulse height under load and compute 3√D from it.

### 4.3 Fail-safe beyond the bleed resistor

The bleed resistor covers power loss. It does not cover a controller that hangs with a
pin stuck high, which puts steady direct current on the cells and freezes the mode.
Add:

1. **A series capacitor** (about 2.2 µF ceramic) between one pin and the cells. It blocks
   any direct current outright. If a pin sticks high, the cell voltage decays to 0 V
   through the bleed resistor in a few seconds (estimate: 4.7 MΩ × 2.2 µF ≈ 10 s), so
   the glasses land in glare-cut. Cost: the cells see about 97% of the drive (estimate),
   and ceramic capacitance varies with voltage, which is one more reason to calibrate in
   measured RMS volts.
2. **The microcontroller's watchdog timer**, so a hung program resets within about 1 s.
3. **Pins default low at reset**, so a reset means 0 V, which means glare-cut.

### 4.4 Bench versus final supply voltage

The bench board (QT Py) runs at 3.3 V; the final design runs at 3.0 V. The same duty
gives 10% more voltage on the bench, so a bench duty must be multiplied by about 1.21
for the final board. Record and transfer the **measured RMS voltage**, never the duty.

### 4.5 Current budget, revised (estimate)

Charge drawn per period for the three-level wave is 2·C·V, versus 4·C·V for the full
±3 V square wave. With 40 to 80 nF total at 100 Hz, lens drive drops from 50–100 µA to
about **24–48 µA**, and the screen-mode total from 170–220 µA to roughly 145–170 µA.
Two cautions:

- Zero intervals give the liquid crystal time to relax each half cycle. Check for
  flicker with a fast photodiode on the scope (the light sensor is too slow). If you see
  it, raise the frequency; current rises in proportion.
- Reviewer 1's point stands: measure the real battery current in both modes with a
  power profiler (Nordic's Power Profiler Kit II is about $100) or a shunt resistor and
  scope. Target: 250 µA or less in screen mode, 10 µA or less in glare-cut standby.

---

## 5. What the cheap cells can and cannot tell you

- Adafruit's small light valve is a twisted nematic cell, but its gap, birefringence,
  alignment and voltage curve are not published and almost certainly differ from your
  custom drawing (first-minimum gap, specified rubbing). Peeling also leaves adhesive
  that adds haze.
- So: a pass shows the arrangement *can* work; a fail does not disprove the custom
  cell; and its screen-mode voltage does not transfer.
- What does transfer: the measurement method, the drive electronics, the a/b/r analysis,
  the button and capacitance numbers, and your judgment of whether ideal screen mode
  (section 2.3) is worth having.
- **Optional second stand-in:** active-shutter 3D glasses (the battery kind, roughly
  $20 to $40) contain eyeglass-sized liquid crystal cells already in a frame. Their cell
  type varies by maker, so they are another screening sample, not a validation, but they
  let you wear the effect outdoors.
- Because of these limits, the quote request goes out **now** and asks the vendor for
  the data on page 7 plus a few answers about safety and alternatives (Appendix B).

---

## 6. Revised test plan with pass criteria

All pass marks are targets. "Unpolarized transmission" means the lens's transmission
for ordinary scene light in the same mode, measured with the same sensor.

### 6.1 Bench (stand-in cells)

| # | Check | How | Pass if |
|---|---|---|---|
| 1 | Glare-cut | Unpowered, horizontal then vertical polarized input, three color bands; repeat with your polarized sunglasses | Horizontal ≤ 5% (green), ≤ 10% (blue, red); vertical ≥ 70%; no worse than your sunglasses by more than 2 points |
| 2 | Screen-mode setpoint | Section 2.4 step 1 | Horizontal and vertical within 5%; record measured RMS volts |
| 3 | Angle sweep (gate) | Section 2.4 steps 2–5 | Worst angle ≥ ⅔ of unpolarized transmission (same as worst/best ≥ 0.5, r ≤ ⅓) in each color band, straight on; worst/best ≥ 0.4 at 15° left, 15° right, 20° down |
| 3b | Color shift | Same data | Blue-to-red ratio varies by no more than ±15% across the rotation; no tint change visible on a white screen |
| 3c | Absolute brightness | Complete stack incl. shield | Worst-angle screen transmission ≥ 10% (set once shield tint is chosen; 50% smoke gives about 13–19% for an ideal cell, estimate) |
| 4 | Fail-safe | Pull power in screen mode; separately, freeze firmware with one pin high | Glare-cut in under 1 s after power loss; glare-cut within 15 s, and watchdog reset within 2 s, after a stuck pin |
| 4b | Drive waveform | Section 4.2 | Average under 20 mV; RMS within 3% |
| 5 | Two cells match | Same drive, screen and glare-cut modes, three bands | Luminous transmission within 10% relative between cells; no visible color difference side by side |
| 6 | Temperature | Setpoint at about 5, 25, 40 °C; then hold the 25 °C setting with one cell at 25 °C and the other at 40 °C | Setpoint follows a smooth curve; at the held setting, check 3 still passes for both cells and interocular difference ≤ 10% |
| 7 | Button | See section 9 | 199 of 200 long presses switch; 0 of 200 taps switch; 0 false toggles in a 30-minute abuse session |
| 8 | Capacitance and current | Capacitance at working voltage with the drive running; battery current with a power profiler | Capacitance within the estimate; currents within section 4.5 targets |
| 9 | Optical quality | Five spots per lens; bright point light on a dark background; photograph a printed grid through the lens | Five spots within ±10%; no halo beyond your plain sunglasses; grid lines straight and single |

### 6.2 Readability comparison (Reviewer 1's step 4)

Phone, laptop, and any car or appliance display; four screen orientations plus 45°;
shade and direct sun. Compare side by side with (a) your polarized sunglasses and (b)
non-polarized sunglasses of similar darkness. Pass if every screen readable through (b)
is readable through the prototype at every orientation.

### 6.3 Mechanical and wear

| # | Check | Pass if |
|---|---|---|
| 10 | Hinge: 10,000 open/close cycles (several a day for about five years), wire continuity logged throughout | No interruption longer than 1 ms; resistance change under 10%; no exposed strands |
| 11 | Frame torsion: twist the front 1,000 times by hand, watching the cells between polarizers | No pressure marks in the liquid crystal (it shows them visibly, which makes it a built-in strain indicator) |
| 12 | Impact: drop a 16 mm (5/8 inch) steel ball from 127 cm (50 inches) onto each lens mounted in the frame. This is the US sunglass-lens rule, used here as a benchmark | Lens stays in the frame; nothing reaches the eye side; the world shield may crack, the eye-side window may not |
| 13 | Whole-glasses drop: 1.5 m onto a hard floor, six orientations | Lenses retained; both modes still work |
| 14 | Dummy-lens wear: frame with lenses of correct mass and center of gravity, 4 hours | No more than one push-up per hour; no soreness; sits level in a photo; compared against your heaviest everyday pair |

---

## 7. Lens stack and safety

Revised stack, world to eye:

1. **World shield**, 1.0 mm (or 0.75 mm, see weight). Optically clean material from the
   crossed-polarizer test (cast acrylic or CR-39). Sacrificial: it may crack.
2. **Air gap and gasket**, 0.5 mm, as now.
3. *(Optional)* **Aligned retarder film**, only if section 2.5 calls for it.
4. **Liquid crystal cell.** Ask the vendor for chemically strengthened glass, 0.4 mm
   glass, or a plastic substrate (Appendix B).
5. **Polarizer film laminated to a 0.5 mm polycarbonate eye-side window.** New layer.

Why the eye-side window is polycarbonate: birefringence after the final polarizer is
invisible, because the eye does not sense polarization in normal vision. So the
toughest material can go exactly where safety needs it, with no optical penalty. The
glass is then sandwiched between two plastic layers and is never the eye-facing surface.

Mounting:

- The stack **seats against a lip on the eye side** of the rim and is installed from the
  front, held by a printed front retainer. A hit from the front pushes the lens into the
  lip, not out of the frame.
- A **thermoplastic polyurethane (TPU) gasket** printed on the H2D's second nozzle wraps
  the stack edge, so no hard plastic touches the glass. Target: at least 0.3 mm of
  elastomer on every edge and face contact.
- Checks 11 to 13 test this directly.

Keep the "not protective eyewear" statement; it is honest. The goal of the changes is
that ordinary wear has a defensible breakage and retention strategy.

---

## 8. Weight and balance

- **Test with dummy lenses of the right mass and balance point** (about 11 g per side
  with the new window, estimate; a printed blank weighted with steel shot or tungsten
  putty), not just the right dimensions.
- **Left/right balance:** the extra mass in the right temple is roughly 2.5 g (battery,
  board, pins; estimate). Reviewer 2's "slides crooked" is plausible but likely
  overstated for that mass, since both ears share the load. It is cheap to settle:
  wear the dummy rig with and without a 2.5 g counterweight in the left temple.
  Moving the battery left instead would add two more wires through a second hinge,
  which trades a small comfort issue for the project's likeliest failure. Counterweight
  first; move the battery only if the hinge solution makes extra wires cheap.
- **Revised weight (estimate):** 47 g, plus about 2.4 g of eye-side windows, 0.5 g of
  gasket and up to 2.5 g of counterweight, gives about 52 g with 0.55 mm glass. With
  0.4 mm glass (−4 g) and a 0.75 mm world shield (about −1.2 g), about 47 g. Widely
  reported figures for camera smart glasses are close to 49 g, so this is within what
  people accept, but the nose takes most of it: use wide, soft nose pads and measure
  comfort in check 14.

---

## 9. Hinge wiring and the button

**Hinge.** Agree with Reviewer 2. Two 30 American Wire Gauge wires bending across a
barrel hinge is the weakest point. Options, best first:

1. Route the wires **through a hollow hinge pin**, so opening and closing twists them
   instead of bending them. Twisting is far gentler on stranded wire.
2. A **flexible printed circuit loop** around the barrel, with a generous radius.
3. Spring contacts on the hinge faces, so folding cuts the drive (which also lands in
   glare-cut). Risk: intermittent contact and corrosion from sweat.

Whichever you pick, check 10's 10,000 cycles is the pass mark, not "a few thousand".

**Button.** Agree with Reviewer 2: switch to a **small sealed tactile switch** under a
flexure button on the underside of the right temple, covered by a printed TPU membrane.
Keep the 0.8 s long press. Two extra benefits: it draws nothing while waiting (the
microcontroller wakes on a pin interrupt, whereas touch sensing has to keep scanning),
which protects the year-long glare-cut standby; and it gives a felt click, so you know
it registered without looking.

---

## 10. Cost and schedule

### 10.1 Revised roadmap

| Step | What | Gate |
|---|---|---|
| 0 (now) | Cinema 3D glasses test (2.3). Send quote requests (Appendix B). Order the Rev D parts plus spectral sensor, a quarter-wave film sheet, a 16 mm steel ball, optionally shutter 3D glasses and a power profiler | You set a price ceiling for four lenses before quotes arrive |
| 1 | Bench optics and drive: checks 1–9 | **Gate A**: checks 1, 3, 3b, 3c pass with the bare cell or with a stock film; readability (6.2) passes |
| 2 (parallel) | Shield test as in Rev D, plus the full stack on the bench | **Gate B**: shield stays clean in the complete stack |
| 3 (parallel) | Dummy-lens frame: fit, balance, hinge cycling, torsion, button | Checks 10, 11, 14 pass |
| 4 | Read quotes | **Gate C**: under your ceiling, vendor drawing matches the outline, data offered; pick option A or C |
| 5 | Order cells; then temple board and firmware while they are made | |
| 6 | Build v1; checks 12 and 13 on a spare lens assembly; full-day wear test | Done, prototype v1 |

If Gate A fails with the bare cell and with a stock film, stop and choose between
option C (ask for its quote), option E/F, or redefining the product as variable-darkness
glasses. Don't build the temple electronics first.

### 10.2 Budget

| Item | Cost |
|---|---|
| Rev D shopping list | $46.05 (checked 11 Oct) |
| Spectral sensor breakout | about $16 (not checked) |
| Quarter-wave retarder film sheet | about $20–60 (not checked) |
| Cinema 3D glasses | free to a few dollars |
| 16 mm steel ball | a few dollars |
| Optional: shutter 3D glasses, power profiler | about $20–40, about $100 |
| **Custom cells: tooling, units, data, any film lamination** | **Unknown. This is what the quote is for.** At quantity four, expect the one-time tooling and engineering charge to dominate. |
| Redesign if Gate A forces option C or E | Unknown |

The cheap part is about $90 to $250. The project's real cost is the custom lenses, so
the quote is on the critical path from day one.

---

## 11. Replacement wording for Rev E

**Page 1 and 3, screen mode:**
> Screen mode (about 2 V). The cell is driven to a partial state chosen so that screen
> light of every polarization angle passes in roughly equal amounts. Bench check 3
> measures whether the cell can reach that state across angles, colors and
> temperatures. That is the project's main feasibility gate.

**Page 2, square wave:**
> Three-level drive. Pin A high puts +3 V across the cells, pin B high puts −3 V, both
> low gives 0 V. Each period has one positive and one negative pulse of equal length,
> timed by one hardware timer, with 0 V between them. RMS = 3√D and the average is zero
> by construction. A 2.2 µF series capacitor blocks any direct current, and the
> differential voltage across the cells is measured to confirm.

**Page 2, fail-safe:**
> Power loss, a stuck pin and a hung program all land in glare-cut: the bleed resistor
> handles the first, the series capacitor the second, the watchdog the third.

**Page 3, stack:**
> The glass cell is never the eye-facing layer. The polarizer film is laminated to a
> 0.5 mm polycarbonate eye-side window, the stack floats in a printed elastomer gasket,
> and it seats against an eye-side lip in the frame.

**Page 7, "Diagonal screens dim (3)":**
> Use the sweep data to work out whether an aligned retarder film on the world side can
> fix it, try the nearest stock film, and revalidate both modes. If not, compare the
> variable-retarder cell quote.

**Page 6, "Two cheap tests cover most of the risk":**
> Two cheap tests screen the idea; they cannot validate the custom lenses, so quotes go
> out at the same time.

---

## 12. What is known versus assumed

- **Derived, not measured:** the screen-mode rule (section 2.2, Appendix A), the
  compensation-film invariance (2.5), the three-level wave math and currents (4), the
  variable-retarder leak figures (3), the weights (8).
- **Assumed, needs checking:** stock film and sensor prices, the cinema-glasses
  construction for the specific pair you get, the fraction of your screens that emit
  linear light, the comfort effect of 2.5 g of imbalance.
- **Unknown until measured or quoted:** where the actual cell's pass state lands, color
  and off-axis behavior, cell cost and lead time, whether strengthened glass or plastic
  substrates are offered.

---

## Appendix A: the math behind section 2

Describe polarization by its Stokes vector on the Poincaré sphere: horizontal is
(1, 0, 0), vertical (−1, 0, 0), +45° (0, 1, 0), circular (0, 0, ±1). For a lossless,
non-depolarizing stack of retarders followed by an ideal polarizer, there is a unit
vector **m** (the pass state, referred to the input) such that, for any input state
**s**,

    T = ½ · Tp · (1 + m · s)

For linear input at angle θ, **s** = (cos 2θ, sin 2θ, 0), so
T(θ) = ½·Tp·(1 + m₁ cos 2θ + m₂ sin 2θ). This is a sinusoid in 2θ with relative swing
r = √(m₁² + m₂²), giving worst/best = (1 − r)/(1 + r) and worst/unpolarized = 1 − r.

- Equal horizontal and vertical means m₁ = 0 only.
- Orientation-independence for all linear inputs needs m₁ = m₂ = 0, so **m** = (0, 0, ±1),
  a circular analyzer. It then fully passes one circular handedness and blocks the other.
- No non-depolarizing lens with one polarizer can be independent of every input state,
  because **m** is a unit vector.

**Aligned retarder on the world side.** A retarder of retardance Γ with its axis
horizontal rotates the sphere about the m₁ axis by Γ. The new pass state is
**m′** = (m₁, m₂ cos Γ − m₃ sin Γ, m₂ sin Γ + m₃ cos Γ) (sign of Γ depends on which
axis is fast). m₁ is unchanged, so transmission of horizontal and vertical light is
unchanged at every wavelength and voltage. To move a measured (m₂, m₃) to the circular
pole, choose Γ so the rotated m₂ is zero: tan Γ = m₂ / m₃. A pure 45° rotator
(m₂ = ±1, m₃ = 0) needs Γ = 90°, a quarter wave. Retardance in nanometres is
Γ/360° × λ. Since the sweep gives m₁ and m₂ but only the size of m₃, the circular-input
measurement in section 2.4 step 5 supplies its sign and any depolarization.

**Untwisted variable retarder at 45°.** It rotates the sphere about the m₂ axis, so the
pass state moves on the m₁–m₃ circle: horizontal pass at zero retardance, circular at a
quarter wave, vertical pass at a half wave. It never crosses the diagonal states, which
is why option C reaches screen mode by construction. Glare leak at half-wave design
λ₀ is cos²(δ/2) with δ = π·(λ₀/λ)·(dispersion), giving the estimates in section 3.

---

## Appendix B: draft quote request (for you to send)

> Subject: Budgetary quote, custom polarizer-free liquid crystal cells, prototype
> quantity
>
> Hello,
>
> I am building a prototype pair of electronically switchable sunglasses and would
> like a budgetary quote and feasibility feedback for the attached one-page cell
> drawing. This is not yet an order.
>
> - Quantity: 4 cells (2 spares), one part number for both eyes.
> - Type: twisted nematic, 90° twist, cell gap at the first Gooch–Tarry minimum,
>   no polarizers, outline and rubbing as drawn.
>
> Could you please tell me:
>
> 1. Price, including any one-time tooling or engineering charge, and lead time.
> 2. Whether you can supply 0.4 mm glass, chemically strengthened glass, or a plastic
>    substrate in this outline, and how each changes the price.
> 3. The expected spread in the 50% transmission voltage between cells, or whether you
>    can select a matched pair.
> 4. Whether you can laminate a retarder film to the world-side face, if I supply the
>    retardance and axis after bench testing.
> 5. Whether you would also quote an untwisted variable retarder in the same outline,
>    with its optic axis at 45° to the edge, designed to be a half-wave at 550 nm
>    unpowered.
> 6. Whether a polarizer-free guest-host (dye) cell in this outline is something you
>    make.
> 7. Your recommended drive frequency and the maximum direct-current component you
>    allow.
> 8. Whether you can supply the transmission data listed in notes 9 and 10 of the
>    drawing, and the cost of doing so.
>
> Thank you,
> [name, email]
