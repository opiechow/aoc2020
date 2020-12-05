#part 1
import math
numbers = []
with open("input", "r") as f:
    for line in f:
        numbers.append(int(line))
others = list(map(lambda x: 2020 - x, numbers))
print(math.prod(set(numbers).intersection(set(others))))

#part 2
sums = sorted(list(others))
nums = sorted(numbers)
sums = list(filter(lambda x: x > nums[0], sums))
nums = list(filter(lambda x: x < sums[-1], nums))
sums = list(filter(lambda x: x > sum(nums[0:2]), sums))
print(sums)
print(nums)
print(201 * 715 * 1104)