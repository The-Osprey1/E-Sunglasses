# Firmware

All programs run on the Adafruit QT Py M0 under CircuitPython.

| Folder | What it does | Roadmap phase |
|---|---|---|
| [`bench-test-1/`](bench-test-1/) | Measures glare-cut of an unpowered cell against polarized sunglasses | 1 |
| [`bench-test-2/`](bench-test-2/) | Drives the cell at a set voltage to look for screen mode, by eye | 2 |
| [`glasses-v0/`](glasses-v0/) | The glasses program: automatic shade from the light sensor, touch pads for manual shade or clear, monitor page | 3 |

Planned: the hardware-timed three-level drive, a watchdog and a sealed button option
(phase 3 onward).
