import logging
logging.basicConfig(level=logging.INFO)

def sanitize_bag(bag_string):
    idx = bag_string.find(" bag")
    return bag_string[:idx]

def extract_type_number(num_type_string):
    num_type_string = num_type_string.lstrip()
    idx = num_type_string.find(" ")
    if num_type_string[:idx] == "no":
        return None, None
    num = int(num_type_string[:idx])
    bag_type = num_type_string[idx:].lstrip()
    return bag_type, num

bag_rules = {}
with open("input", "r") as f:
    for line in f:
        container, containees = line.rstrip().split("contain")
        container = sanitize_bag(container)
        containees = tuple(map(extract_type_number, map(sanitize_bag,containees.split(","))))
        this_bag_rule = {}
        for containee in containees:
            bag_type, allowed_num = containee
            if (bag_type):
                this_bag_rule[bag_type] = allowed_num
        bag_rules[container] = this_bag_rule

logging.debug(bag_rules)

# look for bags containing the shiny gold one
target_bag = "shiny gold"
searched_bags = [target_bag]
last_num_allowed_bags = -1
while last_num_allowed_bags != len(searched_bags) - 1:
    last_num_allowed_bags = len(searched_bags) - 1
    for bag in bag_rules:
        for searched_bag in searched_bags:
            if searched_bag in bag_rules[bag]:
                if bag not in searched_bags:
                    searched_bags.append(bag)
    logging.debug("searched bags after full bag rules run: %s" % searched_bags)
print(last_num_allowed_bags)

# sum all the bags contained in the shiny gold one
def count_bags_in_bag(bag):
    logging.debug("counting bags in bag: '%s'" % bag)
    logging.debug("bag rule: '%s'", bag_rules[bag])
    total = 0
    for inner_bag in bag_rules[bag]:
        total += bag_rules[bag][inner_bag] * (count_bags_in_bag(inner_bag) + 1)
    logging.debug("total bags in '%s' bag: %d" % (bag, total))
    return total
print(count_bags_in_bag(target_bag))




