from collections import Counter

class Puzzle(object):
    def __init__(self, id, map):
        self._id = id
        self._map = map

    def get_border(self, direction):
        if direction == "N":
            return self._map[0]
        if direction == "E":
            border = ""
            for line in self._map:
                border = "".join((border, line[-1]))
            return border
        if direction == "S":
            return self._map[-1]
        if direction == "W":
            border = ""
            for line in self._map:
                border = "".join((border, line[0]))
            return border
    
    def get_all_borders(self):
        borders = []
        for direction in ("N", "E", "S", "W"):
            borders.append(self.get_border(direction))
        return borders

    def get_id(self):
        return self._id

    def full_flip(self):
        new_map = []
        for line in self._map[::-1]:
            new_map.append(line[::-1])
        self._map = new_map

def load_puzzles(filename):
    puzzles = []
    with open(filename, "r") as f:
        current_id = 0
        current_puzzle_map = []
        for line in f:
            line = line.rstrip()
            if "Tile" in line:
                current_id = int(line[5:-1])
            elif not line:
                puzzles.append(Puzzle(current_id, current_puzzle_map))
                current_id = 0
                current_puzzle_map = []
            else:
                current_puzzle_map.append(line)
    return puzzles

puzzles = load_puzzles("input")

border_list = []
for puzzle in puzzles:
    border_list.extend(puzzle.get_all_borders())
border_counts = Counter(border_list)
corner_candidates = []
for puzzle in puzzles:
    print(puzzle.get_id())
    unique_borders = 0
    for border in puzzle.get_all_borders():
        if border_counts[border] == 1:
            unique_borders += 1
    if unique_borders == 2:
        corner_candidates.append(puzzle.get_id())
        puzzle.full_flip()
print(corner_candidates)

corner_ids = []
border_list = []
for puzzle in puzzles:
    border_list.extend(puzzle.get_all_borders())
border_counts = Counter(border_list)
print(border_counts)
for puzzle in puzzles:
    unique_borders = 0
    for border in puzzle.get_all_borders():
        if border_counts[border] == 1:
            unique_borders += 1
    if unique_borders == 2:
        corner_ids.append(puzzle.get_id())
print(corner_candidates)
print(corner_ids)
print(set(corner_candidates).difference(set(corner_ids)))