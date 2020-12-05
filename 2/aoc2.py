line = "6-11 v: kvvvvvvmvvdv"

def line_check(line):
    policy, password = line.split(":")
    policy_range, policy_letter = policy.split(" ")
    policy_min, policy_max = policy_range.split("-")
    check = password.count(policy_letter)
    if check >= int(policy_min) and check <= int(policy_max):
        return 1
    else:
        return 0

def line_check2(line):
    policy, password = line.split(":")
    policy_range, policy_letter = policy.split(" ")
    policy_first_pos, policy_second_pos = policy_range.split("-")
    # Use the fact that password contains " " at 0 - first letter is at 1
    policy_first_pos = int(policy_first_pos)
    policy_second_pos = int(policy_second_pos)
    new_string = "".join((password[policy_first_pos], password[policy_second_pos]))
    check = new_string.count(policy_letter)
    if check == 1:
        return 1
    else:
        return 0


lines = []
with open ("input", "r") as f:
    for line in f:
        lines.append(line.rstrip())
correct_lines = map(line_check, lines[:])
print(sum(correct_lines))

correct_lines2 = map(line_check2, lines[:])
print(sum(correct_lines2))

