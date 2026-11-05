from rover import Rover

rover = Rover()
rover.forward(50, seconds=2)
rover.turn_left(50, seconds=1)
rover.stop()

rover.drive(50, 0)     # nur Motor 1 (J1) dreht, Motor 2 (J5) steht
#rover.drive(0, 50)     # nur Motor 2 dreht
#rover.drive(50, -50)   # Motor 1 im Uhrzeigersinn, Motor 2 dagegen