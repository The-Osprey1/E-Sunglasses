# Automatic brightness: reads the light sensor and turns the light level into a shade.

import config
import light
import valve_drive as drive

SENSOR_MS = 250    # how often the light sensor is read
RETRY_MS = 5000    # how often the sensor's settings are sent again

lux = 0.0          # light level in lux, smoothed
ok = False         # the sensor is answering
bad = 0            # reads in a row that failed
t_read = drive.ticks()
t_retry = t_read


def log2(x):
    # Base-2 logarithm for x >= 1, worked out by hand because the board's build may lack
    # the math module. Halve until between 1 and 2, then a short series for the rest.
    n = 0
    while x >= 2.0 and n < 130:
        x /= 2.0
        n += 1
    z = (x - 1.0) / (x + 1.0)
    z2 = z * z
    return n + 2.8853901 * z * (1.0 + z2 / 3.0 + z2 * z2 / 5.0 + z2 * z2 * z2 / 7.0)


def shade_for(x):
    # Light level to shade: clear up to CLEAR_LUX, full shade from DARK_LUX, and in between
    # it follows the logarithm of the light (the eye judges brightness that way).
    lo = max(config.CLEAR_LUX, 1)
    if x <= lo:
        return 0.0
    span = log2(max(config.DARK_LUX, lo * 1.01) / lo)
    return min(1.0, log2(x / lo) / span) * config.MAX_SHADE


def target():
    # No light reading: clear, which is the safe state.
    return shade_for(lux) if ok else 0.0


def follow(level, dt):
    # Moves the shade level toward the light's target by at most one small step (dt in ms).
    delta = target() - level
    step = (config.DARKEN_PER_S if delta > 0 else config.CLEAR_PER_S) * dt / 1000
    if abs(delta) <= step:
        return level + delta
    return level + step if delta > 0 else level - step


def read(now):
    # Reads the sensor when it's time. Returns True if the sensor just started or stopped answering.
    global lux, ok, bad, t_read, t_retry
    if drive.ms_since(t_read) < SENSOR_MS:
        return False
    t_read = now
    try:
        x = light.read()
    except OSError:
        x = None
    if drive.ms_since(t_retry) >= RETRY_MS:
        t_retry = now
        try:
            light.start()    # also puts the settings back if the sensor was unplugged and restarted
        except OSError:
            pass
    if x is None:
        bad += 1
        if ok and bad >= 8:
            ok = False
            return True
        return False
    bad = 0
    if ok:
        lux += (x - lux) * 0.4
        return False
    lux = x
    ok = True
    return True
