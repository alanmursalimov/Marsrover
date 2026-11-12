# Electronics and power

## Electronics list (NOT fully verified yet – double-check with Alan)
- Raspberry Pi 4 + GrovePi.
- Grove I2C Motor Driver v1.3 boards: 4 on hand, DIP switches for addresses, 2 needed for 4 motors.
  - Boards are numbered with stickers.
  - **Board no. 3 hangs the I2C bus** (even with a different cable) – possibly not faulty after all, see open-questions.md #9.
  - **Board no. 2 works** (address 0x0F) – now used as the RIGHT driver. **Board no. 4** = LEFT driver (left motors turned on 2026-11-10).
  - Address is set with a 4-way DIP switch (SW1) on each board. Default 0x0F.
    The board only reads the switches at start-up → after changing them press **RESET** (or disconnect the battery too;
    the logic runs from the motor battery, so switching off only the Pi is not enough).
    Tested 2026-11-11 on board no. 2: switch 1 flipped → 0x07 (switch 1 = 0x08 bit, 0x07 is I2C-reserved);
    switch 4 flipped instead → **0x0E** (switch 4 = 0x01 bit). Board no. 2 is now set to 0x0E.
    With it the scan also shows `00` (general call – probably the driver's firmware answering it; harmless).
- Grove 16-channel PWM driver (PCA9685) for servos. Address **0x7F** (printed on the back). Connected via the I2C hub
  and to a battery (2026-11-12) – which battery/voltage feeds the servo supply: not recorded yet.
- Grove 8-channel I2C hub (TCA9548A). (Alan doesn't remember why he ordered it.)
- Planned sensors: 2–3 ultrasonic, 2–3 temperature. Also has an M5Stack NCIR (infrared temperature) unit.
- Servos: 2.
  - Reely S-0060 MG: analog, metal gears, about 6 kg·cm stall, 180° positional.
  - Newer one rated 10 kg·cm – exact model to be confirmed (earlier chats mention MG996R servos labelled 10 kg/cm).
  - With tank steering, servos would only be used for wheel lifting (see open-questions.md).

## Power
- **Pi:** its own small powerbank (small MagSafe or borrowed mini powerbank), must deliver 5 V / 3 A over USB-C.
  The 50,000 mAh powerbank (Tank Lite W5001) is out because of its weight.
- **Motors: NOT decided yet.** Decide once everything is discussed and understood.
  - Option A: Amewi Li-Ion pack, 7.4 V, 1200 mAh, 8.88 Wh (borrowed from a friend; red plug + white balance lead).
    Last decision was this pack, because its connector works with Dupont pins. Full charge about 8.4 V.
    (Friend's packs are rated 5C.)
  - Option B: soldered 2×AA holder packs (3 in series per string, about 6 AA total) with an on/off switch or connector.
- Motors are rated 4.5 V → with 7.4–9 V, limit PWM (roughly 55–70% duty, depending on the driver's
  voltage drop) to avoid overheating and wear. In code: `max_speed=80` default in `rover.py` (as of 2026-11-12).
- Fuses: glass fuses 4 A and 8 A on hand, **no fuse holder yet**.
