from rover import Rover
from grovepi import *
from time import sleep

rover = Rover(
    left=[(0x0F, "J1"), (0x0F, "J5")],
    right=[(0x0E, "J1"), (0x0E, "J5")],
    invert_right=True,                  # rechte Seite dreht andersrum
)

middle_USS = 2
right_USS = 8
left_USS = 6

back_left = rover.motor(0x0F, "J1")
back_right = rover.motor(0x0E, "J1", invert=True)
front_left = rover.motor(0x0F, "J5")
front_right = rover.motor(0x0E, "J5", invert=True)

def reverse_and_turn():
    if distance_right_USS > distance_right_USS:
        rover.turn_right(100, seconds=3)
    elif distance_right_USS < distance_left_USS:
        rover.turn_left(100, seconds=3)
     


try:
    while True:
        distance_middle_USS = ultrasonicRead(middle_USS)
        distance_right_USS = ultrasonicRead(right_USS)
        distance_left_USS = ultrasonicRead(left_USS)

        if distance_middle_USS <= 20:
            reverse_and_turn()
        else:
            rover.forward(70)
        sleep(0.1)
except KeyboardInterrupt:
        pass


