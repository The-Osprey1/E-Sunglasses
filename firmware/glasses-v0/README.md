# Glasses v0: automatic shade, with touch pads

Programs for the QT Py M0 (CircuitPython): the light valves darken by a variable amount, set
by an **automatic mode** (a light sensor) or by **two touch pads** you hold to go darker or
clearer. This is the first all-in-one program; it follows bench tests 1 and 2
([`../bench-test-1/`](../bench-test-1/), [`../bench-test-2/`](../bench-test-2/)).

**Status: checked on a simulated board and in a model of the board's memory; not yet run on
the real glasses hardware.** Expect to adjust numbers in `config.py` (below).

## What it needs

- The QT Py M0 with CircuitPython 10 (already on the board).
- Light valves with **both polarizer films on**. Powered off they are clear; the more voltage,
  the darker they get (Adafruit: starts at about 1 V, nearly opaque at about 4 V). A valve
  with one film peeled can't dim ordinary light, so it is no use for this program.
- The VEML7700 light sensor on the QT Py's STEMMA QT port, **facing forward, outside the
  valves** (if it sits behind a valve it sees the dimmed light and the shade would chase itself).
- Two touch wires (bare wire end, foil or a small metal pad) for the touch pads.

## Wiring

| Wire | Goes to |
|---|---|
| Valve, one wire | **A2** |
| Valve, other wire | **A3** (either way round; two valves can share the same two wires) |
| Touch pad "darker" | **A0** |
| Touch pad "clearer" | **A1** |
| Light sensor | the STEMMA QT cable into the QT Py's STEMMA QT port |

Nothing goes to 3V, 5V or GND except through the sensor cable. Keep the touch wires away from
the valve wires. Unplug the USB cable while wiring.

## Install

Double-click `Install to board.bat` with the board plugged in. It copies the program files
onto the `CIRCUITPY` drive (`code.py` last) and the board restarts by itself. If the board's
small drive is nearly full it offers to delete the `lib` folder (only bench test 1 used it).
**Don't touch the touch pads while the board starts**: it measures their resting reading then.

Install keeps a `config.py` that is already on the board, so your tuning survives an update.
To go back to the standard settings, or to repair a `config.py` that stops the program (see
the typo warning below), delete `config.py` on the `CIRCUITPY` drive and run Install again.

## Using it

- **Automatic mode** is on at start. The sensor is read four times a second. Up to
  2,500 lux the lenses stay clear; from 30,000 lux they are at full shade; between the two the
  shade follows the logarithm of the light (the eye judges brightness that way). Darkening is
  quick (about 2 seconds for the whole range) and lightening slower (about 7 seconds), so passing
  shade doesn't flicker the lenses.
- **Hold the "darker" pad (A0)** and the shade rises while you hold; **hold "clearer" (A1)** and
  it falls. A pad counts once it has been held for a quarter of a second. Touching a pad
  switches to **manual mode**, and the lenses stay where you left them.
- **Hold both pads for 1 second** to switch between manual and automatic. Put both fingers down
  together (within a quarter of a second of each other). The lenses blink: one blink = now
  manual, two blinks = now automatic.
- If the light sensor isn't answering, automatic mode keeps the lenses clear (safe) and the
  touch pads still work. It checks again every few seconds.
- Both valve pins are low whenever the program stops or fails, so the valves go clear.

## The monitor page

Open `Glasses monitor.html` in Chrome or Edge with the board plugged in and press **Connect to
board**. It shows the mode, shade, valve voltage, light level, the touch pad readings and the
board's free memory, twice a second, and has buttons to switch mode or set the shade from the
computer. It never stops the program. **Restart the board** shows the start-up messages if
nothing seems to happen. The "Tune automatic mode" box lets you try new lux numbers live and
copies the two lines to paste into `config.py`.

## Settings: `config.py`

Open `config.py` on the board's drive in Notepad (the copy on the board, not the one in this
folder), change a number and save; the board restarts. Keep only numbers after the `=` signs:
a typo stops the program at start-up, and the monitor page then shows the error.

| Setting | Default | Meaning |
|---|---|---|
| `VOLTS_START` | 1.0 | Valve voltage at the faintest shade. |
| `VOLTS_DARK` | 3.2 | Valve voltage at full shade (3.2 is the most this board gives). |
| `FREQ_HZ` | 100 | Pulses per second. Try higher if you ever see flicker. |
| `CLEAR_LUX` | 2500 | At or below this light level the lenses stay clear. |
| `DARK_LUX` | 30000 | At or above this the lenses go to full shade. |
| `MAX_SHADE` | 1.0 | Darkest automatic mode may go (0 to 1). |
| `DARKEN_PER_S` | 0.5 | Darkening speed (1 = whole range in 1 second). |
| `CLEAR_PER_S` | 0.15 | Lightening speed. |
| `MANUAL_PER_S` | 0.5 | How fast a held pad changes the shade. |
| `BOTH_HOLD_S` | 1.0 | Seconds to hold both pads to switch mode. |
| `TOUCH_MARGIN` | 100 | How far above rest a pad must read to count as touched. Raise it if the pads trigger by themselves; lower it if a touch isn't noticed. |

The shade (0 to 1) becomes a valve voltage: 0 V below 1% shade, otherwise
`VOLTS_START + (VOLTS_DARK - VOLTS_START) x shade`, never above 3.2 V.

## Typed commands (any serial console at 115200 baud, or the monitor page)

| Type | Does |
|---|---|
| `s` | Show the state once. |
| `mon 1` / `mon 0` | Show the state twice a second / stop. |
| `auto` | Automatic mode. |
| `m 0.5` | Manual shade, 0 (clear) to 1 (full shade). |
| `lux 1000 20000` | Stay clear up to 1000 lux, full shade from 20000, until the board restarts. |

## Known limits

- **No hardware fail-safe yet.** The drive is timed in software, with no series capacitor and
  no watchdog (design-revision.md, section 4.3). If the board itself froze with a valve pin
  high, the valve would get steady current, which can damage it and leave the lens dark. The
  program sets both pins low whenever it stops or fails *in software*, but don't leave the
  glasses running unattended or wear them for long stretches until those parts are added.
- **The drive is the same as bench test 2's**, so it can't give more than about 3.2 V. The
  large valve may need about 4 V to get nearly opaque; if full shade isn't dark enough, a
  higher-voltage driver is the next change.
- **Touch pads can misfire with wet skin or sweat.** The design review suggested a sealed tactile
  button instead; the pad wires can be swapped for buttons later without changing the program
  much.
- The lens "blink" for mode changes uses the valves themselves, so it only shows if the valves
  are dark enough or clear enough for a dip of about 0.4 in shade to be seen.
- The light sensor's range is the lowest-sensitivity setting (up to about 140,000 lux), so full
  sun doesn't overload it, but a dim room reads coarsely. That is fine for sunglasses.

## Memory

The QT Py M0 compiles each `.py` file in about 20 KB of memory, so the program is many small
files and `code.py` loads them one at a time, biggest first, clearing leftovers in between.
In a model of the board's memory (which counts some extra for stand-in parts) the whole
program, running and answering commands, needs about 14 KB free at the start; bench test 2,
which ran on the real board, needs about 13 KB in the same model. The monitor page shows the
real free memory. If the board ever stops with `MemoryError`, `console.py` is the first thing
to slim down.

## Files

`code.py` (start-up), `config.py` (settings), `valve_drive.py` (the three-level drive),
`light.py` (sensor), `auto.py` (automatic shade), `touch.py` (pads), `controls.py` (modes and
shade), `out.py` (shade to voltage, blink), `console.py` (typed commands and state line).
