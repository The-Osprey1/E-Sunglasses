# Bench test 1: glare-cut with no power

Program: [code.py](code.py), for the QT Py SAMD21 with the VEML7700 light sensor.
It measures how much polarized screen light gets through a sample (peeled cell or
sunglasses lens) at each angle, as a percent of the light with nothing in the way.

## Setup (once)

1. Install CircuitPython on the QT Py. Download the `.uf2` for **Adafruit QT Py M0**
   (the SAMD21 board) from circuitpython.org. Double-tap the board's reset button, and
   a `QTPY_BOOT` drive appears. Drag the `.uf2` file onto it. The board restarts as a
   `CIRCUITPY` drive.
2. Install the sensor library. The easiest way is `pip install circup`, then
   `circup install adafruit_veml7700`, which also pulls in the libraries it needs.
   Or copy `adafruit_veml7700.mpy`, `adafruit_register/` and `adafruit_bus_device/`
   from the CircuitPython library bundle into `CIRCUITPY/lib/`.
3. Copy `code.py` to the root of `CIRCUITPY`, replacing the one that's there.
4. Plug the VEML7700 into the QT Py with the STEMMA QT cable.
5. Open a serial console (Mu or Thonny work, or any terminal at 115200 baud) and press
   Enter. You should see `Bench test 1` and a `>` prompt.

## Test runner page (no console app needed)

`Bench test runner.html` runs the whole test from Chrome or Edge, with no serial console
to install. Open it in Chrome or Edge, click **Connect to board**, then **Start test**. It
restarts `code.py`, sends every command, switches the screen between white, red and blue,
draws an angle dial around the sensor spot, and beeps and shows what to do at each step.
At the end it shows pass or fail for each sweep (including the cell-versus-sunglasses
check) and has a **Copy results** button for the CSV.

## Running the test

| Type | Does |
|---|---|
| `d` | Dark reading. Cover the sensor tube completely. This subtracts leftover room light. |
| `r` | Reference. Sensor against the screen, nothing in the way. This counts as 100%. |
| `s cell-white` | Sweep. The program asks for 0°, 15° … 180°. Rotate the sample to each angle and press Enter. Type `q` to stop early. |
| `t` | Summary of all sweeps, with pass or fail. |
| `c` | All readings as CSV. Paste this into the project thread. |

Suggested order:

1. White screen, room lights down: `d`, `r`, `s sun-white` (sunglasses lens), `s cell-white` (peeled cell, peeled side toward the screen).
2. Red screen: `r`, `s sun-red`, `s cell-red`.
3. Blue screen: `r`, `s sun-blue`, `s cell-blue`.
4. `t`, then `c`, and paste the CSV output into the thread.

Put `white`, `red` or `blue` in each sweep name, because the program picks the pass mark
from it. Take a new reference (`r`) every time you change the screen color.

## Pass marks

- Lowest reading (glare getting through): 5% or less on white, 10% or less on red and blue.
- Highest reading (scene light getting through): 70% or more.
- The cell's lowest reading is no more than 2 points worse than the sunglasses' for the same color.

## Tips

- Keep the sensor tube pressed flat against the screen and hold the sample flat over it.
  Tilting the sample changes the result.
- If you see a "saturated" warning, lower the screen brightness and take the reference again.
- If the reference is weak, raise the screen brightness or darken the room.
- Peeled cells may have adhesive left on them. Clean it off gently with a little
  isopropyl alcohol on a cotton swab, and don't press hard on the glass.
- The light sensor responds roughly like the eye. Red and blue screens give a rough
  color check until a spectral sensor is added.

This code has been checked against a simulated sensor, not on real hardware yet.

## Windows one-click install

`Install to board.bat` runs `install-to-board.ps1`, which waits for the board, copies
CircuitPython onto `QTPY_BOOT` if needed, then copies `lib/` and `code.py` onto `CIRCUITPY`.
It expects two things in this folder that are not stored in the repository:

- `adafruit-circuitpython-qtpy_m0-en_US-10.3.1.uf2` from circuitpython.org
- a `lib/` folder holding `adafruit_veml7700.mpy`, `adafruit_register/` and `adafruit_bus_device/`
  from the CircuitPython library bundle (or run `circup install adafruit_veml7700` instead)
