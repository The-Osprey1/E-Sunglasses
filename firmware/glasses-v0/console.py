# Typed commands over USB, for tuning at the bench. They never stop the drive.
#   s            show the state once
#   mon 1        show the state twice a second (mon 0 stops it); the monitor page uses this
#   auto         automatic mode
#   m X          manual shade, 0 (clear) to 1 (full shade)
#   lux A B      stay clear up to A lux, full shade from B lux (lasts until the board restarts;
#                put the numbers you like in config.py to keep them)
# The state line: mode, light, shade, volts (estimate), pads touched (A0 A1), pad readings
# now/needed (A0 A1), whether the light sensor answers, the board's free memory in bytes, the
# two lux settings in use (clear up to / full shade from) and whether a fault was caught (0 or 1).

import gc
import sys
import supervisor
import config
import valve_drive as drive

# auto, touch and controls are imported inside the functions that use them: that way this module
# can be loaded early (while the board has the most free memory) and the others after it.

line = ""
streaming = False
t_mon = 0


def status():
    import auto, touch, controls as ctl
    a, b = touch.pads
    return "S %s lux=%d shade=%.2f volts=%.2f pads=%d%d raw=%d/%d,%d/%d sensor=%s free=%d lo=%d hi=%d fault=%d" % (
        ctl.NAMES[ctl.mode], auto.lux, ctl.level, drive.volts_at(drive.period_us),
        touch.down[0], touch.down[1], a.raw_value, a.threshold, b.raw_value, b.threshold,
        "ok" if auto.ok else "missing", gc.mem_free(), config.CLEAR_LUX, config.DARK_LUX, ctl.faulted)


def run_command(cmd):
    global streaming
    import controls as ctl
    w = cmd.split()
    try:
        if w[0] == "s":
            print(status())
        elif w[0] == "mon":
            streaming = w[1] == "1"
        elif w[0] == "auto":
            ctl.mode = ctl.AUTO
        elif w[0] == "m":
            ctl.set_manual(float(w[1]))
        elif w[0] == "lux" and 1 <= float(w[1]) < float(w[2]) < 1e7:
            config.CLEAR_LUX = float(w[1])
            config.DARK_LUX = float(w[2])
        else:
            raise ValueError
    except (ValueError, IndexError):
        print("s, mon 1, mon 0, auto, m 0-1, lux A B")


def poll():
    # Collects typed characters. CircuitPython hands over Enter as "\n".
    global line, t_mon
    while supervisor.runtime.serial_bytes_available:
        ch = sys.stdin.read(1)
        if ch == "\n" or ch == "\r":
            if line.strip():
                run_command(line)
            line = ""
        elif " " <= ch <= "~":
            line += ch
    if streaming and drive.ms_since(t_mon) >= 500:
        t_mon = drive.ticks()
        print(status())
