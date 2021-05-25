import collections
import numpy as np
import logging
import random
import math
import re

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
#logging.disable(logging.DEBUG)

def get_array_from_lines(rows):
    new_rows = []
    for row in rows:
        new_row = list(row.replace("#", "1").replace(".", "0"))
        new_rows.append(list(map(int,new_row)))
    return np.array(new_rows)

def repr_row_to_puzzle_str(row):
    puzzle_str = ""
    for elem in row:
        if elem:
            puzzle_str += "#"
        else:
            puzzle_str += "."
    return puzzle_str

def get_repr_string(rep):
    repr_string = ""
    rows = rep.shape[1]
    for row in range(rows):
        repr_string += repr_row_to_puzzle_str(rep[row,:])
        repr_string += "\n"
    return repr_string


class Puzzle(object):
    def __init__(self, puzzle_id, rows):
        self._id = puzzle_id
        self._repr = get_array_from_lines(rows)
        self._orientation = 0

    def __str__(self):
        puzzle_id_str = "PUZZLE DUMP\nPuzzle id: {}\n".format(self._id) + "\n"
        puzzle_repr_str = get_repr_string(self._repr) + "\n"
        puzzle_border_str = self._get_border_string() + "\nPUZZLE DUMP END"
        return puzzle_id_str + puzzle_repr_str + puzzle_border_str
    
    def __repr__(self):
            return "Puzzle ID: {}".format(self._id) 

    def _get_border_string(self):
        repr_string  = "N: " + self.get_north() + "\n"
        repr_string += "E: " + self.get_east() + "\n"
        repr_string += "W: " + self.get_west() + "\n"
        repr_string += "S: " + self.get_south() + "\n"
        return repr_string

    def get_raw_repr(self):
        return self._repr

    def rotate(self):
        self._orientation += 1
        if self._orientation == 8:
            self._orientation = 0
        self._repr = np.rot90(self._repr, 1)
        if self._orientation % 4 == 0  :
            self._repr = np.fliplr(self._repr)

    def get_north(self):
        return repr_row_to_puzzle_str(self._repr[ 0, :])
            
    def get_south(self):
        return repr_row_to_puzzle_str(self._repr[-1, :])
            
    def get_east(self):
        return repr_row_to_puzzle_str(self._repr[:, -1])
            
    def get_west(self):
        return repr_row_to_puzzle_str(self._repr[:,  0])

    def get_id(self):
        return int(self._id)
            
def go_dir(puzzle, puzzles_left, direction):
    #logging.debug(puzzles_left)
    match_candidates = []
    old_puzzle_border = {"N" : puzzle.get_north(),
                         "S" : puzzle.get_south(),
                         "E" : puzzle.get_east(),
                         "W" : puzzle.get_west()}
    for fitted_puzzle in puzzles_left:
        for     i in range(8):
            new_puzzle_border = {"N" : fitted_puzzle.get_south(),
                                 "S" : fitted_puzzle.get_north(),
                                 "E" : fitted_puzzle.get_west(),
                                 "W" : fitted_puzzle.get_east()}
            if new_puzzle_border[direction] == old_puzzle_border[direction]:
                match_candidates.append(fitted_puzzle)
                break
            fitted_puzzle.rotate()
    logging.debug(match_candidates)
    assert(len(match_candidates) <= 1)
    return match_candidates


def load_input(filename):
    puzzles = {}
    with open(filename) as f:
        for line in f:
            if line.startswith("Tile "):
                curr_id = re.findall(r"[0-9]+", line)[0]
                puzzles[curr_id] = []
            elif line.rstrip():
                puzzles[curr_id].append(line.rstrip())
    return puzzles

if __name__ == "__main__":
    puzzle_dict = load_input("input")
    puzzle_list = []
    for key in puzzle_dict:
        puzzle_list.append(Puzzle(key, puzzle_dict[key]))
    puzzle_grid_size = int(math.sqrt(len(puzzle_list)))
    logging.debug("Grid size: {}".format(puzzle_grid_size))
    

    edges = []
    for puzzle in puzzle_list:
        placed_puzzles = []
        start_puzzle = puzzle
        placed_puzzles.append(start_puzzle)
        logging.debug("Selected puzzle: {}".format(start_puzzle))
        dirs = ["N", "S", "E", "W"]
        dir_puzzles = {}
        for direction in dirs:
            puzzles_left = list(set(puzzle_list).difference(set(placed_puzzles)))
            puzzles_in_dir = go_dir(start_puzzle, puzzles_left, direction)
            dir_puzzles[direction] = puzzles_in_dir
        logging.debug(dir_puzzles)
        count = 0
        for key in dir_puzzles:
            if dir_puzzles[key]:
                count += 1
        if count == 2:
            edges.append(puzzle.get_id())

print(edges)
print(np.prod(edges))

