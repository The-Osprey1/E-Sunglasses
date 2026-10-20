# Bench test 2: light valve with power on (screen mode)
# QT Py SAMD21, CircuitPython. Light valve wires on A2 and A3 (either way round).
# The VEML7700 light sensor on the STEMMA QT cable is optional: the eye check needs none.
#
# The board drives the valve with the design's three-level wave (design-revision.md 4.1):
# A2 high for a pulse, both low, A3 high for an equal pulse, both low, 100 times a second.
# Both pulses run through the same code, so they are equal and the average voltage across
# the valve is zero: no steady (direct) current. Both pins low shorts the valve to 0 V.
# Voltage (root-mean-square) = 3.3 V x square root of D, where D is the fraction of the
# time either pin is high. The pulses are timed by counted loops, calibrated at start-up.
#
# Commands (type, then Enter):
#   v VOLTS   drive the valve at this voltage, 0 to 3.2. "v 0" turns it off.
#   v         show the voltage and frequency actually running (measured)
#   f HZ      drive frequency, 30 to 300 (starts at 100)
#   m         one light reading in sensor counts (for voltage scans)
#   d, r, s NAME, t, c   dark, reference, sweep, table, CSV: as in bench test 1,
#             with the valve driven at the voltage set by v
#   h         help

import sys
import supervisor
import board
import digitalio

SUPPLY = 3.3       # volts on a pin when it is high
VMAX = 3.2         # highest setting; leaves time between pulses for the board's other work
STEP = 15          # sweep: degrees between readings
SAMPLES = 5        # readings averaged per point
SAMPLE_MS = 120    # one sensor integration period plus margin
FULL = 65535       # sensor saturates here

try:
    supervisor.status_bar.console = False   # keep title-bar codes out of the serial text
except AttributeError:
    pass

# Pins start low: 0 V across the valve, which leaves it in glare-cut.
pin_a = digitalio.DigitalInOut(board.A2)
pin_a.switch_to_output(value=False)
pin_b = digitalio.DigitalInOut(board.A3)
pin_b.switch_to_output(value=False)

veml = None
try:
    import adafruit_veml7700
    i2c = board.STEMMA_I2C() if hasattr(board, "STEMMA_I2C") else board.I2C()
    veml = adafruit_veml7700.VEML7700(i2c)
    veml.light_gain = veml.ALS_GAIN_1
    veml.light_integration_time = veml.ALS_100MS
except Exception:   # no sensor plugged in, or no library: eye checks still work
    veml = None


def ticks():
    return supervisor.ticks_ms()


def ms_since(t0):
    return (supervisor.ticks_ms() - t0) & 0x1FFFFFFF   # ticks_ms wraps at 2**29


def wait(n):
    while n:
        n -= 1


def pulse(pin, n):
    # Both pulses go through this one function, so they last the same time.
    pin.value = True
    while n:
        n -= 1
    pin.value = False


def pulse_idle(pin, n):
    # Same work as pulse(), but the pin stays low. Used only to time pulse().
    pin.value = False
    while n:
        n -= 1
    pin.value = False


def calibrate():
    # Microseconds per loop step, and the fixed cost of one pulse() call.
    n = 60000
    t0 = ticks()
    wait(n)
    step_us = ms_since(t0) * 1000.0 / n
    calls = 4000
    t0 = ticks()
    k = calls
    while k:
        pulse_idle(pin_a, 0)
        k -= 1
    call_us = ms_since(t0) * 1000.0 / calls - step_us   # less this loop's own step
    return step_us, call_us


step_us, call_us = calibrate()
edge_us = call_us / 2   # part of a call's fixed cost that falls between the two edges

volts = 0.0        # setting asked for
freq = 100         # setting asked for
n_on = 0           # loop steps per pulse, in use
n_gap = 0          # loop steps per gap, in use
next_on = 0        # settings take effect at the start of the next cycle
next_gap = 0
pulse_us = 0.0     # estimated pulse width, in use
period_us = 10000.0    # measured period
win_t0 = ticks()
win_cycles = 0


def plan(v, f):
    # Loop counts for voltage v at frequency f. Returns (n_on, n_gap, pulse_us).
    half = 500000.0 / f
    if v <= 0:
        return 0, max(0, int((half - call_us) / step_us)), 0.0
    d = (v / SUPPLY) ** 2
    want = d * half
    n1 = max(1, int((want - edge_us) / step_us + 0.5))
    width = n1 * step_us + edge_us
    n2 = max(0, int((half - width - 2 * call_us) / step_us))
    return n1, n2, width


