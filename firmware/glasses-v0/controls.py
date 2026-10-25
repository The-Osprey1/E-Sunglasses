# Glasses controls: the shade level and its mode (automatic or manual).
# tick() is called from the drive loop (valve_drive.run) after every pulse, with both pins low,
# so nothing here can make the two pulses of a cycle different.
#
# Shade is a number from 0 (clear) to 1 (full shade). Touch pad A0 = darker, A1 = clearer.
#   Touch one pad:                the shade changes while you hold it (manual mode).
#   Hold both pads for 1 second:  switch between automatic and manual mode.
#                                 One blink of the lenses = manual, two blinks = automatic.

import config
import auto
import touch
import out
import valve_drive as drive

AUTO = 0
MANUAL = 1
NAMES = ("auto", "manual")

mode = AUTO
level = 0.0            # shade being asked for: 0 = clear, 1 = full shade
faulted = False
phase = False
t_last = drive.ticks()


def set_manual(x):
    global mode, level
    mode = MANUAL
    level = max(0.0, min(1.0, x))


def tick():
    global phase, t_last, mode, level
    phase = not phase
    if phase:
        return              # the drive loop calls twice per cycle: work 100 times a second
    now = drive.ticks()
    dt = min(drive.ms_since(t_last), 100)   # after a long pause, don't make the shade jump
    t_last = now

    t = touch.poll(dt)
    if t and not out.busy():
        if t == 3:
            out.blink(1 if mode == AUTO else 2, now)
            mode = 1 - mode
        else:
            mode = MANUAL
            step = config.MANUAL_PER_S * dt / 1000
            level = min(1.0, level + step) if t == 1 else max(0.0, level - step)

    auto.read(now)
    if mode == AUTO:
        level = auto.follow(level, dt)
    out.show(level)


def fault(e):
    # Something broke. Go clear and keep running, so the glasses stay usable by touch alone.
    global faulted, level
    level = 0.0
    out.clear()
    if not faulted:
        faulted = True
        print("FAULT:", repr(e))
