import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
#logging.disable(logging.FATAL)

def load_seat_map(filename):
    rows = []
    with open(filename, "r") as f:
        for line in f:
            rows.append(list(line.rstrip()))
    return rows

def get_points_to_check(seat_map, row, col):
    num_rows = len(seat_map)
    num_cols = len(seat_map[0])
    points = ((row - 1, col - 1), (row - 1, col    ), (row - 1, col + 1),
              (row    , col - 1),                     (row    , col + 1),
              (row + 1, col - 1), (row + 1, col    ), (row + 1, col + 1))
    return tuple(filter(lambda x: x[0] >= 0 and x[0] < num_rows and
                                  x[1] >= 0 and x[1] < num_cols, points))

def count_occupied_neighbours(seat_map, row, col):
    count = 0
    points = get_points_to_check(seat_map, row, col)
    for point in points:
        row = point[0]
        col = point[1]
        if seat_map[row][col] == "#":
            count += 1
    return count

def count_occupied_total(seat_map):
    count = 0
    for row in seat_map:
        for col in row:
            if col == "#":
                count += 1
    return count

def seating_step(old_state):
    new_state = []
    num_rows = len(old_state)
    num_cols = len(old_state[0])
    change_count = 0
    for r in range(num_rows):
        new_row = []
        for c in range(num_cols):
            count = count_occupied_neighbours(old_state, r, c)
            if old_state[r][c] == "L" and count == 0:
                    change_count += 1
                    new_row.append("#")
            elif old_state[r][c] == "#" and count >= 4:
                    change_count += 1
                    new_row.append("L")
            else:
                new_row.append(old_state[r][c])
        new_state.append(new_row)
    return new_state, change_count

test_seats = load_seat_map("input")
change_count = -1
loop_count = 0
while change_count != 0:
    for row in test_seats:
        logging.debug("iter %d row: %s" % (loop_count, "".join(row)))
    logging.debug("----------------------")
    test_seats, change_count = seating_step(test_seats)
    loop_count += 1
print(count_occupied_total(test_seats))

