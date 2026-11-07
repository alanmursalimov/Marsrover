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
7. Check I2C addresses on the Pi (`i2cdetect -y 1`): PWM board (expected 0x7F), GrovePi (0x04).
   Check whether the `grovepi` library is installed. Calibrate servo pulse range (`min_us`/`max_us`) per servo.
8. Exact model of the 10 kg·cm servo (MG996R is only mentioned in earlier chats, not confirmed).
