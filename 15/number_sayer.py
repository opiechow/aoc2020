import logging
import os 

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
logging.disable(logging.DEBUG)
tests_enable = True

def get_sample_no(first_samples, sample_no):
    # doesn't contain the last one
    last_seen = {}
    for idx, val in enumerate(first_samples[:-1]):
        last_seen[val] = idx
    samples = first_samples[:]
    while len(samples) < sample_no:
        last_said = samples[-1]
        if last_said in last_seen:
            logging.debug("last said seen, appending dist: %d" % dist)
            last_said_idx = len(samples) - 1
            dist = last_said_idx - last_seen[last_said]
        else:
            logging.debug("last said %d not seen, appending 0" % last_said)
            dist = 0
        samples.append(dist)
        last_seen_not_last = len(samples) - 2
        last_seen[samples[last_seen_not_last]] = last_seen_not_last
        if len(samples) % 1000000 == 0:
            logging.info("{} / {} samples calculated"
            .format(len(samples), sample_no))
    return samples[sample_no - 1]

if tests_enable:
    test_ins = []
    with open("test_inputs", "r") as f:
        for line in f:
            test_ins.append(list(map(int, line.rstrip().split(","))))
    test_outs = []
    with open("test_outputs", "r") as f:
        for line in f:
            test_outs.append(int(line.rstrip()))
    logging.debug("test_ins: %s, test_outs: %s" % (test_ins, test_outs))
    for test in zip(test_ins, test_outs):
        test_in, test_out = test
        assert(get_sample_no(test_in, 2020) == test_out)

actual_in = []  
with open("input", "r") as f:
    for line in f:
        actual_in.append(list(map(int, line.rstrip().split(","))))
logging.debug("actual in: %s" % actual_in)

print(get_sample_no(*actual_in, 2020))
print(get_sample_no(*actual_in, 30000000 ))