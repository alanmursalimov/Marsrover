# rover_motors.py
from smbus2 import SMBus
import time##

# ---------- Konfiguration ----------
GROVEPI_PORT = "I2C-1"   # Port am GrovePi, in dem der Motortreiber steckt (I2C-1, I2C-2 oder I2C-3)
I2C_BUS = 1              # Raspberry Pi: /dev/i2c-1
DRIVER_ADDR = 0x0F       # Grove I2C Motor Driver v1.3b

CMD_SPEED = 0x82         # Geschwindigkeit Motor 1 und Motor 2 (0-255)
CMD_DIRECTION = 0xAA     # Richtung beider Motoren

# Richtungs-Bits pro Motor
_STOP, _BACK, _FWD = 0b00, 0b01, 0b10


class MotorDriver:
    def __init__(self, bus=I2C_BUS, addr=DRIVER_ADDR, port=GROVEPI_PORT):
        self.addr = addr
        self.port = port
        self.bus = SMBus(bus)
        self._speed = [0, 0]   # -255..255 je Motor
        self._check_connection()

    def _check_connection(self):
        try:
            self.bus.write_i2c_block_data(self.addr, CMD_SPEED, [0, 0])
            print(f"Motortreiber gefunden: GrovePi-Port {self.port}, "
                  f"Adresse 0x{self.addr:02X}")
        except OSError:
            raise RuntimeError(
                f"Kein Motortreiber an GrovePi-Port {self.port} "
                f"(Adresse 0x{self.addr:02X}). Kabel/Strom pruefen, "
                f"'i2cdetect -y 1' ausfuehren."
            )

    def _apply(self):
        bits = []
        for s in self._speed:
            bits.append(_FWD if s > 0 else _BACK if s < 0 else _STOP)
        direction = (bits[0] << 2) | bits[1]
        self.bus.write_i2c_block_data(self.addr, CMD_DIRECTION, [direction, 0x01])
        self.bus.write_i2c_block_data(
            self.addr, CMD_SPEED, [abs(self._speed[0]), abs(self._speed[1])]
        )

    @staticmethod
    def _clamp(v):
        return max(-255, min(255, int(v)))

    def set_motor(self, motor, speed):
        """motor = 1 oder 2, speed = -255 (rueckwaerts) ... 255 (vorwaerts)"""
        if motor not in (1, 2):
            raise ValueError("motor muss 1 oder 2 sein")
        self._speed[motor - 1] = self._clamp(speed)
        self._apply()

    def drive(self, left, right):
        """Beide Motoren gleichzeitig: Motor 1 = links, Motor 2 = rechts"""
        self._speed = [self._clamp(left), self._clamp(right)]
        self._apply()

    def stop(self):
        self.drive(0, 0)

    def close(self):
        self.stop()
        self.bus.close()


if __name__ == "__main__":
    m = MotorDriver()
    try:
        print("Motor 1 vorwaerts");  m.set_motor(1, 150); time.sleep(2)
        m.stop();                    time.sleep(0.5)
        print("Motor 2 vorwaerts");  m.set_motor(2, 150); time.sleep(2)
        m.stop();                    time.sleep(0.5)
        print("Beide vorwaerts");    m.drive(150, 150);   time.sleep(2)
        print("Beide rueckwaerts");  m.drive(-150, -150); time.sleep(2)
        print("Drehen auf der Stelle"); m.drive(-120, 120); time.sleep(1)
    finally:
        m.close()