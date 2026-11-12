"""
servotest.py - Servo am Grove 16-Kanal PWM-Treiber (PCA9685) testen.

Aufruf auf dem Pi (Dienst vorher stoppen):
    sudo systemctl stop marsrover
    python3 ~/Marsrover/servotest.py            # Servo an Kanal 0
    python3 ~/Marsrover/servotest.py 1          # Servo an Kanal 1
    python3 ~/Marsrover/servotest.py 0 0x7F 3   # Kanal 0, Adresse 0x7F, Hub-Port 3

Ohne Hub-Port sucht das Skript selber, an welchem Port des I2C-Hubs der
PWM-Treiber haengt. Der Servo faehrt 90 -> 60 -> 120 -> 90 Grad und wird
dann stromlos geschaltet. Servo-Horn vorher frei drehen lassen!
"""
import sys
import time

from rover import Rover

channel = int(sys.argv[1]) if len(sys.argv) > 1 else 0
address = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x7F
hub_port = int(sys.argv[3]) if len(sys.argv) > 3 else "auto"

rover = Rover(addresses=[])   # keine Motortreiber, nur Servo
servo = rover.servo(channel=channel, address=address, hub_port=hub_port)
print(f"PWM-Treiber {address:#04x}, Hub-Port {servo._board.hub_port}, Kanal {channel}")

try:
    for deg in (90, 60, 120, 90):
        print(f"-> {deg} Grad")
        servo.angle(deg)
        time.sleep(1.5)
finally:
    servo.off()
    print("Servo aus.")
