# Bench test 2: light valve with power on (screen mode), eye check
# QT Py SAMD21, CircuitPython. Light valve wires on A2 and A3 (either way round).
# The light sensor isn't used. The drive itself is in valve_drive.py.
#
# Commands (type, then Enter):
#   v VOLTS   drive the valve at this voltage, 0 to 3.2. "v 0" turns it off.
#   v         show the drive: estimated voltage, measured frequency
#   f HZ      drive frequency, 30 to 300 (starts at 100)
#   h         help

import sys
import supervisor

try:
    supervisor.status_bar.console = False   # keep title-bar codes out of the serial text
except AttributeError:
    pass

import valve_drive as drive   # sets both pins low, then times its loops (about 1 second)


def show_drive(measured):
    if measured:
        print("  valve = %.2f V (estimate) at %.1f Hz (measured)" % (
            drive.volts_at(drive.period_us), 1000000.0 / drive.period_us))
    else:
        f = drive.freq
        print("  valve = %.2f V at %d Hz" % (drive.volts_at(1000000.0 / f), f))


def help_text():
    print("v VOLTS = drive the valve (0 to %.1f), v = show the drive, f HZ = frequency, h = help" % drive.VMAX)


def run_command(cmd):
    key = cmd[0].lower()
    try:
        x = float(cmd[1:].strip()) if cmd[1:].strip() else None
    except ValueError:
        x = -1
    if key == "v" and x is None:
        show_drive(True)
    elif key == "v":
        if 0 <= x <= drive.VMAX:
            drive.set_drive(x, drive.freq)
            show_drive(False)
        else:
            print("  Give a voltage from 0 to %.1f, like: v 1.8" % drive.VMAX)
    elif key == "f":
        if x is not None and 30 <= x <= 300:
            drive.set_drive(drive.volts, int(x))
            show_drive(False)
        else:
            print("  Give a frequency from 30 to 300, like: f 100")
    else:
        help_text()


line = ""


def poll_serial():
    # Collects typed characters without stopping the drive. Runs a command on Enter.
    # CircuitPython hands over Enter as "\n" (it turns "\r" into "\n").
    global line
    while supervisor.runtime.serial_bytes_available:
        ch = sys.stdin.read(1)
        if ch == "\n" or ch == "\r":
            sys.stdout.write("\r\n")
            cmd = line.strip()
            line = ""
            if cmd:
                run_command(cmd)
            sys.stdout.write("> ")
        elif ch == "\x08" or ch == "\x7f":
            if line:
                line = line[:-1]
                sys.stdout.write("\x08 \x08")
        elif " " <= ch <= "~":
            line += ch
            sys.stdout.write(ch)


drive.set_drive(0.0, 100)
print("\nBench test 2: light valve with power on")
print("Drive pins A2 and A3. Loop step %.2f us, pulse call %.1f us." % (drive.step_us, drive.call_us))
if drive.spread > 0.03:
    print("WARNING: the timing check varied by %d%%. Voltages may be off." % (drive.spread * 100))
help_text()
sys.stdout.write("> ")
drive.run(poll_serial)
