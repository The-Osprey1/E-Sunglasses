# Turns the shade level into a valve voltage, and shows the mode-change blink.

import config
import valve_drive as drive

BLINK_MS = 150     # half of one blink

n = 0              # blinks to show (0 = none)
t0 = 0
last_v = -1.0


def blink(count, now):
    global n, t0
    n = count
    t0 = now


def busy():
    # True while a blink is showing.
    return n and drive.ms_since(t0) < 2 * BLINK_MS * n


def show(level):
    # Called every tick. Sends the shade to the drive, changing it only when it moved.
    global n, last_v
    if n and drive.ms_since(t0) >= 2 * BLINK_MS * n:
        n = 0
    if n and (drive.ms_since(t0) // BLINK_MS) % 2 == 0:
        level = level + 0.4 if level < 0.5 else level - 0.4
    v = 0.0
    if level >= 0.01:
        v = min(drive.VMAX, config.VOLTS_START + (config.VOLTS_DARK - config.VOLTS_START) * level)
    if abs(v - last_v) >= 0.01 or (v == 0.0) != (last_v == 0.0):
        last_v = v
        drive.set_drive(v, config.FREQ_HZ)


def clear():
    global last_v
    last_v = 0.0
    drive.set_drive(0.0, config.FREQ_HZ)
