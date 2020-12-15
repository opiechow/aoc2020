import logging
import os
import re

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.disable(logging.FATAL)

program = []
with open("input", "r") as f:
    for line in f:
        program.append(line.rstrip().split(" = "))

logging.debug(program)

memory = {}
current_mask = {"set" : 0, "clr" : 0}
for line in program:
    cmd, arg = line
    if cmd == "mask":
        current_mask["set"] = int(arg.replace("0", "X")
                                         .replace("X", "0"), base=2)
        current_mask["clr"] = int(arg.replace("1", "X")
                                         .replace("0", "1")
                                         .replace("X", "0"), base=2)
        logging.debug("in_mask:  {}".format(arg))
        logging.debug("set_mask: {:036b}".format(current_mask["set"]))
        logging.debug("clr_mask: {:036b}".format(current_mask["clr"]))
    else:
        mem_addr = re.search(r"([0-9]+)", cmd).group(0)
        val = int(arg)
        logging.debug("---set mask---".format(val))
        logging.debug("value:  {:036b}".format(val))
        logging.debug("mask:   {:036b}".format(current_mask["set"]))
        val |= current_mask["set"]
        logging.debug("result: {:036b}".format(val))
        logging.debug("---clr mask---".format(val))
        logging.debug("val:    {:036b}".format(val))
        logging.debug("mask:   {:036b}".format(current_mask["clr"]))
        val &= ~current_mask["clr"]
        logging.debug("result: {:036b}".format(val))
        logging.debug("--- result ---".format(val))
        logging.debug("writing {:10d} val to 0x{:04x} addr".format(val, int(mem_addr)))
        memory[mem_addr] = val

print(sum(memory.values()))

# program = []
# with open("test_input2", "r") as f:
#     for line in f:
#         program.append(line.rstrip().split(" = "))

logging.debug(program)

def patternify(addr, mask):
    pattern = []
    addr = "{:036b}".format(addr)
    assert(len(addr) == len(mask))
    for i in range(len(addr)):
        if mask[i] == "X":
            pattern.append("X")
        else:
            pattern.append(addr[i])
    return "".join(pattern)

def not_matching_masks(old_mask, transforming_mask):
    assert(len(old_mask) == len(transforming_mask))
    if len(old_mask) == 1:
        if old_mask == "X":
            if transforming_mask == "X":
                return []
            if transforming_mask == "1":
                return ["0"]
            if transforming_mask == "0":
                return ["1"]
            assert(0)
        if old_mask != transforming_mask and transforming_mask != "X":
            return [old_mask]
        else:
            return [] 
    # end of base case
    masks = []
    if old_mask[0] == "X":
        if transforming_mask[0] == "1":
            masks.append("".join(("0", old_mask[1:])))
            for mask in not_matching_masks(old_mask[1:], transforming_mask[1:]):
                masks.append("".join(("1", mask)))
        if transforming_mask[0] == "0":
            masks.append("".join(("1", old_mask[1:])))
            for mask in not_matching_masks(old_mask[1:], transforming_mask[1:]):
                masks.append("".join(("0", mask)))
        if transforming_mask[0] == "X":
            for mask in not_matching_masks(old_mask[1:], transforming_mask[1:]):
                masks.append("".join(("X", mask)))
    if old_mask[0] == "0":
        if transforming_mask[0] == "X" or transforming_mask[0] == "0":
            for mask in not_matching_masks(old_mask[1:], transforming_mask[1:]):
                masks.append("".join(("0", mask)))
        if transforming_mask[0] == "1":
            masks.append("".join(("0", old_mask[1:])))
    if old_mask[0] == "1":
        if transforming_mask[0] == "X" or transforming_mask[0] == "1":
            for mask in not_matching_masks(old_mask[1:], transforming_mask[1:]):
                masks.append("".join(("1", mask)))
        if transforming_mask[0] == "0":
            masks.append("".join(("1", old_mask[1:])))
    return masks

def memory_write(addr, val, mask, mask_values):
    set_mask = int(mask.replace("0", "X").replace("X", "0"), base=2)
    logging.info("addr: {:036b}".format(addr))
    addr |= set_mask
    logging.info("mask: {:36s}".format(mask))
    logging.info("addr: {:036b}".format(addr))

    pattern = patternify(addr, mask)
    logging.info("pttr: {:36s}".format(pattern))
    logging.info(mask_values)
    new_dict = {}
    for old_key in mask_values:
        logging.info("old_key: {:36s}".format(old_key))
        logging.info("pattern: {:36s}".format(pattern))
        new_keys = not_matching_masks(old_key, pattern)
        logging.info("new keys: %s" % new_keys)
        for new_key in new_keys:
            new_dict[new_key] = mask_values[old_key]
    new_dict[pattern] = val
    return new_dict
    

mask_values = {}

for line in program:
    logging.info("processing %s", line)
    cmd, arg = line
    if cmd == "mask":
        current_mask = arg
    else:
        base_addr = re.search(r"([0-9]+)", cmd).group(0)
        val = int(arg)
        mask_values = memory_write(int(base_addr), val, current_mask, mask_values)
    logging.info("mask_values after last iteration:")
    for key in mask_values:
        logging.info("{:36s}: {:d}".format(key,mask_values[key]))
        logging.info(key.count("X"))
    
total = 0
for key in mask_values:
    calculated = mask_values[key] * 2**key.count("X")
    total += calculated
print(total)

57021454080
53367562662
78968085342
38647331616
2747291119060