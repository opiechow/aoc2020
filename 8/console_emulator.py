import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.disable(logging.FATAL)

code = []
with open("input", "r") as f:
    for line in f:
        code.append(line.rstrip())

logging.debug("code: '%s'" % code)

def run(code):
    acc = 0
    #points to the instruction about to be executed
    pc = 0
    line_exec_count = {}
    while pc < len(code):
        instruction, argument = code[pc].split(" ")
        if pc in line_exec_count:
            # our break condition!
            return False, acc
        else:
            line_exec_count[pc] = 1
        if instruction == "nop":
            pc += 1
        elif instruction == "acc":
            acc += int(argument)
            pc += 1
        elif instruction == "jmp":
            pc += int(argument)
        else:
            raise UnsupportedOperationError
    return True, acc

#part 1 result
clean_exit, acc = run(code)
print(acc)

#part 2
pc_test = 0
while pc_test < len(code):
    old_line = code[pc_test]
    op, arg = old_line.split(" ")
    if op == "jmp":
        op = "nop"
    elif op == "nop":
        op = "jmp"
    new_line = " ".join((op, arg))
    code[pc_test] = new_line
    clean_exit, acc = run(code)
    if clean_exit:
        break
    # it wasn't this line :(
    code[pc_test] = old_line
    pc_test += 1

if clean_exit:
    print(acc)
else:
    print("cows can fly")







