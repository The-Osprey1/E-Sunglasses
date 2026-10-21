# Glasses settings. Open this file in Notepad, change a number, and save. The board restarts
# by itself and uses the new numbers. (Don't add anything except numbers after the = signs.)

# How dark the valves get
VOLTS_START = 1.0    # the valve starts to darken at about 1 V (Adafruit's figure)
VOLTS_DARK = 3.2     # volts at full shade. 3.2 is the most this board can give.
FREQ_HZ = 100        # how many times a second the valve is pulsed

# Automatic mode
CLEAR_LUX = 2500     # at or below this light level the lenses stay clear
DARK_LUX = 30000     # at or above this light level the lenses go to full shade
MAX_SHADE = 1.0      # the darkest automatic mode may go: 0 = never darken, 1 = full shade
DARKEN_PER_S = 0.5   # how fast it darkens (1.0 = the whole range in 1 second)
CLEAR_PER_S = 0.15   # how fast it lightens again (slower, so passing shade doesn't flicker)

# Touch pads (A0 = darker, A1 = clearer)
MANUAL_PER_S = 0.5   # how fast a held pad changes the shade (0.5 = whole range in 2 seconds)
BOTH_HOLD_S = 1.0    # hold both pads this long to switch between automatic and manual
TOUCH_MARGIN = 100   # how far above its resting reading a pad must go to count as touched
