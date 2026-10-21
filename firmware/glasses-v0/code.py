# Glasses: automatic shade, with touch pads to override it. See README.md.
# QT Py M0. Valves on A2 and A3, light sensor on the STEMMA QT port, touch pad wires on
# A0 (darker) and A1 (clearer). Settings are in config.py.

import gc
import supervisor

try:
    supervisor.status_bar.console = False   # keep title-bar codes out of the serial text
except AttributeError:
    pass

# The board compiles each file in its small memory, so the parts are loaded one at a time,
# the biggest first, clearing out leftovers before each.
gc.collect()
import valve_drive as drive    # sets both pins low, then times its loops (about 1 second)
gc.collect()
import console
gc.collect()
import touch
gc.collect()
import auto
gc.collect()
import config
gc.collect()
import out
gc.collect()
import controls
gc.collect()
import light

print("\nGlasses: automatic shade, touch pads A0 darker and A1 clearer")
print("Loop step %.2f us, pulse call %.1f us." % (drive.step_us, drive.call_us))
if drive.spread > 0.03:
    print("WARNING: timing check varied by %d%%" % (drive.spread * 100))
drive.set_drive(0.0, config.FREQ_HZ)
try:
    light.start()
except OSError:
    print("No answer from the light sensor: automatic mode stays clear (touch still works)")


def between():
    # Called by the drive loop after each pulse, with both valve pins low.
    try:
        console.poll()
    except Exception as e:
        console.line = ""
        print("console error:", repr(e))
    try:
        controls.tick()
    except Exception as e:
        controls.fault(e)


gc.collect()
drive.run(between)
