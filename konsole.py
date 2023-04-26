import numpy as np

cube = np.zeros((3,3,3))

path = [3, 2, 2, 2, 2, 2, 3, 2, 3, 2, 2, 2, 2, 3, 2, 3, 2, 2, 2, 3]

# Print a visual representation of the path
def visualize_path(path):
    # Store the current cursor position
    cursor = (0, 0)
    # Store the current direction
    vertical = False
    page = False
    print('X', end='')
    # Iterate over the path and print path to console as X's first horizontally, then vertically
    for i in path:
        i -= 1
        if vertical:
            for j in range(i):      
                print('')
                print(' ' * cursor[1] + 'X', end='')
                cursor = (cursor[0] + 1, cursor[1])
        else:
            print('X' * i, end='')
            cursor = (cursor[0], cursor[1] + i)
        vertical = not vertical
            
            
visualize_path(path)

def start_positions(cube):
    for x in range(cube.shape[0]):
        for y in range(cube.shape[1]):
            for z in range(cube.shape[2]):
                yield (x, y, z)

def can_place(cube, position):
    return (position[0] < cube.shape[0] and
            position[1] < cube.shape[1] and
            position[2] < cube.shape[2] and
            position[0] >= 0 and
            position[1] >= 0 and
            position[2] >= 0 and
            cube[position] == 0)

def all_vectors():
    yield (-1,  0,  0)
    yield ( 1,  0,  0)
    yield ( 0, -1,  0)
    yield ( 0,  1,  0)
    yield ( 0,  0, -1)
    yield ( 0,  0,  1)

def place_positions(cube, position, ban_direction, length):
    for vector in (v for v in all_vectors() if v != ban_direction):
        solution = cube.copy()
        next_pos = None
        for i in range(length-1):
            next_pos = tuple(np.asarray(position) + np.asarray(vector) * (i + 1)) 
            if not can_place(solution, next_pos):
                solution = None
                break
            solution[next_pos] = 1
        if solution is not None:
            yield (solution, next_pos, vector)
                
def step_solutions(cube, position, last_dir, path, depth=0):
    if (len(path) == 0):
        assert(np.sum(cube) == 27)
        print("Found solution!")
        return True

    global step_count
    step_count += 1
    for solution, next_position, direction in place_positions(cube, position, last_dir, path[0]):
        if step_solutions(solution, next_position, direction, path[1:], depth+1):
            print()
            print("Depth: " + str(depth))
            print(str(solution))
            return True
    return False

def solve(path):
    cube = np.zeros((3,3,3))
    steps = [cube]
    for position in start_positions(cube):
        start = cube.copy()
        start[(position)] = 1
        print ("Starting position:" + str(position))
        if step_solutions(start, position, None, path):
            print("Step count: " + str(step_count))
            break

step_count = 0
solve(path)