import logging

logging.basicConfig(format='|%(asctime)s|%(levelname)s|%(message)s', level=logging.DEBUG)
logging.disable(logging.FATAL)

def extract_group_answers(filename):
    all_groups_answers = []
    with open(filename, "r") as f:
        group_answers = []
        for line in f:
            if line == "\n":
                all_groups_answers.append(group_answers)
                group_answers = []
            else:
                group_answers.append(line.rstrip())
    return all_groups_answers

def count_unique_group_answers(group_answers):
    answers = set()
    for person_answer in group_answers:
        answers.update(list(person_answer))
    return(len(answers))

def count_all_group_answers(group_answers):
    people_num = len(group_answers)
    answers = {}
    for person_answer in group_answers:
        for letter in person_answer:
            if not letter in answers:
                answers[letter] = 1
            else:
                answers[letter] += 1
    logging.debug(answers)
    everyone_answered_num = 0
    for val in answers.values():
        if val == people_num:
            everyone_answered_num += 1
    return everyone_answered_num

group_answers = extract_group_answers("input")
num_answers = list(map(count_unique_group_answers, group_answers))
print(sum(num_answers))
num_answers = list(map(count_all_group_answers, group_answers))
print(sum(num_answers))
