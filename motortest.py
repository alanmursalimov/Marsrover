"""
motortest.py - Motortreiber direkt testen (OHNE rover.py)
==========================================================

Spricht den Grove I2C Motor Driver v1.3 direkt an. So sieht man, ob das
Problem am Treiber/Strom liegt oder an der Library.

Starten (Raeder in der Luft!):
    sudo systemctl stop marsrover
    python3 ~/Marsrover/motortest.py                 # 0x0F, J1 und J5, 60 %
    python3 ~/Marsrover/motortest.py 0x0F J5 80      # nur J5 mit 80 %
    python3 ~/Marsrover/motortest.py 0x0F J1 60 490  # zusaetzlich PWM 490 Hz

Argumente (alle optional, in dieser Reihenfolge):
    Adresse   z.B. 0x0F
    Klemme    J1, J5 oder beide (Standard)
    Tempo     0-100 = % der AKKU-Spannung (hier gibt es KEIN max_speed!)
              DG01D sind 4.5-V-Motoren: bei 7.4 V nur kurz ueber 60-70 %.
    PWM-Hz    31372 (Firmware-Standard), 3921, 490, 122 oder 30

Dabei auf dem Treiber auf die LEDs IN1/IN2 (J1) und IN3/IN4 (J5) achten.
"""

import sys
import time

import smbus

REG_SPEED = 0x82
REG_PWM_FREQ = 0x84
REG_DIRECTION = 0xAA
PWM_CODES = {31372: 0x01, 3921: 0x02, 490: 0x03, 122: 0x04, 30: 0x05}

address = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0x0F
which = sys.argv[2].upper() if len(sys.argv) > 2 else "BEIDE"
percent = float(sys.argv[3]) if len(sys.argv) > 3 else 60
pwm_hz = int(sys.argv[4]) if len(sys.argv) > 4 else None

duty = round(max(0, min(100, percent)) * 255 / 100)
bus = smbus.SMBus(1)


def write(register, data):
    bus.write_i2c_block_data(address, register, data)
    time.sleep(0.02)


def run(m1, m2, text):
    """m1, m2: -255..255."""
    direction = (0b0010 if m1 >= 0 else 0b0001) | (0b1000 if m2 >= 0 else 0b0100)
    print(f"  {text:<28} Richtung={direction:04b}  Tempo=[{abs(m1)}, {abs(m2)}]")
    write(REG_DIRECTION, [direction, 0])
    write(REG_SPEED, [abs(m1), abs(m2)])
    time.sleep(2)
    write(REG_SPEED, [0, 0])
    time.sleep(0.5)


try:
    bus.write_quick(address)
except OSError:
    sys.exit(f"Kein Treiber auf {address:#04x}. 'i2cdetect -y -a 1' ausfuehren.")

print(f"Treiber {address:#04x} antwortet. Tempo {percent:.0f} % = {duty}/255")
if pwm_hz is not None:
    if pwm_hz not in PWM_CODES:
        sys.exit(f"PWM {pwm_hz} Hz gibt es nicht. Erlaubt: {sorted(PWM_CODES)}")
    write(REG_PWM_FREQ, [PWM_CODES[pwm_hz], 0])
    print(f"PWM-Frequenz auf {pwm_hz} Hz gesetzt")

try:
    if which in ("J1", "BEIDE"):
        run(duty, 0, "J1 vorwaerts")
        run(-duty, 0, "J1 rueckwaerts")
    if which in ("J5", "BEIDE"):
        run(0, duty, "J5 vorwaerts")
        run(0, -duty, "J5 rueckwaerts")
finally:
    write(REG_SPEED, [0, 0])
    print("Fertig, Motoren aus.")
