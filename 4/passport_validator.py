def passport_valid(dict_passport, required_fields):
    print(dict_passport)
    for field in required_fields:
        if not field in dict_passport:
            return False
    print("required fields check passed")
    if len(dict_passport["byr"]) != 4:
        return False
    byr = int(dict_passport["byr"])
    if byr < 1920 or byr > 2002:
        return False
    print("byr check passed")
    if len(dict_passport["iyr"]) != 4:
        return False
    iyr = int(dict_passport["iyr"])
    if iyr < 2010 or iyr > 2020:
        return False
    print("iyr check passed")
    if len(dict_passport["eyr"]) != 4:
        return False
    eyr = int(dict_passport["eyr"])
    if eyr < 2020 or eyr > 2030:
        return False
    print("eyr check passed")
    hgt = dict_passport["hgt"]
    cm_pos = hgt.find("cm")
    in_pos = hgt.find("in")
    if in_pos == -1 and cm_pos == -1:
        return False
    if in_pos > -1 and cm_pos > -1:
        return False
    if in_pos > -1:
        in_val = int(hgt[:in_pos])
        if in_val < 59 or in_val > 76:
            return False
    if cm_pos > -1:
        cm_val = int(hgt[:cm_pos])
        if cm_val < 150 or cm_val > 193:
            return False
    print("hgt check passed")
    hcl = dict_passport["hcl"]
    if(len(hcl)) != 7:
        return False
    if hcl[0] != "#":
        return False
    hcl_val = -1
    try:
        hcl_val = int(hcl[1:], 16)
    except ValueError:
        return False
    if hcl_val < 0 or hcl_val > 0xffffff:
        return False
    print("hcl check passed")
    ecl = dict_passport["ecl"]
    if not ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False
    print("ecl check passed")
    pid = -1
    if len(dict_passport["pid"]) != 9:
        return False
    try:
        pid = int(dict_passport["pid"])
    except ValueError:
        return False
    if pid < 0 or pid > 999999999:
        return False
    print("pid check passed")
    print("all checks passed")
    return True
                
passports = []
current_passport = []
with open("input", "r") as f:
    for line in f:
        if line == "\n":
            passports.append(current_passport)
            current_passport = []
            continue
        current_passport.extend(line.split())

dict_passports = []
for passport in passports:
    dict_passport = {}
    for entry in passport:
        key, val = entry.split(":")
        dict_passport[key] = val
    dict_passports.append(dict_passport)

valid_passports = 0
required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
for passport in dict_passports:
    if passport_valid(passport, required_fields):
        valid_passports += 1
print(valid_passports)
