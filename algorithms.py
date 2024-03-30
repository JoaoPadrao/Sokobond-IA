from elements import *
from boards import *

     
def dfs(game_state):
    stack = [(game_state, [])]  # Stack now stores tuples of (state, path)
    visited = set()

    while stack:
        current_state, path = stack.pop()
        if current_state in visited:
            continue
        visited.add(current_state)

        if current_state.is_goal():
            return path  # Return the path to the goal state

        """
        for move in current_state.get_possible_moves():
            next_state = current_state.make_move(move)
            stack.append(next_state) """
        
        neighbors = current_state.get_neighbors()
        for neighbor, move in neighbors:
            stack.append((neighbor, path + [move]))

    return None  # No solution found
