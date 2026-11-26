'''
Marsrover - main.py

Controls the class Marsrover (KSK). The rover drives on its own and avoids
obstacles with 3 ultrasonic sensors. A servo turns the solar panel towards
the brighter side, measured with 2 light sensors.

Hardware:
    <Timo mach du das>

External code:
    rover.py: motor/servo library, written by Claude (AI)
    grovepi: Dexter Industries GrovePi library

Authors: Alan Mursalimov, Christian Scanzoni, Timo Möckli
Date:    17.12.2026
'''


##Importing the libraries##
from rover import Rover #Rover library made by Claude
from grovepi import * #GrovePi library
from time import sleep #time library

##rover with all the ports. Used for all the motors (DC and servo). From Claude's library##
rover = Rover(
    left=[(0x0F, "J1"), (0x0F, "J5")], #the left side/driver to which the 2 left motors are connected
    right=[(0x0E, "J1"), (0x0E, "J5")], #the right side/driver to which the 2 right motors are connected
    invert_right=True,  #the right side is inverted in terms of spinning direction
)

##digital ports of the Ultrasonic sensors##
middle_USS = 2 #middle
right_USS = 8 #right
left_USS = 6 #left

##analog ports of the light sensors##
right_light_sensor = 0 #right
left_light_sensor = 2 #left

auto_button = 4
pinMode(auto_button, 4)

#Servo connections. Servo motors connected on channels which are on the driver. 
#The driver is connected to the 0x7F address on the I2C-Hub. 
#min_us/max_us is the puls length at 0 and 180 degrees
#The command .servo is from Claude's library
solar_panel_servo = rover.servo(channel=0, address=0x7F, min_us=2225, max_us=480)
servo2 = rover.servo(channel=1, address=0x7F, min_us=2100, max_us=480)

def start_menu():
    '''
    Small start screen for options. Made so that the rover doesn't run away while testing.
    Start menu options:
    auto: drive automatically, avoid obstacles, turn the solar panel
    wasd: drive manually with the keyboard (W/A/S/D, space = stop, Q = quit)
    test: type an angle to test the solar panel servo
    kal:  calibrate a servo (find min_us / max_us)
    '''
    try:
        #Programm asks what you want to do and you type the option in there
        option = input("auto/wasd/test/kal: ") 
        option = "auto"
        if option == "auto": #auto drive
            while True:
                drive() #function for driving around and avoiding the obstacles
                solar_panel_turning() #turning the solar panel to the brighter side
                
        elif option == "test":#Test block for testing servos
            while True:
                angle = int(input("Winkel: "))#the typed angle
                solar_panel_servo.angle(angle) #command for setting the angle. The servo knows where it is. Made by Claude

        elif option == "kal": #calibration option
            servo2.calibrate() #calibration command from Claudes library

        elif option == "wasd": #Control the rover with WASD
            rover.wasd(speed=100) #Claude's Code for driving around with WASD

    except KeyboardInterrupt:
        pass


def drive():
    '''
    Function for driving the rover and avoiding obstacles
    '''
    ##distances the Ultrasonicsensors measured##
    distance_middle_USS = ultrasonicRead(middle_USS)
    sleep(0.03)
    distance_right_USS = ultrasonicRead(right_USS)
    sleep(0.03)
    distance_left_USS = ultrasonicRead(left_USS)
    if distance_middle_USS <= 25: #if the distance is under 25cm
        print(distance_middle_USS)
        turn(distance_right_USS, distance_left_USS) #run function
    else:
        rover.forward(50) #or drive forward at 50% of max_speed. From Claude's library
    
def turn(distance_right_USS, distance_left_USS):
    '''
    Function for turning the rover to the more open side so it avoids obstacles
    '''
    rover.stop() #fuction made by Claude to make the motors stop turning
    sleep(1)
    ##part for deciding which way to turn##
    if distance_right_USS > distance_left_USS: #If the right side is more open to the rover
        rover.turn_left(100, seconds=1) #turns left at 100% speed for 1s
    elif distance_right_USS < distance_left_USS: #if the left side is more open to the rover
        rover.turn_right(100, seconds=1) #turns right at 100% for 1s

    ##another part which also makes use of the side ultrasonicsensors. Makes the rover "smarter"##
    #if the distance from the right/left side is under 20 it should turn to the opposing side
    if distance_right_USS < 20:
         rover.turn_left(100, seconds=0.1) #turns left for 0.1 seconds at full speed. Function from Claude's library
    elif distance_left_USS < 20:
         rover.turn_right(100, seconds=0.1)


def solar_panel_turning():
    '''
    Function for turning the 3D-printed solar panel by 180 degrees to whichever side is the brightest.
    Brightness is measured with light sensors.
    '''
    #Reading the values of the light sensors
    value_right_light_sensor = analogRead(right_light_sensor)
    value_left_light_sensor = analogRead(left_light_sensor)

    #determining to which side the motor should turn. The side with the higher value (lighter) is the "winner"
    if value_left_light_sensor > value_right_light_sensor:
        solar_panel_servo.angle(180) #Claude's code from the library. Controls the servo and spins it to a desired angle
    elif value_left_light_sensor < value_right_light_sensor:
        solar_panel_servo.angle(0)

def heat_seaker():
    pass




start_menu()