def actual_volts():
    if n_on == 0:
        return 0.0
    d = min(1.0, 2.0 * pulse_us / period_us)
    return SUPPLY * d ** 0.5


def regulate():
    # Once a second, nudge the gap so the measured period matches the frequency asked for.
    global win_t0, win_cycles, next_gap, period_us
    el = ms_since(win_t0)
    if el < 1000 or win_cycles == 0:
        return
    period_us = el * 1000.0 / win_cycles
    err = 1000000.0 / freq - period_us
    adj = int(0.6 * err / 2 / step_us)
    next_gap = max(0, next_gap + adj)
    win_t0 = ticks()
    win_cycles = 0


# ---------- light readings (taken between pulses, so the drive keeps running) ----------
dark = 0.0
ref = None
sweeps = []        # (name, volts, [(angle, percent), ...])
meas_kind = None   # what the reading is for: "d", "r", "m", "s"
meas_left = 0
meas_total = 0.0
meas_peak = 0
meas_t0 = 0
sweep_name = None
sweep_angle = 0
sweep_points = []


def start_reading(kind):
    global meas_kind, meas_left, meas_total, meas_peak, meas_t0
    meas_kind = kind
    meas_left = SAMPLES
    meas_total = 0.0
    meas_peak = 0
    meas_t0 = ticks()


def step_reading():
    # Called between pulses. Takes one sample when it is due.
    global meas_left, meas_total, meas_peak, meas_t0, meas_kind
    if ms_since(meas_t0) < SAMPLE_MS:
        return
    meas_t0 = ticks()
    v = veml.light
    meas_total += v
    meas_peak = max(meas_peak, v)
    meas_left -= 1
    if meas_left == 0:
        kind = meas_kind
        meas_kind = None
        if meas_peak >= FULL - 100:
            print("  WARNING: sensor saturated. Dim the screen and redo the reference.")
        finish_reading(kind, meas_total / SAMPLES)


def finish_reading(kind, value):
    global dark, ref, sweep_angle
    if kind == "d":
        dark = value
        print("  dark = %.0f counts" % dark)
    elif kind == "r":
        ref = value
        print("  reference = %.0f counts (100%%)" % ref)
        if ref - dark < 500:
            print("  WARNING: reference is weak. Brighten the screen or block room light.")
    elif kind == "m":
        print("  light = %.0f counts at %.2f V" % (value - dark, actual_volts()))
    elif kind == "s":
        pct = 100.0 * (value - dark) / (ref - dark)
        sweep_points.append((sweep_angle, pct))
        print("  %3d deg  %6.1f %%" % (sweep_angle, pct))
        sweep_angle += STEP
        if sweep_angle > 180:
            end_sweep()
            return
        prompt()
        return
    prompt()


def prompt():
    if sweep_name is not None:
        sys.stdout.write("  %3d deg > " % sweep_angle)
    else:
        sys.stdout.write("> ")


def start_sweep(name):
    global sweep_name, sweep_angle, sweep_points
    if veml is None:
        print("No light sensor found. Plug it in with the STEMMA QT cable and restart.")
        return
    if ref is None or ref - dark <= 0:
        print("Take a reference first (r), brighter than the dark reading.")
        return
    print("Sweep '%s' at %.2f V. Rotate the sample to each angle, then press Enter." % (
        name, actual_volts()))
    print("Type q and Enter to stop early.")
    sweep_name = name
    sweep_angle = 0
    sweep_points = []


def end_sweep():
    global sweep_name, sweep_points
    if sweep_points:
        sweeps.append((sweep_name, actual_volts(), sweep_points))
        summarize(sweep_name, actual_volts(), sweep_points)
    sweep_name = None
    sweep_points = []
    prompt()


def summarize(name, v, points):
    lo = min(points, key=lambda p: p[1])
    hi = max(points, key=lambda p: p[1])
    print("  %-14s %.2f V  low %5.1f%% at %3d  high %5.1f%% at %3d" % (
        name, v, lo[1], lo[0], hi[1], hi[0]))
    if hi[1] > 0:
        ratio = lo[1] / hi[1]
        print("  %-14s dimmest / brightest = %.2f  screen mode (0.5 or more) %s" % (
            "", ratio, "PASS" if ratio >= 0.5 else "FAIL"))


