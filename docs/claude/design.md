# Mechanical design (current state)

## Chassis / body
- Hollow 3D-printed PETG box, about 17 × 10 × 8 cm, 2.5 mm walls (about 235 g).
- Holds all electronics and the battery (Pi 4, GrovePi, drivers, servos). Nothing electronic goes in the wheels.
- The body sits on the "legs" parts, which slide up into a small box/slot on each side of the body.

## Legs (as of 2026-10-29)
- Each motor is screwed to a separate printed bracket on each leg.
- The legs part slides onto the existing top box/body.
- Alan is drawing a more accurate sketch.
- Material: PETG or PLA (ABS only if needed), about 40% infill.

## Drive
- Layout (as of 2026-10-29): **6 wheels, 4 motors** (one motor at each corner).
  The middle wheel on each side has no motor and spins freely on a printed adapter with an M3 screw.
- Motors: 4 × Dagu DG01D 48:1 mini DC gearbox motors – rated 4.5 V, about 140 rpm no-load,
  0.8 kg·cm torque (cheap motors → plan on roughly 40% continuous), 190 mA typical / 250 mA max, 30 g each.
- Wheels: rubber wheels, **67.3 mm diameter** (supersedes the earlier 62 mm figure), mounted
  directly on the white plastic D-shaft of the gearbox (direct drive).
- Wheels should sit close to the gearbox housing to avoid stressing the plastic shaft.

## Steering
- Tank style (skid steering): fixed wheels, left and right sides driven separately.
  Chosen because it's simpler; car-like steering is off the table.

## Weight
- Target about 1 kg, maximum 1.5 kg.
- Earlier estimate of about 950–1000 g assumed 4 servos; there are now only 2.

## Control
- Raspberry Pi 4 + GrovePi, driven from the keyboard with WASD. Speed should stay slow.

## CAD
- Alan prefers Fusion. Wheel hub design and CAD still to do (see open-questions.md).

## Calculations so far (rough estimates)
- Flat ground: 4 motors give about 4–5× force reserve (about 3.9 N continuous traction).
- A short 20° ramp is possible; continuous climbing would overheat the motors.
- Top speed about 0.3 m/s at about 100 rpm under load.
- Note: these were done with the earlier 62 mm wheel and 4-wheel assumption.
