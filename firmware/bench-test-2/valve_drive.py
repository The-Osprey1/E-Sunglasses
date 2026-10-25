# Bench test 2: the valve drive. code.py imports this and handles the commands.
# (Two files instead of one: the QT Py M0 compiles each file in its roughly 20 KB of
# memory, and one big file stops with a MemoryError before it runs.)
#
# The board drives the valve with the design's three-level wave (design-revision.md 4.1):
# A2 high for a pulse, both low, A3 high for an equal pulse, both low, 100 times a second.
# Both pulses run through the same code with the same count, so they last the same time
# and the average voltage across the valve is zero: no steady (direct) current.
# Voltage (root-mean-square) = 3.3 V x square root of D, where D is the fraction of the
# time either pin is high. It is an estimate from the 3.3 V supply, not a meter reading.

import supervisor
import board
import digitalio

SUPPLY = 3.3       # volts on a pin when it is high
VMAX = 3.2         # highest setting; leaves time between pulses for the board's other work

# Pins start low: 0 V across the valve, which leaves it in glare-cut.
pin_a = digitalio.DigitalInOut(board.A2)
pin_a.switch_to_output(value=False)
pin_b = digitalio.DigitalInOut(board.A3)
pin_b.switch_to_output(value=False)
PINS = (pin_a, pin_b)


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
    t0 = ticks()
    wait(50000)
    step = max(1, ms_since(t0)) / 50.0
    t0 = ticks()
    k = 3000
    while k:
        pulse_idle(pin_a, 0)
        k -= 1
    return step, ms_since(t0) / 3.0 - step   # less this loop's own step


runs = sorted([calibrate(), calibrate(), calibrate()])
step_us, call_us = runs[1]                   # the middle of three runs
spread = (runs[2][0] - runs[0][0]) / step_us
edge_us = call_us / 2   # part of a call's fixed cost that falls between the two edges

volts = 0.0        # setting asked for
freq = 100         # setting asked for
next_on = 0        # loop steps per pulse, for the next cycle
next_gap = 0       # loop steps per gap, for the next cycle
base_gap = 0       # gap from the plan, before the trim below
trim = 0           # learned gap correction (loop steps), kept across settings
pulse_us = 0.0     # estimated pulse width
period_us = 10000.0    # measured period
win_t0 = ticks()
win_cycles = 0
disturbed = False  # a long pause in this window: don't learn from it


def set_drive(v, f):
    global volts, freq, next_on, next_gap, base_gap, pulse_us
    volts, freq = v, f
    half = 500000.0 / f
    if v <= 0:
        next_on, pulse_us = 0, 0.0
        base_gap = int((half - call_us) / step_us)
    else:
        want = (v / SUPPLY) ** 2 * half
        next_on = max(1, int((want - edge_us) / step_us + 0.5))
        pulse_us = next_on * step_us + edge_us
        base_gap = int((half - pulse_us - 2 * call_us) / step_us)
    next_gap = max(0, base_gap + trim)


def volts_at(period):
    if next_on == 0:
        return 0.0
    return SUPPLY * min(1.0, 2.0 * pulse_us / period) ** 0.5


def regulate():
    # Once a second, nudge the gap so the measured period matches the frequency asked for.
    global win_t0, win_cycles, next_gap, trim, period_us, disturbed
    el = ms_since(win_t0)
    if el < 1000 or win_cycles == 0:
        return
    period = el * 1000.0 / win_cycles
    if not disturbed:
        period_us = period
        adj = int(0.5 * (1000000.0 / freq - period) / 2 / step_us)
        lim = next_gap // 10 + 2   # small steps, so one odd window can't swing it far
        trim += max(-lim, min(lim, adj))
        trim = max(trim, -max(base_gap, 0))   # no point trimming below a zero gap
        next_gap = max(0, base_gap + trim)
    win_t0 = ticks()
    win_cycles = 0
    disturbed = False


def run(between):
    # The drive loop. between() is called after each pulse, with both pins low:
    # anything slow there only lengthens a 0 V gap.
    global win_cycles, disturbed
    try:
        while True:
            # New settings start only here, so the two pulses of a cycle always match.
            n_on = next_on
            n_gap = next_gap
            for pin in PINS:
                if n_on:
                    pulse(pin, n_on)
                t0 = ticks()
                between()
                if ms_since(t0) > 2:
                    disturbed = True
                regulate()
                wait(n_gap)
            win_cycles += 1
    finally:
        pin_a.value = False
        pin_b.value = False
