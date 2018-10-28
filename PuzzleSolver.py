from Puzzle import VacuumCleanerPuzzle as Puzzle
from queue import PriorityQueue


# Helpful Notes:
# To create a priority queue: queue = PriorityQueue()
# Useful function include:
# queue.put(item) : adds an item to the queue
# queue.get() : gets (and removes) the item with the least value
# Useful Tricks:
# queue can be implicitly cast into a boolean which will be False if empty and True otherwise
# When tuples are compared, their components are compared in order
# so (1,10) < (2,3) since 1 < 2 and (1,2) < (1,3) since 1==1 and 2<3
# so if you wish to use a custom priority, you can insert a tuple which contains (priority, item) instead of the item


# Given an initial state, return a list of actions to reach the goal state.
# def solve(state):
#     # TODO: Write an A* search algorithm to solve VacuumCleanerPuzzle
#     Q = []
#     nodes = {state: (None, None)}
#     Q.append(state)
#     while Q:
#         current = Q.pop(0)
#         if Puzzle.is_goal(current):
#             actions = []
#             while True:
#                 current, action = nodes[current]
#                 if action is None:
#                     return actions[::-1]
#                 actions.append(action)
#         for action in Puzzle.get_possible_actions(current):
#             child = Puzzle.apply_action(current, action)
#             if child not in nodes:
#                 nodes[child] = (current, action)
#                 Q.append(child)


def solve(state):
    # TODO: Write an A* search algorithm to solve VacuumCleanerPuzzle
    Q = PriorityQueue()
    f = 0 + state.h
    Q.put((f, state))
    nodes = {state: (None, None, None)}
    while Q:
        (f, current) = Q.get()
        if Puzzle.is_goal(current):
            actions = []
            while True:
                current, action, f = nodes[current]
                if action is None:
                    return actions[::-1]
                actions.append(action)
        for action in Puzzle.get_possible_actions(current):
            child = Puzzle.apply_action(current, action)
            child_f = f - current.h + current.weight + child.h

            if child not in nodes:
                nodes[child] = (current, action, child_f)
                Q.put((child_f, child))
            else:
                _, _, old_f = nodes[child]
                if old_f is not None:
                    if child_f < old_f:
                        nodes[child] = (current, action, child_f)
                        Q.put((child_f, child))