def table():
    if not sweeps:
        print("No sweeps yet.")
        return
    print("Screen mode passes when dimmest / brightest is 0.5 or more.")
    for name, v, points in sweeps:
        summarize(name, v, points)


def csv():
    print("sweep,volts,angle_deg,percent")
    for name, v, points in sweeps:
        for a, p in points:
            print("%s,%.2f,%d,%.2f" % (name, v, a, p))


def help_text():
    print("v VOLTS = drive the valve (0 to %.1f), v = show drive, f HZ = frequency," % VMAX)
    print("m = one reading, d = dark, r = reference, s NAME = sweep, t = table, c = CSV, h = help")


def number(text):
    try:
        return float(text)
    except ValueError:
        return None


def set_drive(v, f):
    global volts, freq, next_on, next_gap, pulse_us
    volts, freq = v, f
    next_on, next_gap, pulse_us = plan(v, f)


def show_drive(measured):
    if measured:
        print("  valve = %.2f V at %.1f Hz (measured)" % (actual_volts(), 1000000.0 / period_us))
    else:
        v = SUPPLY * min(1.0, 2.0 * pulse_us * freq / 1000000.0) ** 0.5 if next_on else 0.0
        print("  valve = %.2f V at %d Hz" % (v, freq))


def run_command(cmd):
    # Returns True when the command has printed its own prompt or will print it later
    # (a reading prints it when done).
    if sweep_name is not None:
        if cmd.lower() == "q":
            end_sweep()
            return True
        start_reading("s")
        return True
    if not cmd:
        return False
    key = cmd[0].lower()
    arg = cmd[1:].strip()
    if key == "v":
        if not arg:
            show_drive(True)
            return False
        v = number(arg)
        if v is None or v < 0 or v > VMAX:
            print("  Give a voltage from 0 to %.1f, like: v 1.8" % VMAX)
            return False
        set_drive(v, freq)
        show_drive(False)
    elif key == "f":
        f = number(arg)
        if f is None or f < 30 or f > 300:
            print("  Give a frequency from 30 to 300, like: f 100")
            return False
        set_drive(volts, int(f))
        show_drive(False)
    elif key in "dmr" and veml is None:
        print("No light sensor found. Plug it in with the STEMMA QT cable and restart.")
    elif key in "dmr":
        start_reading(key)
        return True
    elif key == "s":
        start_sweep(arg or "sweep%d" % (len(sweeps) + 1))
        if sweep_name is not None:
            prompt()
            return True
    elif key == "t":
        table()
    elif key == "c":
        csv()
    else:
        help_text()
    return False


line = ""
pending = ""       # characters received but not handled yet
last_cr = False


def poll_serial():
    # Collects typed characters without stopping the drive. Runs a command on Enter.
    global line, pending, last_cr
    n = supervisor.runtime.serial_bytes_available
    if n:
        pending += sys.stdin.read(n)
    while pending and meas_kind is None:
        ch = pending[0]
        pending = pending[1:]
        if ch == "\n" and last_cr:
            last_cr = False
            continue
        last_cr = ch == "\r"
        if ch in "\r\n":
            sys.stdout.write("\r\n")
            cmd = line.strip()
            line = ""
            if not run_command(cmd):
                prompt()
        elif ch in "\x08\x7f":
            if line:
                line = line[:-1]
                sys.stdout.write("\x08 \x08")
        elif ch >= " ":
            line += ch
            sys.stdout.write(ch)


def housekeeping():
    # Runs between pulses, with both pins low. Anything slow here only lengthens a gap.
    if meas_kind is not None:
        step_reading()
    else:
        poll_serial()
    regulate()


set_drive(0.0, freq)
print("\nBench test 2: light valve with power on")
print("Drive pins A2 and A3. Loop step %.2f us, pulse call %.1f us." % (step_us, call_us))
if veml is None:
    print("No light sensor found: eye checks only.")
help_text()
prompt()

try:
    while True:
        # New settings start only here, so the two pulses of a cycle always match.
        n_on = next_on
        n_gap = next_gap
        if n_on:
            pulse(pin_a, n_on)
        housekeeping()
        wait(n_gap)
        if n_on:
            pulse(pin_b, n_on)
        housekeeping()
        wait(n_gap)
        win_cycles += 1
finally:
    pin_a.value = False
    pin_b.value = False
