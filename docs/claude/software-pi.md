# Software and Raspberry Pi setup

## Pi (kskpi1)
- School Raspberry Pi, hostname `kskpi1`. Teacher said Alan can do almost anything with it.
- Goal: wireless dev "server" – only a power cable, joins known Wi-Fi networks automatically.
  Wi-Fi: school network `campus-wlan`.
- Up to 3 people work on the code.
- Always-running service (set up 2026-11-05, starts on power-up, systemd name `marsrover`):
  pulls this repo every 5 seconds and runs the code when it changes. It stops running
  programs with SIGTERM and has no keyboard.
- They also code on the Pi using Thonny.

## Workflow (decided)
- Write code on the laptops (VS Code) → push to GitHub → leave the Pi off until code is done →
  Pi pulls and runs it.
- Mac clone: `~/Documents/GitHub/Marsrover`.
- Repo `alanmursalimov/Marsrover` is **public** (since 2026-11-05) so the Pi can pull without a token.

## Code structure
- Teacher's guidance: use a library for the rover code that `main.py` calls. Alan writes `main.py`
  himself; he doesn't need to understand the library code.
- `rover.py` – library for the Grove I2C Motor Driver v1.3 (German user guide in the docstring at the top).
  - `Rover(addresses=[0x0F], max_speed=60, invert_left=False, invert_right=False)`
  - Speed 0–100 = % of `max_speed` (not full battery voltage).
  - `drive(left, right, seconds=None)`, `forward`, `backward`, `turn_left`, `turn_right` (tank turn on the spot),
    `stop()`, `wait(s)`, `wasd(speed=50)` (W/A/S/D, space = stop, Q = quit).
  - Without `seconds`, motors keep running until the next command or until main.py ends (then they stop).
  - Wiring convention per driver: terminal **J1** (IN1/IN2 LEDs) = LEFT motor, **J5** (IN3/IN4) = RIGHT motor.
  - Safety: motors stop automatically on exit, crash, Ctrl+C or SIGTERM. Test with wheels in the air.
  - `wasd()` only works when main.py is started manually in a terminal:
    `sudo systemctl stop marsrover` then `python3 ~/Marsrover/main.py`.
  - Troubleshooting: "Motortreiber … antwortet nicht" → check Grove cable, run `i2cdetect -y 1`.
    Very slow / empty scan → a driver blocks the bus (like board no. 3) – unplug it.
- `main.py` – currently a test: `rover.drive(50, 0, seconds=3)` (only motor 1 / J1 turns).
