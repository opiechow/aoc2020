import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.disable(logging.FATAL)

class XmasChecker():  
    # Data structure:
    # Triangle table of sums
    # +--------+--------+--------+--------+
    # |   --   |   X1   |   X2   |   X3   |
    # +--------+--------+--------+--------+
    # |   X1   |   --   |   --   |   --   |
    # +--------+--------+--------+--------+
    # |   X2   | X1 +X2 |   --   |   --   |
    # +--------+--------+--------+--------+
    # |   X3   | X1 +X3 | X2 +X3 |   --   |
    # +--------+--------+--------+--------+
    def __init__(self, init_vals):
        self._vals = init_vals
        self._flat_triangle = [] # First goes down, then goes left
        N = len(self._vals)
        for i in range(N):
            for j in range(i+1, N):
                summed = self._vals[i] + self._vals[j]
                self._flat_triangle.append(summed)
        logging.debug(self._flat_triangle)
        assert(len(self._flat_triangle) == N*(N-1)/2)
    
    # 1. Remove old first column
    # 2. Calculate new last row
    # 3. Use those to make a new triangle
    def update(self, num):
        # Updating base (not summed) values
        logging.debug("Vals before update: %s" % self._vals)
        self._vals.pop(0)
        self._vals.append(num)
        logging.debug("Vals after update: %s" % self._vals)
        N = len(self._vals)
        # Removing old column
        keep_values = self._flat_triangle[N-1:]
        logging.debug("Keeping sums: %s" % keep_values)
        # Calculating new last row
        new_values = []
        for i in range(N-1):
            new_values.append(num + self._vals[i])
        logging.debug("New sums: %s" % new_values)
        # Construct new triangle
        new_triangle = []
        idxs = []
        for i in range(N-1):
            idxs.append(N-1-i)
        for i in range(1, N-1):
            idxs[i] = idxs[i] + idxs[i-1]
        logging.debug(idxs)
        for idx, value in enumerate(new_values):
            logging.debug("Inserting value: %d @ %d" % (value, idxs[idx] - 1))
            keep_values.insert(idxs[idx] - 1, value)
        new_triangle = keep_values
        logging.debug("New triangle: %s" % new_triangle)
        self._flat_triangle = new_triangle       

    def check(self, num):
        return num in self._flat_triangle

def main(filename):
    numbers = []
    with open(filename, "r") as f:
        for line in f:
            numbers.append(int(line))
    if filename == "test_input":
        len_check = 5
    elif filename == "input":
        len_check = 25
    else:
        raise NoSuchTestError

    x = XmasChecker(numbers[:len_check])
    for number in numbers[len_check:]:
        if not x.check(number):
            print(number)
            break
        x.update(number)

    # I'm tired with part 1. Let's go O(N^2)
    range_sum = number
    for range_len in range (2, len(numbers)):
        for beg_idx in range(0, len(numbers) - range_len):
            checked_range = numbers[beg_idx:beg_idx+range_len]
            checked_sum = sum(checked_range)
            if checked_sum == range_sum:
                print(min(checked_range) + max(checked_range))
            
if __name__ == "__main__":
    main("input")
