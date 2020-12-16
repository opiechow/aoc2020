import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
logging.disable(logging.FATAL)

def load_input(filename):
    with open(filename, "r") as f:
        lines = []
        for line in f:
            lines.append(line.rstrip())
        my_idx = lines.index("your ticket:")
        other_idx = lines.index("nearby tickets:")
        fields = lines[:my_idx-1]
        ticket = lines[my_idx+1]
        other_tickets = lines[other_idx+1:]
    return fields, ticket, other_tickets

def get_allowed_numbers(fields):
    allowed_numbers = set()
    for line in fields:
        name, arg = line.split(":")
        ranges = arg.split("or")
        for elem in ranges:
            start, stop = elem.split("-")
            allowed = set(range(int(start), int(stop) + 1))
            logging.debug("adding %s to allowed nums" % allowed)
            allowed_numbers.update(allowed)
    return allowed_numbers

def get_class_allowed(fields):
    class_allowed = {}
    for line in fields:
        name, arg = line.split(":")
        class_allowed[name] = set()
        ranges = arg.split("or")
        for elem in ranges:
            start, stop = elem.split("-")
            allowed = set(range(int(start), int(stop) + 1))
            logging.debug("adding %s to allowed nums for class %s" % 
                           (allowed, name))
            class_allowed[name].update(allowed)
    return class_allowed

def get_nums_to_check(other_tickets):
    nums_to_check = []
    for line in other_tickets:
        nums_to_check.extend()
    logging.debug("nums to check: %s" % nums_to_check)
    return nums_to_check

fields, ticket, other_tickets = load_input("input")
logging.debug("fields: %s" % fields)
logging.debug("ticket: %s" % ticket)
logging.debug("nearby tickets: %s" % other_tickets)

allowed_nums = get_allowed_numbers(fields)
class_allowed = get_class_allowed(fields)
logging.debug("class_allowed: %s" % class_allowed)
error_rate = 0
correct_tickets = []
for line in other_tickets:
    line_correct = True
    nums_to_check = list(map(int, line.split(",")))
    for num in nums_to_check:
        if not num in allowed_nums:
            error_rate += num
            line_correct = False
    if line_correct:
        correct_tickets.append(line)

print(error_rate)
correct_tickets.append(ticket)
correct_tickets = list(map(lambda x: list(map(int, x.split(","))), correct_tickets))
fields_num = len(class_allowed.keys())
logging.debug("correct tickets: %s" % correct_tickets)
logging.debug("fields_num %d" % fields_num)
assert fields_num == len(correct_tickets[0])
field_id_allowed_classes = dict.fromkeys(range(0,fields_num),tuple(class_allowed.keys()))
logging.debug("fields_allowed_classes %s" % field_id_allowed_classes)
for key in field_id_allowed_classes:
    logging.debug("checking field (column): %d" % key)
    for ticket in correct_tickets:
        logging.debug("checking ticket: %s" % ticket)
        for check_class in class_allowed:
            logging.debug("checking field class: '%s'" % check_class)
            logging.debug("ticket field: %d" % ticket[key])
            logging.debug("allowed numbers: %s" % class_allowed[check_class])
            if ticket[key] not in class_allowed[check_class]:
                set_from_tuple = set(field_id_allowed_classes[key])
                set_from_tuple.discard(check_class)
                field_id_allowed_classes[key] = tuple(set_from_tuple)
logging.debug("fields_allowed_classes %s" % field_id_allowed_classes)

actual_classes = {}
while (len(actual_classes) < fields_num):
    actual_class = ""
    for key in field_id_allowed_classes:
        if len(field_id_allowed_classes[key]) == 1:
            actual_class = field_id_allowed_classes[key][0]
            actual_classes[key] = actual_class
            break
    del field_id_allowed_classes[key]
    for key in field_id_allowed_classes:
        set_from_tuple = set(field_id_allowed_classes[key])
        set_from_tuple.discard(actual_class)
        field_id_allowed_classes[key] = tuple(set_from_tuple)
        
logging.debug(actual_classes)
product = 1
for key in actual_classes:
    if actual_classes[key].startswith("departure"):
        product *= ticket[key]
print(product)
