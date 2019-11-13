from math import degrees, atan2
import config


def taninv(dy, dx):
    ''' returns tan inverse in degrees [-179,180] '''
    return degrees(atan2(-dy, dx))


def get_current_direction(orient_dir):
    '''
    orient_dir = orientation in degrees

    Tells current direction, -1 if none
    '''
    for i in range(4):
        if abs(orient_dir - config.ANGLES[i]) > config.ANGLE_TOLERANCE:
            return i
    return -1


def get_nearest_direction(direction):
    '''
    direction: orientation in degrees

    Returns direction_name, 2/3 for L/R, angle_difference
    '''
    mini = 10000
    pos = None
    for i in range(4):
        temp = abs(direction - config.ANGLES[i])
        if temp < mini:
            mini = temp
            pos = i
    rot = (direction - config.ANGLES[pos]) % 360
    if rot > 180:
        return pos, 3, 360-rot
    return pos, 2, rot


def get_rotation_info(old_direction, new_direction):
    ''' returns 2/3 for L/R, angle_difference '''
    rot = (new_direction - old_direction) % 360
    if rot > 180:
        return 3, 360-rot
    return 2, rot


def get_direction_from_name(direction_name):
    '''
    direction_name: Can be FORWARD, F, 0 or any other direction name

    Finds direction name from input

    returns integer [0,3]
    '''
    if isinstance(direction_name, str):
        direction_name = direction_name.upper()
    if direction_name in ["FORWARD", "F", 0]:
        return 0
    if direction_name in ["BACKWARD", "B", 1]:
        return 1
    if direction_name in ["LEFT", "L", 2]:
        return 2
    if direction_name in ["RIGHT", "R", 3]:
        return 3
    return -1


if __name__ == "__main__":
    raise Exception("This is not a top level module")
