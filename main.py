from rover import Rover
from grovepi import *
from time import sleep

sound_sensor = 0


rover = Rover()
# rover.forward(50, seconds=2)
# rover.turn_left(50, seconds=1)
# rover.stop()

rover.drive(50, 0, seconds=3)     # nur Motor 1 (J1) dreht, Motor 2 (J5) steht
#rover.drive(0, 50)     # nur Motor 2 dreht
#rover.drive(50, -50)   # Motor 1 im Uhrzeigersinn, Motor 2 dagegen

while True:
    value = ultrasonicRead(sound_sensor)
    print("Disnanz ca. = %d cm" %value)
    sleep(.5)

