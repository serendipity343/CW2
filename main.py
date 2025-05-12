"""
Braightenberg robot for crossing the reality gap
The light sensors allow light following behaviours.

The sensor pins are read at 26 and 27, if the robot is not turning away from the collision,
consider switching the pins around (26 & 27).

Code by Dexter R Shepherd

"""

from EduBot_CP import wheelBot
import time
import board
from analogio import AnalogIn

s1 = AnalogIn(board.GP26)
s2 = AnalogIn(board.GP27)

#change the sensor gain to preference
sensor_gain=0.5
def get_intensity(pin):
    return (pin.value*3.3) /65536

def calc(genotype):
    w_ll,w_lr,w_rl,w_rr,bl,br = (genotype[0],genotype[1],genotype[2],genotype[3],genotype[4],genotype[5])
    # Calculate (square) distance to element
    #  Calculate local intensity
    il,ir=(get_intensity(s1)*10,get_intensity(s2)*10)

    #weights times inputs plus bias
    lm = il*w_ll + ir*w_rl + bl;
    rm = il*w_lr + ir*w_rr + br;
    print("sensor:",il,ir)
    print("motor:",lm,rm)
    return lm,rm

# Define bot instance
bot = wheelBot(board_type="pico")

genotype = [0.1375, 3.4721, 3.3984,  0.1246, 0.7152,  0.7238]


# Test move
speed = 1000
bot.forward(speed) # Activate both motors
time.sleep(1) # Wait for 1 second
bot.stop() # Stops both motors
sensitivity = 1

while True:
    # Do this for both motors
    lm, rm = calc(genotype)

    # Convert the computed commands to a speed in the range 0-100
    # (This scaling/clamping may need to be adjusted for your robot and sensors)
    lm_speed = max(0, min(100, int(abs(lm)))) * sensitivity
    rm_speed = max(0, min(100, int(abs(rm)))) * sensitivity
    print(">",lm_speed,rm_speed)

    # Determine motor direction: forward if positive, reverse if negative
    lm_direction = "r" if lm >= 0 else "f"
    rm_direction = "r" if rm >= 0 else "f"

    # Map motor 3 to left and motor 4 to right (adjust if your wiring is different)
    bot.motorOn(3, lm_direction, lm_speed)
    bot.motorOn(4, rm_direction, rm_speed)

    # A short delay between updates (adjust as needed)
    time.sleep(0.1)
