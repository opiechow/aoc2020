test_input = "FBFBBFFRLR"

def bisect(coded, lower_letter, upper_letter):
    lower = 0
    upper = 2**len(coded) - 1
    #print("- Start by considering the whole range, rows {} through {}".format(lower, upper))
    for letter in coded:
        distance = upper - lower + 1
        if letter == lower_letter:
            upper = (lower + distance/2) - 1
            #print("- {} means to take the lower half, keeping rows {} through {}".format(letter, lower, upper))
        if letter == upper_letter:
            lower = lower + distance/2
            #print("- {} means to take the upper half, keeping rows {} through {}".format(letter, lower, upper))
    assert(lower == upper)
    return lower

def decode_entry(entry):
    assert(len(entry) == 10)
    rows = entry[0:7]
    cols = entry[7:]
    row = bisect(rows, "F", "B")
    col = bisect(cols, "L", "R")
    seat_id = row * 8 + col
    return seat_id

assert(decode_entry(test_input) == 357)

boarding_passes = []
with open("input","r") as f:
    for line in f:
        boarding_passes.append(line.rstrip())

seat_ids = list(map(decode_entry, boarding_passes))
print(max(seat_ids))
seat_ids = sorted(seat_ids)
for i in range(0, len(seat_ids)):
    if seat_ids[i + 1] - seat_ids[i] != 1:
        print (seat_ids[i + 1] - 1)
        break



