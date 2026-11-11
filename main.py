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


def turn_left():
      back_left.speed(70, seconds=2)

try:
    rover.turn_left(100, seconds=5)
    # while True:
    #     value = ultrasonicRead(distance_middle_USS)##
    #     print("Disnanz ca. = %d cm" %value)

    #     if value <= 20:
    #         rover.stop()
    #     else:
    #         rover.forward(70)
    #     sleep(0.1)
except KeyboardInterrupt:
        pass


