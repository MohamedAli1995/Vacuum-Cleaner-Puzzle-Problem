from Puzzle import VacuumCleanerPuzzle as Puzzle
from PuzzleSolver import solve


def read_file(test_file):
    lines = [list(line.strip()) for line in open(test_file, 'r').readlines()]
    return tuple(tuple(r) for r in lines)


def test(test_file):
    state = Puzzle.State(read_file(test_file))
    print("Initial State:")
    print(state)
    print("Heuristic:", Puzzle.get_heuristic(state))
    actions = solve(state)
    directions = {(1, 0): 'right', (-1, 0): 'left', (0, 1): 'down', (0, -1): 'up'}
    if actions is None:
        print("This puzzle is not solvable.")
    else:
        print("Solution:")
        path_cost = 0
        for index, action in enumerate(actions):
            action_cost = Puzzle.get_action_cost(state, action)
            state = Puzzle.apply_action(state, action)
            print("Step", index+1, ":", directions[action])
            print(state)
            print("Step cost:", action_cost)
            print("Heuristic:", Puzzle.get_heuristic(state))
            path_cost += action_cost
        print("Solved in", len(actions), "steps:", ','.join(directions[action] for action in actions))
        print("Total path cost:", path_cost)
        print("Number of generated states:", Puzzle.State.Count)


if __name__ == '__main__':
    test('test2.txt')
