# Bench test 2: light valve with power on (screen mode)

Programs: [code.py](code.py) (commands) and [valve_drive.py](valve_drive.py) (the drive), for
the QT Py SAMD21. They drive a light valve on pins A2 and A3 with the design's three-level wave
([design revision](../../docs/design-revision.md), section 4.1) and let you set the voltage.
Test page: `Power-on test.html`.

## Why

With no power, the valve blocks glare (bench test 1). Screen mode needs a voltage where a
screen looks about equally bright at every angle through the valve. This test looks for that
voltage by eye. Whether this valve has one is not known yet (design revision, section 2.2):
the darkest angle may fade away as the voltage rises, or it may just slide round. Either is a
useful result. The measured version (dimmest / brightest of 0.5 or more, section 2.4) needs
the light sensor and comes later as a separate program.

## Wiring

One valve wire to **A2**, the other to **A3**, either way round. Nothing else. Never connect
the valve to 3V, 5V or GND: those are steady voltages and would push a steady (direct)
current through it. Unplug the USB cable while connecting. A2 and A3 are neighbouring holes,
so make sure the two wires (and any clips) can't touch. Leave enough slack to turn the valve
half a turn. The VEML7700 sensor can stay on the STEMMA QT cable; this test doesn't use it.

## Install

Double-click `Install to board.bat` with the board plugged in. It copies `code.py` and
`valve_drive.py` onto the `CIRCUITPY` drive. To go back to bench test 1, run bench test 1's
installer (it replaces `code.py`; the extra `valve_drive.py` does no harm).

## Eye check with the page

Open `Power-on test.html` in Chrome or Edge, click **Connect to board**, then **Start the eye
check**. It walks through three steps: valve off (find the dark angle), full power (the dark
angle should turn light, which proves the wiring), then stepping the voltage with the arrow
keys while turning the valve slowly through half a turn, and pressing M at the most even
voltage. It ends with four quick questions, with the white area still showing beside them,
and a **Copy results** button (which also turns the valve off). The results screen turns the
valve off by itself after 3 minutes.

## Commands (any serial console at 115200 baud)

| Type | Does |
|---|---|
| `v 1.8` | Drive the valve at 1.8 volts (root-mean-square), 0 to 3.2. `v 0` turns it off. |
| `v` | Show the drive: the voltage estimate and the measured frequency. |
| `f 100` | Drive frequency, 30 to 300 times a second (starts at 100). Try higher if you see flicker. |
| `h` | Help. |

## How the drive keeps the valve safe

- Each cycle: A2 high for a pulse, both low, A3 high for an equal pulse, both low. Both pulses
  run through the same function with the same loop count, so they last the same time and the
  average voltage across the valve is zero. In a simulation on a computer, with far rougher
  timing than the board's, the average stayed under 5 millivolts.
- Voltage = 3.3 × √D, where D is the fraction of each cycle that either pin is high. The pulse
  loops are timed against the board's millisecond clock at start-up (three runs, middle one
  used, with a warning if they disagree), and the gap is trimmed once a second to hold the
  frequency, in small steps, ignoring any second with a long pause. The voltage shown is an
  estimate from the 3.3 V supply, not a meter reading.
- Everything slow (serial, printing) happens while both pins are low, so a stall only
  lengthens a 0 V gap. New settings start at the beginning of a cycle, so both pulses of a
  cycle always match.
- Both pins start low, and the program sets them low when it stops (Ctrl-C, an error or a
  reload). Unplugging the board leaves the valve unpowered, which is glare-cut.
- The final glasses use a hardware timer, a series capacitor and a watchdog instead
  (section 4.3). This bench version has none of those, so don't leave it running unattended.

## Memory

The QT Py M0 compiles each `.py` file in its roughly 20 KB of free memory. One file holding
everything (including the sensor commands) needed about 31 KB to compile, so the program is
split in two and has no sensor code. In a model of the board's memory, it needs about 12 KB
free, against about 20 KB for bench test 1 with the sensor library.

This code has been checked on a simulated board, not on real hardware yet.
