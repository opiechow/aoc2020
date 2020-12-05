def extract_map_of_slope(filename):
    rows = []
    with open(filename, "r") as f:
        for row in f:
            rows.append(row.rstrip())
    return rows

def check_slope(map_of_slope, right, down):
    num_rows = len(map_of_slope)
    num_cols = len(map_of_slope[0])
    col = 0
    row = 0
    trees = 0
    while (row < num_rows):
        if map_of_slope[row][col] == '#':
            trees += 1
        col = (col + right) % num_cols
        row += down
    return trees

map_of_slope = extract_map_of_slope("input")
trees = check_slope(map_of_slope, 3, 1)
print(trees)

slopes_to_check = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
result = 1
for slope_to_check in slopes_to_check:
    result *= check_slope(map_of_slope, slope_to_check[0], slope_to_check[1])
print(result)