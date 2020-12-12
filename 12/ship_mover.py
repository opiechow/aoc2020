import logging
import math

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
logging.disable(logging.FATAL)

def load_instructions(filename):
    instructions = []
    with open(filename, "r") as f:
        for line in f:
            instructions.append({"action" : line[0], "value" : int(line[1:])})
    return instructions

def swim_ship(starting_coords, directions):
    current_coords = starting_coords.copy()
    for instruction_dict in directions:
        action = instruction_dict["action"]
        value = instruction_dict["value"]
        logging.debug("executing %s" % instruction_dict)
        logging.debug("current coords before: %s", current_coords)
        if action == "L":
            current_coords["d"] -= value
        if action == "R":
            current_coords["d"] += value
        if action == "F":
            if current_coords["d"] % 360 == 0:
                action = "N"
            if current_coords["d"] % 360 == 90:
                action = "E"
            if current_coords["d"] % 360 == 180:
                action = "S"
            if current_coords["d"] % 360 == 270:
                action = "W"
        if action == "N":
            current_coords["y"] += value
        if action == "S":
            current_coords["y"] -= value
        if action == "E":
            current_coords["x"] -= value
        if action == "W":
            current_coords["x"] += value
        logging.debug("current coords after: %s", current_coords)
    return current_coords

def rotate_waypoint(waypoint, degrees):
    x = waypoint["x"]
    y = waypoint["y"]
    
    r = math.sqrt(x**2 + y**2)
    fi = math.degrees(math.atan2(y, x))
    new_fi = fi + degrees

    new_x = round(r * math.cos(math.radians(new_fi)))
    new_y = round(r * math.sin(math.radians(new_fi)))
    return {"x" : new_x, "y" : new_y}
    

def swim_ship_waypoint(starting_coords, waypoint_coords, directions):
    current_coords = starting_coords.copy()
    waypoint_coords = waypoint_coords.copy()
    for instruction_dict in directions:
        action = instruction_dict["action"]
        value = instruction_dict["value"]
        logging.debug("executing %s" % instruction_dict)
        logging.debug("current coords before: %s", current_coords)
        logging.debug("waypoint coords before: %s", waypoint_coords)
        if action == "L":
            waypoint_coords = rotate_waypoint(waypoint_coords, -value)
        if action == "R":
            waypoint_coords = rotate_waypoint(waypoint_coords, value)
        if action == "F":
            current_coords["x"] += value * waypoint_coords["x"]
            current_coords["y"] += value * waypoint_coords["y"]
        if action == "N":
            waypoint_coords["y"] += value
        if action == "S":
            waypoint_coords["y"] -= value
        if action == "E":
            waypoint_coords["x"] -= value
        if action == "W":
            waypoint_coords["x"] += value
        logging.debug("current coords after: %s", current_coords)
        logging.debug("waypoint coords after: %s", waypoint_coords)
    return current_coords

def manhattan_distance(coords_from, coords_to):
    return abs(coords_from["x"] - coords_to["x"]) + \
           abs(coords_from["y"] - coords_to["y"])

dirs = load_instructions("input")
start_coords = {"x" : 0, "y" : 0, "d" : 90}
ship_coords = swim_ship(start_coords, dirs)
logging.debug(ship_coords)
print(manhattan_distance(ship_coords, start_coords))
waypoint_coords = {"x" : -10, "y" : 1}
ship_coords = swim_ship_waypoint(start_coords, waypoint_coords, dirs)
print(manhattan_distance(ship_coords, start_coords))

