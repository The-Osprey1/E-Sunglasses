# Bench test 2: light valve with power on (screen mode)

Program: [code.py](code.py), for the QT Py SAMD21. It drives a light valve on pins A2 and A3
with the design's three-level wave ([design revision](../../docs/design-revision.md), section 4.1)
and lets you set the voltage. Test page: `Power-on test.html`.

## Why

With no power, the valve blocks glare (bench test 1). Screen mode needs a voltage where a
screen looks about equally bright at every angle through the valve. This test finds that
voltage by eye. The measured version (dimmest / brightest of 0.5 or more, section 2.4 of the
design revision) uses the light sensor and the `d`, `r`, `s` commands below.

## Wiring

One valve wire to **A2**, the other to **A3**, either way round. Nothing else. Never connect
the valve to 3V, 5V or GND: those are steady voltages and would push a steady (direct)
current through it. Unplug the USB cable while connecting. The VEML7700 sensor can stay on
the STEMMA QT cable; the eye check doesn't use it.

## Install

Double-click `Install to board.bat` with the board plugged in. It copies `code.py` onto the
`CIRCUITPY` drive (and the sensor library from `../bench-test-1/lib` if the board lacks it).
To go back to bench test 1, run bench test 1's installer.

## Eye check with the page

Open `Power-on test.html` in Chrome or Edge, click **Connect to board**, then **Start the eye
check**. It walks through three steps: valve off (find the dark angle), full power (the dark
angle should turn light, which proves the wiring), then stepping the voltage with the arrow
keys until turning the valve makes no difference, and pressing M. It ends with three quick
questions (evenness, tint, flicker) and a **Copy results** button.

## Commands (any serial console at 115200 baud)

| Type | Does |
|---|---|
| `v 1.8` | Drive the valve at 1.8 volts (root-mean-square), 0 to 3.2. `v 0` turns it off. |
| `v` | Show the voltage and frequency actually running, as measured by the board. |
| `f 100` | Drive frequency, 30 to 300 times a second (starts at 100). Try higher if you see flicker. |
| `m` | One light reading, in sensor counts (for voltage scans). |
| `d`, `r`, `s NAME`, `t`, `c` | Dark, reference, sweep, table, CSV, as in bench test 1, with the valve driven at the set voltage. The sweep summary shows dimmest / brightest; 0.5 or more passes screen mode. |

## How the drive keeps the valve safe

- Each cycle: A2 high for a pulse, both low, A3 high for an equal pulse, both low. Both pulses
  run through the same function with the same loop count, so they last the same time and the
  average voltage across the valve is zero. A simulated run measured under 2 millivolts average.
- Voltage = 3.3 × √D, where D is the fraction of each cycle that either pin is high. The pulse
  loops are timed against the board's millisecond clock at start-up, and the gap is adjusted
  once a second to hold the frequency, so the voltage shown is an estimate from the 3.3 V
  supply, not a meter reading.
- Everything slow (serial, sensor reads, printing) happens while both pins are low, so a stall
  only lengthens a 0 V gap. New settings start at the beginning of a cycle, so both pulses of a
  cycle always match.
- Both pins start low, and the program sets them low when it stops (Ctrl-C, an error or a
  reload). Unplugging the board leaves the valve unpowered, which is glare-cut.
- The final glasses use a hardware timer, a series capacitor and a watchdog instead
  (section 4.3). This bench version has none of those, so don't leave it running unattended.

This code has been checked on a simulated board, not on real hardware yet.
