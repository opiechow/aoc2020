import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.disable(logging.FATAL)

def load_cubes(filename):
    active_cubes = set()
    lines = []
    with open(filename, "r") as f:
        for line in f:
            lines.append(line.rstrip())
    z = 0
    w = 0
    for y, row in enumerate(lines):
        for x, col in enumerate(row):
            if col == "#":
                active_cubes.add((x, y, z, w))
    return active_cubes

def get_relative_neigbours():
    points = set()
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                for w in range(-1, 2):
                    points.add((x, y, z , w))
    points.remove((0, 0, 0, 0))
    return points

relative_neighbours = get_relative_neigbours()

def get_neighbours(point):
    logging.debug(point)
    return tuple(map(lambda rel : (rel[0] + point[0],
                                   rel[1] + point[1],
                                   rel[2] + point[2],
                                   rel[3] + point[3]),
                     relative_neighbours))

# only neighbours and currently active guys are of intrest
def get_points_of_intrest(active_cubes):
    points_of_intrest = active_cubes.copy()
    logging.debug("old active cubes: %s", points_of_intrest)
    neighs_set = set()
    for point in points_of_intrest:
        neighs_set.update(get_neighbours(point))
    logging.debug("new neighbours: %s", neighs_set)
    points_of_intrest.update(neighs_set)
    logging.debug("final points of intrest: %s" % points_of_intrest)
    return points_of_intrest

def count_neighbours(points_of_intrest, active_cubes):
    neighbour_counts = {}
    logging.debug("count neighbours POIs: %s" % points_of_intrest)
    for point in points_of_intrest:
        act_neighs = sum(map(lambda x: x in active_cubes, get_neighbours(point)))
        neighbour_counts[point] = act_neighs
    return neighbour_counts

def new_cubes(points_of_intrest, active_cubes, neighbour_counts):
    new_active = set()
    logging.debug("new cubes POIs: %s" % points_of_intrest)
    for point in points_of_intrest:
        if point in active_cubes:
            if neighbour_counts[point] in (2, 3):
                new_active.add(point)
        else:
            if neighbour_counts[point] == 3:
                new_active.add(point)
    return new_active


active_cubes = load_cubes("input") 
logging.debug("active cubes: %s" % active_cubes)

for i in range(6):
    points_of_intrest = get_points_of_intrest(active_cubes)
    neighbour_counts = count_neighbours(points_of_intrest, active_cubes)
    active_cubes = new_cubes(points_of_intrest, active_cubes, neighbour_counts)

print(len(active_cubes))
    


