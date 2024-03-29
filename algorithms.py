"""
    ########## CALL TO SOLVE WITH AI ##########
    def solve_with_astar(self):
        # Create a copy of the board elements to avoid modification during search
        board_elements_copy = [atom.copy() for atom in self.board_elements]

        # Initial state representation (replace with your state class if needed)
        start_state = (board_elements_copy, self.atom_player.x, self.atom_player.y)

        def goal_test(state):
        # Check if all atoms are connected to their targets (replace with your logic)
            for atom in state[0]:
                if isinstance(atom, Atom) and atom.max_connection > 0:
                    target_x, target_y = self.find_target_position(atom.color)  # Replace with your target finding logic
                    if atom.x != target_x or atom.y != target_y:
                        return False
            return True

        astar = AStarSearch(self, manhattan_distance)
        solution = astar.a_star_search(start_state, goal_test)
        if solution is not None:
            for dx, dy in solution:
                self.move_atom_player(dx, dy)  # Assuming this method exists in your GameLevel class
            print("Level solved!")  # Or provide visual feedback of the solved state
        else:
            print("No solution found for this level.")  # Inform player about unsolvable scenario

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

################################################################# A* #################################################################
class AStarSearch:
    def __init__(self, game_level, heuristic_fn):
        self.game_level = game_level
        self.heuristic_fn = heuristic_fn

    def manhattan_distance(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def heuristic(self, node):
    # Manhattan distance between player atom and all targets
        total_distance = 0
        for atom in self.game_level.board_elements:
            if isinstance(atom, Atom) and atom.max_connection > 0:
                target_x, target_y = self.game_level.find_target_position(atom.color)  # Replace with your target finding logic
                total_distance += self.manhattan_distance(node.atom_player.x, node.atom_player.y, target_x, target_y)
        return total_distance

    def get_neighbors(self, node):
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x = node.atom_player.x + dx
            new_y = node.atom_player.y + dy
            # Check for valid move and calculate cost (consider cost for pushing atoms)
            if self.game_level.is_valid_move(node.atom_player, dx, dy):
                new_state = self.GameLevelState(self.game_level.copy_board_elements(), new_x, new_y)
                neighbors.append((new_state, 1))  # Adjust cost if needed (e.g., for pushing)
        return neighbors

    def a_star_search(self, start_state, goal_test):
        open_set = PriorityQueue()
        open_set.put((start_state.f_score, start_state))
        closed_set = set()

        while not open_set.empty():
            current_state = open_set.get()[1]
            closed_set.add(current_state)

        if goal_test(current_state):
            # Reconstruct path by backtracking from parent
            path = []
            while current_state.parent is not None:
                path.append((current_state.atom_player.x - current_state.parent.atom_player.x,
                       current_state.atom_player.y - current_state.parent.atom_player.y))
                current_state = current_state.parent
            return path[::-1]  # Reverse path for correct order

        for neighbor_state, cost in self.get_neighbors(current_state):
            if neighbor_state not in closed_set:
                tentative_g_score = current_state.g_score + cost
            if neighbor_state not in (state for state, _ in open_set):
                neighbor_state.parent = current_state
                neighbor_state.g_score = tentative_g_score
                neighbor_state.f_score = neighbor_state.g_score + self.heuristic(neighbor_state)
                open_set.put((neighbor_state.f_score, neighbor_state))
            elif tentative_g_score < neighbor_state.g_score:
                neighbor_state.parent = current_state
                neighbor_state.g_score = tentative_g_score
                neighbor_state.f_score = neighbor_state.g_score + self.heuristic(neighbor_state)
                open_set.put((neighbor_state.f_score, neighbor_state))

        return None  # No solution found
"""    