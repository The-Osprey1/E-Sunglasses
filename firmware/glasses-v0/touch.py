# The two touch pads: A0 = darker, A1 = clearer. Wires on A0 and A1 are the pads.
# The pads settle to their resting reading as the board starts: don't touch them then.

import board
import touchio
import config

DEBOUNCE = 3       # readings in a row (30 ms) before a touch or a release counts
ALONE_MS = 250     # a single pad must stay down this long to count, so two fingers landing
                   # a moment apart are still read as a both-pad hold

pads = (touchio.TouchIn(board.A0), touchio.TouchIn(board.A1))
for _p in pads:
    _p.threshold = _p.raw_value + config.TOUCH_MARGIN

down = [False, False]   # which pads are touched, after debouncing
run = [0, 0]            # readings in a row that disagree with that
both_ms = 0
alone_ms = 0
latched = False         # the two-pad hold was handled: wait until both pads are let go


def poll(dt):
    # dt = milliseconds since the last call. Returns what the touch means right now:
    # 0 nothing, 1 darker pad alone, 2 clearer pad alone, 3 both pads held long enough.
    global both_ms, alone_ms, latched
    for i in (0, 1):
        raw = pads[i].value
        if raw != down[i]:
            run[i] += 1
            if run[i] >= DEBOUNCE:
                down[i] = raw
                run[i] = 0
        else:
            run[i] = 0
    dark, clear = down
    if dark and clear:
        both_ms += dt
        alone_ms = 0
        if both_ms >= config.BOTH_HOLD_S * 1000 and not latched:
            latched = True
            return 3
        return 0
    both_ms = 0
    if not dark and not clear:
        latched = False
        alone_ms = 0
        return 0
    if latched:
        return 0
    alone_ms += dt
    if alone_ms < ALONE_MS:
        return 0
    return 1 if dark else 2
