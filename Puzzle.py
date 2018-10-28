# Class containing static methods for N-Puzzle
class VacuumCleanerPuzzle:
    NO_HEURISTIC = 0
    HEURISTIC_NEAREST_NODE = 1
    HEURISTIC_FARTHEST_NODE = 2
    HEURISTIC_MEAN_MANHATTEN = 3
    HEURISTIC_FARTHEST_NEAREST_NODE = 4

    HEURISTIC = HEURISTIC_FARTHEST_NEAREST_NODE
    CLEANER_SYMBOL = '@'
    WALL_SYMBOL = '#'
    DIRT_SYMBOL = '*'
    EMPTY_SYMBOL = '.'

    # State class containing the tile grid and location of the empty tile
    # This class is immutable
    class State:
        __slots__ = ["level", "position", "weight", "h"]

        # Stores the number of times as a state is initialized
        Count = 0
        # Create a new from a grid and optionally the empty tile location which is automatically calculated if not given
        def __init__(self, level, weight=1, position=None, h=0):
            VacuumCleanerPuzzle.State.Count += 1
            position = position or next(((x, y) for y, x in enumerate(
                next((x for x, i in enumerate(r) if i == VacuumCleanerPuzzle.CLEANER_SYMBOL), -1) for r in level) if
                                         x >= 0),
                                        (-1, -1))
            assert position[0] >= 0 and position[1] >= 0, 'No player found'
            super().__setattr__("level", level)
            super().__setattr__("position", position)
            super().__setattr__("weight", weight)
            super().__setattr__("h", VacuumCleanerPuzzle.get_heuristic(self))

        # Disable setting attributes after the initializer is called
        def __setattr__(self, key, value):
            raise AttributeError("State is immutable")

        # Get an item from location (x,y). Can be used like this: state[x, y]
        def __getitem__(self, pos):
            return self.level[pos[1]][pos[0]]

        # Get the grid size along the x-axis (in 8-puzzle it should return 3)
        @property
        def width(self):
            return len(self.level[0])

        # Get the grid size along the y-axis (in 8-puzzle it should return 3)
        @property
        def height(self):
            return len(self.level)

        # Get the hash of the state. Enables using the state with sets and dictionaries
        def __hash__(self):
            return hash((self.level, self.weight))

        # Equality comparison for states. Enables using the state with sets and dictionaries
        def __eq__(self, other):
            return self.level == other.level and self.weight == other.weight

        # Support casting state to string
        def __str__(self):
            return '\n'.join(''.join(i for i in r) for r in self.level) + '\nWeight: {}'.format(self.weight)

        # Dummy support for "<" to enable using the state with priority queues
        def __lt__(self, other):
            return False

    # Gets all possible actions for any state
    @staticmethod
    def get_possible_actions(state):
        actions = []
        pos = state.position
        if pos[0] > 0 and state[pos[0] - 1, pos[1]] != VacuumCleanerPuzzle.WALL_SYMBOL:
            actions.append((-1, 0))
        if pos[0] < state.width - 1 and state[pos[0] + 1, pos[1]] != VacuumCleanerPuzzle.WALL_SYMBOL:
            actions.append((1, 0))
        if pos[1] > 0 and state[pos[0], pos[1] - 1] != VacuumCleanerPuzzle.WALL_SYMBOL:
            actions.append((0, -1))
        if pos[1] < state.height - 1 and state[pos[0], pos[1] + 1] != VacuumCleanerPuzzle.WALL_SYMBOL:
            actions.append((0, 1))
        return actions

    # Gets a new state after applying the given action to the given state
    @staticmethod
    def apply_action(state, action):
        level = [list(r) for r in state.level]
        x, y = state.position
        level[y][x] = VacuumCleanerPuzzle.EMPTY_SYMBOL
        fx, fy = x + action[0], y + action[1]
        weight = state.weight + 1 if level[fy][fx] == VacuumCleanerPuzzle.DIRT_SYMBOL else state.weight
        level[fy][fx] = VacuumCleanerPuzzle.CLEANER_SYMBOL
        return VacuumCleanerPuzzle.State(tuple(tuple(r) for r in level), weight, (fx, fy))

    # Gets the action cost
    @staticmethod
    def get_action_cost(state, action):
        return state.weight

    # Gets the heuristic value of a state
    @staticmethod
    def get_heuristic(state):
        # TODO: Write a heuristic for VacuumCleanerPuzzle
        if VacuumCleanerPuzzle.HEURISTIC == VacuumCleanerPuzzle.HEURISTIC_NEAREST_NODE:
            nearest_distance = 1000000000000
            found = False
            for r_indx, r in enumerate(state.level):
                for c_indx, c in enumerate(r):
                    if c == VacuumCleanerPuzzle.DIRT_SYMBOL:
                        found = True
                        nearest_distance = min(
                            abs(state.position[0] - c_indx) + abs(state.position[1] - r_indx), nearest_distance
                        )
            if found:
                return nearest_distance
        elif VacuumCleanerPuzzle.HEURISTIC == VacuumCleanerPuzzle.HEURISTIC_FARTHEST_NODE:
            farthest_distance = -1
            found = False
            for r_indx, r in enumerate(state.level):
                for c_indx, c in enumerate(r):
                    if c == VacuumCleanerPuzzle.DIRT_SYMBOL:
                        found = True
                        farthest_distance = max(
                            abs(state.position[0] - c_indx) + abs(state.position[1] - r_indx), farthest_distance
                        )
            if found:
                return farthest_distance
            return 0
        elif VacuumCleanerPuzzle.HEURISTIC == VacuumCleanerPuzzle.HEURISTIC_MEAN_MANHATTEN:
            sum = 0
            found = False
            count = 0
            for r_indx, r in enumerate(state.level):
                for c_indx, c in enumerate(r):
                    if c == VacuumCleanerPuzzle.DIRT_SYMBOL:
                        found = True
                        sum += abs(state.position[0] - c_indx) + abs(state.position[1] - r_indx)
                        count += 1
            if found:
                return sum
            return 0
        elif VacuumCleanerPuzzle.HEURISTIC == VacuumCleanerPuzzle.HEURISTIC_FARTHEST_NEAREST_NODE:
            farthest_distance = -1
            sum = 0
            count = 0
            nearest_distance = 10000000000
            found = False
            for r_indx, r in enumerate(state.level):
                for c_indx, c in enumerate(r):
                    if c == VacuumCleanerPuzzle.DIRT_SYMBOL:
                        found = True
                        farthest_distance = max(
                            abs(state.position[0] - c_indx) + abs(state.position[1] - r_indx), farthest_distance
                        )
                        nearest_distance = min(
                            abs(state.position[0] - c_indx) + abs(state.position[1] - r_indx), nearest_distance
                        )
                        sum += abs(state.position[0] - c_indx) + abs(state.position[1] - r_indx)
                        count += 1

            if found:
                return sum + state.weight + count
            return 0

        return 0

    # Returns True if this is the goal state, False otherwise
    @staticmethod
    def is_goal(state):
        return not any(i == VacuumCleanerPuzzle.DIRT_SYMBOL for r in state.level for i in r)
