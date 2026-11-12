from smbus2 import SMBus
import time

ADDR = 0x70
KANAL = 0
bus = SMBus(1)

bus.write_byte_data(ADDR, 0x00, 0x10)   # Sleep
bus.write_byte_data(ADDR, 0xFE, 121)    # 50 Hz
bus.write_byte_data(ADDR, 0x00, 0x20)   # Wake + Auto-Increment
time.sleep(0.01)

def winkel(grad):                        # 0..180°
    ms = 0.5 + grad / 180 * 2.0          # 0.5 ms .. 2.5 ms
    pulse = round(ms / 20 * 4096)
    reg = 0x06 + 4 * KANAL
    bus.write_i2c_block_data(ADDR, reg, [0, 0, pulse & 0xFF, pulse >> 8])

winkel(0)
time.sleep(1)
winkel(90)                               # um 90° drehen
time.sleep(1)