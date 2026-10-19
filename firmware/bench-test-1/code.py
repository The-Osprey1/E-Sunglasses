# Bench test 1: glare-cut with no power
# QT Py SAMD21 + VEML7700 light sensor (STEMMA QT cable), CircuitPython.
#
# Open the serial console (Mu, Thonny, or any serial terminal), then type commands:
#   d         dark reading: block the sensor tube, measures leftover room light
#   r         reference: nothing in the way, screen showing the test color = 100%
#   s NAME    sweep a sample through 0..180 degrees in 15 degree steps
#             (put white, red or blue in NAME, e.g. "s cell-white", "s sun-red")
#   t         summary table of every sweep, with pass marks
#   c         print every reading as CSV (copy it into the project thread)
#   h         help
# Take a new reference (r) every time you change the screen color.

import time
import board
import adafruit_veml7700

STEP = 15          # degrees between readings
SAMPLES = 5        # readings averaged per point
FULL = 65535       # sensor saturates here

i2c = board.STEMMA_I2C() if hasattr(board, "STEMMA_I2C") else board.I2C()
veml = adafruit_veml7700.VEML7700(i2c)
# Fixed gain and timing so readings stay proportional to light.
veml.light_gain = veml.ALS_GAIN_1
veml.light_integration_time = veml.ALS_100MS

dark = 0.0
ref = None
sweeps = []        # (name, ref, [(angle, percent), ...])


def read_avg():
    total = 0
    peak = 0
    for _ in range(SAMPLES):
        time.sleep(0.12)   # one integration period
        v = veml.light
        total += v
        peak = max(peak, v)
    if peak >= FULL - 100:
        print("  WARNING: sensor saturated. Dim the screen and redo the reference.")
    return total / SAMPLES


def limit_low(name):
    # Pass mark for the lowest reading (glare getting through), in percent.
    return 5.0 if "white" in name else 10.0


def do_sweep(name):
    if ref is None or ref - dark <= 0:
        print("Take a reference first (r), brighter than the dark reading.")
        return
    print("Sweep '%s'. Rotate the sample to each angle, then press Enter." % name)
    print("Type q and Enter to stop early.")
    points = []
    angle = 0
    while angle <= 180:
        if input("  %3d deg > " % angle).strip().lower() == "q":
            break
        pct = 100.0 * (read_avg() - dark) / (ref - dark)
        points.append((angle, pct))
        print("  %3d deg  %6.1f %%" % (angle, pct))
        angle += STEP
    if points:
        sweeps.append((name, ref, points))
        summarize(name, points)


def summarize(name, points):
    lo = min(points, key=lambda p: p[1])
    hi = max(points, key=lambda p: p[1])
    lo_ok = lo[1] <= limit_low(name)
    hi_ok = hi[1] >= 70.0
    print("  %-14s low %5.1f%% at %3d  high %5.1f%% at %3d  low %s  high %s" % (
        name, lo[1], lo[0], hi[1], hi[0],
        "PASS" if lo_ok else "FAIL", "PASS" if hi_ok else "FAIL"))
    if lo[1] > 0:
        print("  %-14s contrast (high / low) %.0f : 1" % ("", hi[1] / lo[1]))


def table():
    if not sweeps:
        print("No sweeps yet.")
        return
    print("Pass marks: low <= 5% (white) or <= 10% (red, blue); high >= 70%.")
    print("Also compare each cell sweep with the sunglasses sweep of the same color:")
    print("the cell's low should be no more than 2 points worse.")
    for name, _, points in sweeps:
        summarize(name, points)


def csv():
    print("sweep,angle_deg,percent")
    for name, _, points in sweeps:
        for a, p in points:
            print("%s,%d,%.2f" % (name, a, p))


def help_text():
    print("d = dark, r = reference, s NAME = sweep, t = table, c = CSV, h = help")


print("\nBench test 1: glare-cut with no power")
help_text()
while True:
    try:
        cmd = input("> ").strip()
    except EOFError:
        break
    if not cmd:
        continue
    key = cmd[0].lower()
    if key == "d":
        dark = read_avg()
        print("  dark = %.0f counts" % dark)
    elif key == "r":
        ref = read_avg()
        print("  reference = %.0f counts (100%%)" % ref)
        if ref - dark < 500:
            print("  WARNING: reference is weak. Brighten the screen or block room light.")
    elif key == "s":
        name = cmd[1:].strip() or "sweep%d" % (len(sweeps) + 1)
        do_sweep(name)
    elif key == "t":
        table()
    elif key == "c":
        csv()
    else:
        help_text()
