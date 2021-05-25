import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
logging.disable(logging.FATAL)

def load_rules_n_samples(filename):
    rules = {}
    examples = []
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip()
            if ":" in line:
                rule_id, rule = line.split(":")
                or_list = rule.split("|")
                or_list = list(map(lambda x: list(map(lambda x: int(x) if x.isnumeric() else x[1], x.split())), or_list))
                rules[int(rule_id)] = or_list
            elif line:
                examples.append(line)
    return rules, examples

#in:  single int key
#out  set of allowed strings
def resolve_rule(rules_resolved, int_key):
    if int_key in rules_resolved:
        return rules_resolved[int_key]
    allowed_strings_set = set()
    or_list = rules[int_key]
    for sequence in or_list:
        string_combos = []
        for elem in sequence:
            if elem == int_key:
                if elem == 8:
                    wildcard = "x"
                elif elem == 11:
                    wildcard = "y"
                string_combos.append(set((wildcard,)))
            else:
                string_combos.append(resolve_rule(rules_resolved, elem))
        possible_strings = string_combos[0]
        for i in range(1, len(string_combos)):
            temp = []
            for beg_string in possible_strings:
                for end_string in string_combos[i]:
                    temp.append("".join((beg_string, end_string)))
            possible_strings = temp
        allowed_strings_set.update(possible_strings)
    rules_resolved[int_key] = allowed_strings_set
    return allowed_strings_set

rules, examples = load_rules_n_samples("input_mod")
# logging.debug("rules: %s" % rules)
# logging.debug("examples: %s" % examples)
rules_resolved = {}
for rule in rules:
    for sequence in rules[rule]:
        for elem in sequence:
            if elem == "a" or elem == "b":
                rules_resolved[rule] = set(sequence)
# logging.debug("init rules resolved: %s" % rules_resolved)
for rule in rules:
    resolve_rule(rules_resolved, rule)
# logging.debug("rules resolved: %s" % rules_resolved)
# logging.debug("rule 31: %s" % rules_resolved[31])

# logging.debug("rule 8: %s" % rules_resolved[8])
# logging.debug("rule 11: %s" % rules_resolved[11])
# logging.debug("rule 0: %s" % rules_resolved[0])
count = 0
# part 1
for example in examples:
    if example in rules_resolved[0]:
        count += 1
print(count)
# part 2

def rule_len(rules_resolved, rule_no):
    for rule in rules_resolved[rule_no]:
        return len(rule)

def x_multiple(rules_resolved):
    return(rule_len(rules_resolved, 42))

def y_multiple(rules_resolved):
    return rule_len(rules_resolved, 42) + rule_len(rules_resolved, 31)

def check_x(rules_resolved, string_to_check):
    if string_to_check == "":
        return True
    if string_to_check in rules_resolved[42]:
        return True
    return False

def check_y(rules_resolved, string_to_check):
    if string_to_check == "":
        return True
    len_42 = rule_len(rules_resolved, 42)
    len_31 = rule_len(rules_resolved, 31)
    return string_to_check[:len_42] in rules_resolved[42] and \
           check_y(rules_resolved, string_to_check[len_42:-len_31]) and \
           string_to_check[-len_31:] in rules_resolved[31]

def check_middle_string(rules_resolved, required_parts, required_parts_lens, string_to_check):
    if string_to_check in required_parts[1]:
        return True
    x_len = x_multiple(rules_resolved)
    y_len = y_multiple(rules_resolved)
    while len(string_to_check):
        while string_to_check[:required_parts_lens[1]] not in required_parts[1]:
            if check_x(rules_resolved, string_to_check[:x_len]):
                string_to_check = string_to_check[x_len:]
            else:
                return False
        # here required parts 1 is satisfied
        if check_y(rules_resolved, string_to_check[required_parts_lens[1]:]):
            return True
        else:
            if check_x(rules_resolved, string_to_check[:x_len]):
                string_to_check = string_to_check[x_len:]
            else:
                return False
    return False

required_parts = {0 : set(), 1 : set(), 2 : set()}
required_parts_lens = {0: 0, 1: 0, 2: 0}
test_patterns = []
for pattern in rules_resolved[0]:
    if "x" in pattern and "y" in pattern:
        x_pos = pattern.find("x")
        y_pos = pattern.find("y")
        required_parts[0].add(pattern[:x_pos])
        required_parts_lens[0] = len(pattern[:x_pos])
        required_parts[1].add(pattern[x_pos+1:y_pos])
        required_parts_lens[1] = len(pattern[x_pos+1:y_pos])
        required_parts[2].add(pattern[y_pos+1:])
        required_parts_lens[2] = len(pattern[y_pos+1:])
    elif not "x" in pattern and not "y" in pattern:
        test_patterns.append(pattern)
logging.debug("req parts: %s" % required_parts)
# logging.debug("req parts: %s" % required_parts_lens)
# logging.debug("rule 42: %s" % rules_resolved[42])
count = 0
for example in examples:
    logging.debug("current example: %s" % example)
    if len(example) < required_parts_lens[0] + \
                      required_parts_lens[1] + \
                      required_parts_lens[2]:
        continue
    if example[:required_parts_lens[0]] not in required_parts[0]:
        continue
    example = example[required_parts_lens[0]:]
    if example[-required_parts_lens[2]:] not in required_parts[2]:
        continue
    example = example[:-required_parts_lens[2]]
    logging.debug("example left to check: %s" % example)
    if check_middle_string(rules_resolved, required_parts, required_parts_lens, example):
        count += 1
        logging.debug("+1")
print(count)
    

