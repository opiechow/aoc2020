import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.disable(logging.FATAL)

def load_timetable(filename):
    with open(filename, "r") as f:
        timestamp = int(f.readline())
        entires = f.readline().rstrip().split(",")
    return timestamp, entires

timestamp, entries = load_timetable("input")
bus_ids = sorted(list(map(int, filter(lambda x: x.isnumeric(), entries))))
until_next_departure = list(map(lambda x: x - (timestamp % x), bus_ids))
buses_times = sorted(zip(bus_ids, until_next_departure), key=lambda x: x[1])
print(buses_times[0][0] * buses_times[0][1])

def join_remainders(two_div_remainders):
    div1, rem1 = two_div_remainders[0]
    div2, rem2 = two_div_remainders[1]
    while rem1 != rem2:
        if rem1 < rem2:
            rem1 += div1
        if rem2 < rem1:
            rem2 += div2
    logging.debug("found common div/rem: %d/%d", div1*div2, rem1)
    return (div1*div2, rem1)

conds = filter(lambda x: x[1] != "x", enumerate(entries))
fixed_conds = list(map(lambda x: (x[0], int(x[1])), conds))
div_remainder_list = list(map(lambda x: (x[1], (x[1]-x[0]) % x[1]), fixed_conds))
div_remainder_list = sorted(div_remainder_list, reverse=True)
logging.debug(div_remainder_list)
while len(div_remainder_list) > 1:
    div_remainder_list.append(join_remainders((div_remainder_list.pop(), div_remainder_list.pop())))
    div_remainder_list = sorted(div_remainder_list, reverse=True)
print(div_remainder_list[0][1])