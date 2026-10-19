# E-Sunglasses

Glasses whose lenses switch between two modes at the press of a button:

- **Glare-cut**: works like polarized sunglasses, cutting reflected glare from roads,
  water and car hoods. This is also what the lenses fall back to with no power.
- **Screen mode**: lets polarized screen light through evenly, so phones, laptops and car
  displays stay readable at any angle.

The lenses use liquid crystal cells driven by a small CircuitPython board. The darkness in
screen mode is set by the drive voltage, so it can be tuned.

## Hardware

- Adafruit liquid crystal light valve cells (36 mm squares) for the first versions
- Adafruit QT Py M0 (SAMD21) running CircuitPython
- VEML7700 light sensor for bench measurements
- Nonprescription lenses only

## Plan

Get it working first, then make it small, and only then order lens-shaped cells.
Full criteria are in [docs/roadmap.md](docs/roadmap.md).

| Stage | Phase | Goal | Status |
|---|---|---|---|
| 1. Make it work | 1 | Glare-cut on the bench | In progress (bench test 1) |
| | 2 | Screen mode and drive on the bench (gate A) | Not started |
| | 3 | Wearable first version, clip-on electronics box (gate B) | Not started |
| 2. Miniaturize | 4 | Electronics into the right temple | Not started |
| 3. Final lenses | 5 | Quotes and order for lens-shaped cells (gate C) | Not started |
| | 6 | Final build and drop tests | Not started |
| | 7 | Full-day wear | Not started |

## Repository layout

| Folder | Holds |
|---|---|
| [`docs/`](docs/) | Roadmap and design revision (optics, drive electronics, safety, test plan) |
| [`firmware/`](firmware/) | CircuitPython programs, one folder per bench test and later the glasses firmware |
| [`hardware/`](hardware/) | Frame CAD and printable files; later the temple circuit board |

## Getting started

To run bench test 1, follow [firmware/bench-test-1/README.md](firmware/bench-test-1/README.md).
On Windows, `Install to board.bat` in that folder sets up the board in one step.
