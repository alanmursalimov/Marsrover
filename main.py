
##Importing the libraries##
from rover import Rover #Rover library made by Claude
from grovepi import * #GrovePi library
from time import sleep #time library

rover = Rover(
    left=[(0x0F, "J1"), (0x0F, "J5")], #the left side/driver to which the 2 right motors are connected
    right=[(0x0E, "J1"), (0x0E, "J5")], #the right side/driver to which the 2 right motors are connected
    invert_right=True,  #the right side is inverted in terms of spinning direction
)

middle_USS = 2 #middle Ultrasonicsensor digital port
right_USS = 8 #right Ultrasonicsensor digital port
left_USS = 6 #left Ultrasonicsensor digital port

#rear left motor connected to the DC-Motor-Driver with the I2C-Address 0x0F at connection J1
back_left = rover.motor(0x0F, "J1")
#rear right motor connected to the DC-Motor-Driver with the I2C-Address 0x0E at connection J1. 
#Plus it's inversed so it spins into the right direction
back_right = rover.motor(0x0E, "J1", invert=True) 
#front left motor connected to the DC-Motor-Driver with the I2C-Address 0x0F at connection J5
front_left = rover.motor(0x0F, "J5")
#front right motor connected to the DC-Motor-Driver with the I2C-Address 0x0E at connection J5. 
#Plus it's inversed so it spins into the right direction
front_right = rover.motor(0x0E, "J5", invert=True)

servo1 = rover.servo(channel=0, address=0x7F, min_us=2400, max_us=500)
servo2 = rover.servo(channel=1, address=0x7F, min_us=2400, max_us=500)


def reverse_and_turn():
    '''
    Function for turning the rover to the more open side so it avoids obstacles
    '''
    ##part for deciding which way to turn##
    if distance_right_USS > distance_left_USS: #If the right side is more open to the rover
        rover.turn_left(100, seconds=1) #turns left at 100% speed for 1s
    elif distance_right_USS < distance_left_USS: #if the left side is more open to the rover
        rover.turn_right(100, seconds=1) #turns right at 100% for 1s
    ##another part which also makes use of the side ultrasonicsensors. Makes the rover "smarter"##
    if distance_right_USS < 20:
         rover.turn_left(100, seconds=0.1)
    if distance_left_USS < 20:
         rover.turn_right(100, seconds=0.1)


try:
    option = input("auto/wasd/test/kal: ")
    if option == "auto":
        while True:
            #*distances the Ultrasonicsensors measured
            distance_middle_USS = ultrasonicRead(middle_USS)
            sleep(0.03)
            distance_right_USS = ultrasonicRead(right_USS)
            sleep(0.03)
            distance_left_USS = ultrasonicRead(left_USS)

            if distance_middle_USS <= 25: #if the distance is under 20cm
                reverse_and_turn() #run function
                print(distance_middle_USS)
            else:
                rover.forward(50) #or drive forward at 50% of max_speed
    elif option == "test":
        motor = int(input("What motor: "))
        while True:
            angle = int(input("Winkel: "))
            motor.angle(angle)
    elif option == "kal":
        motor = int(input("What motor: "))
        motor.calibrate()
            

        
         
except KeyboardInterrupt:
        pass


