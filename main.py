from rover import Rover
from grovepi import *
from time import sleep

rover = Rover(
    left=[(0x0F, "J1"), (0x0F, "J5")],
    right=[(0x0E, "J1"), (0x0E, "J5")],
    invert_right=True,                  # rechte Seite dreht andersrum
)

distance_middle_USS = 2
distance_right_USS = 8
distance_left_USS = 6

back_left = rover.motor(0x0F, "J1")
back_right = rover.motor(0x0E, "J1", invert=True)
front_left = rover.motor(0x0F, "J5")
front_right = rover.motor(0x0E, "J5", invert=True)



# rover.forward(50, seconds=2)
# rover.turn_left(50, seconds=1)
# rover.stop()

# back_left.speed(50, seconds=2)     # nur Motor 1 (J1) dreht, Motor 2 (J5) steht
# back_right.speed(50, seconds=2)
# front_left.speed(50, seconds=2)

rover.forward(70, seconds=5)
#rover.drive(0, 50)     # nur Motor 2 dreht
#rover.drive(50, -50)   # Motor 1 im Uhrzeigersinn, Motor 2 dagegen

while True:
    try:
        value = ultrasonicRead(distance_middle_USS)##
        print("Disnanz ca. = %d cm" %value)
        sleep(.5)
    except KeyboardInterrupt:
        break

