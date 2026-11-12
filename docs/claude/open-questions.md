# Still open

1. **Wheel up/down movement (Perseverance-style).** Alan said he'd abandon it, but is still considering it.
   Idea: 2 servos at the body-side rocker pivots (copied from another rover) instead of a complex
   multi-part printed arm. Known issues:
   - Worst-case torque ≈ 0.75 kg × 9.5 cm ≈ 7 kg·cm at 1.5 kg total (≈ 4.5 kg·cm at 1 kg).
     More than the usable continuous torque of the Reely (≈ half its stall torque); the 10 kg·cm servo only just covers it.
   - Likely fix: link rod with 2–3× mechanical gain (2 cm servo horn driving a 4–6 cm lever).
   - The two servos have different torque ratings – matters if used as a left/right pair.
   - A servo-held pivot is rigid → passive rocker-bogie suspension is lost. A spring could offload static weight.
   - The servo's bushing shaft must not carry structural load; use a bearing or printed bushing with a screw at the pivot.
   - Pivot-to-wheel distance (≈ 9–10 cm) was estimated from the old 7.5 cm wheel assumption → re-measure
     with the current wheels and leg design.
2. **Tank steering check:** turning drags fixed wheels sideways (now 6 wheels). Check turning force and
   traction on the surfaces that will be used.
3. **Motor power:** Li-ion vs AA packs (see electronics-power.md), plus a fuse holder.
4. **Verify the electronics list**, including the motor driver's supply voltage range.
5. **Wheel hub design and CAD** (Fusion). Leg sketch in progress.
6. Second motor driver: only board no. 2 (0x0F) is confirmed working; a second working board/address
   is needed for 4 motors.
7. I2C scan 2026-11-10 (`i2cdetect -y -a 1`): **04** (GrovePi), **0f** (motor driver no. 2), **70** (probably the
   TCA9548A hub). **7f missing** → PWM board not seen. Likely reason: it sits behind the TCA9548A hub, which hides all its ports
   until one is switched on (`servotest.py` now does that) – not confirmed on the Pi yet.
   Servo turns now (2026-11-12), but angles don't match the commanded degrees → calibrate `min_us`/`max_us`.
   Check whether the `grovepi` library is installed. Calibrate servo pulse range (`min_us`/`max_us`) per servo.
8. Exact model of the 10 kg·cm servo (MG996R is only mentioned in earlier chats, not confirmed).
9. **Motor drivers stop answering (2026-11-10).** Left driver = **board no. 4**, right driver = **board no. 2**
   (both work earlier). Both have their 4 DIP switches in the same position (from photos) → probably both 0x0F →
   one must get a different address before using both.
   Observed: right board alone → fast but empty scan; both → very slow scan; with the drivers unplugged the scan is
   normal again (04 back).
   Battery measured (2026-11-10, no load): one pack about 7.7 V, the other 6.67 V (≈3.3 V/cell, nearly empty).
   Which pack feeds which board: not recorded yet. Hypothesis: below about 7 V the 78M05 on the driver can't hold 5 V
   → that board's logic is unstable and can drag the bus down. Both boards on the same address (0x0F) could also
   explain the slow scan with both plugged in. Neither confirmed yet.
   Later: board no. 4 alone (7.7 V pack) first gave a fast but empty scan (04 gone too), then after a while it was
   recognized again – cause unknown. Untested idea if it keeps happening: lower I2C speed
   (`dtparam=i2c_arm_baudrate=50000` in `/boot/firmware/config.txt`; Pi vs. ATmega8 clock stretching – hypothesis).
   Last test of the day: the BACK RIGHT motor turned and the left ones didn't, although board no. 4 is the left driver
   → check wiring (which motor is on which board/terminal) and the `rover.motor(...)` lines in main.py. Alan checks 2026-11-11.
   If confirmed, board no. 3 was probably not faulty either (same symptom) → retest it.
   Also note: speed 50 with `max_speed=60` is only 30 % duty – may be too little to start (estimate).
10. **Servo power + motor drivers crashing (2026-11-12).** Servo powerbank switches off at low current. Every time Alan
    presses its button to turn it back on, the motor drivers lose the I2C connection and need RESET.
    Hypothesis (not confirmed): all servos jump to position at once → current spike / ground bounce → the drivers'
    ATmega8 I2C firmware hangs. Test: press the button with the servos unplugged – do the drivers still crash?
    Ideas: separate servo supply without auto-off (e.g. 4×AA), big electrolytic capacitor across servo Power In.
