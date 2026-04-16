import math
import datetime

def get_hand_position(center, length, angle_degrees):
    """
    Calculates the (x, y) coordinates for a clock hand tip.
    Subtracts 90 degrees so that 0° starts at the 12 o'clock position.
    """
    angle_radians = math.radians(angle_degrees - 90)
    
    x = center[0] + length * math.cos(angle_radians)
    y = center[1] + length * math.sin(angle_radians)
    return (int(x), int(y))

def get_current_time_data():
    """
    Retrieves current time and calculates rotation angles in degrees.
    """
    now = datetime.datetime.now()
    
    # Seconds: 6 degrees per second (360 / 60)
    sec_angle = now.second * 6
    
    # Minutes: 6 degrees per minute + smooth offset based on seconds
    min_angle = now.minute * 6 + now.second * 0.1
    
    return sec_angle, min_angle