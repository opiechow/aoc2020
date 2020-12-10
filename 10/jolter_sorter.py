import logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
logging.disable(logging.FATAL)

def count_differences(sorted_adapters):
    diffs = {}
    for i in range(len(sorted_adapters) - 1):
        diff = sorted_adapters[i+1] - sorted_adapters[i]
        if diff in diffs:
            diffs[diff] += 1
        else:
            diffs[diff] = 1
    return diffs

def add_laptop_adapter(adapter_list):
    adapter_list.append(max(adapter_list) + 3)

def add_charging_outlet(adapter_list):
    adapter_list.append(0)

def prepare_list(in_list):
    add_charging_outlet(in_list)
    add_laptop_adapter(in_list)
    in_list.sort()
    logging.debug("sorted list: %s", in_list)

def get_diffs(in_list):
    diffs = count_differences(in_list)
    logging.debug("diffs: %s", diffs)
    return diffs

def get_result(in_list):
    prepare_list(in_list)
    diffs = get_diffs(in_list)
    return diffs[1] * diffs[3]    

def count_possible(current, in_list, result_cache):
    logging.debug("count possible | current %d" % current)
    if current in result_cache:
        count = result_cache[current]
        logging.debug("count possible | retrived %d from cache" % count)
        return count
    possibilities = (current + 1, current + 2, current + 3)
    logging.debug("count possible | possibilities: %s" % (possibilities, ))
    count = 0
    for number in possibilities:
        if number in in_list:
            count += count_possible(number, in_list, result_cache)
    result_cache[current] = count
    return count

def get_count_of_arrangements(in_list):
    logging.debug("looking for arrangements in: %s" % in_list)
    logging.debug("start: %d stop: %d" % (in_list[0], in_list[-1]))
    result_cache = {}
    #recurrence base case
    result_cache[in_list[-1]] = 1
    count = count_possible(0, in_list, result_cache)
    return count

test_ins = []
test_outs = []
for i in (1, 2):
    joltages = []
    with open("test_input_{}".format(i), "r") as f:
        for line in f:
            joltages.append(int(line.rstrip()))
    test_ins.append(joltages)
    results = []
    with open("test_output_{}".format(i), "r") as f:
        for line in f:
            results.append(int(line.rstrip()))
    test_outs.append(results)

logging.debug("test_ins: %s, test_outs: %s" % (test_ins, test_outs))

for test in zip(test_ins, test_outs):
    assert(get_result(test[0]) == test[1][0])
    assert(get_count_of_arrangements(test[0]) == test[1][1])

actual_in = []  
with open("input", "r") as f:
    for line in f:
        actual_in.append(int(line.rstrip()))
print(get_result(actual_in))
print(get_count_of_arrangements(actual_in))
