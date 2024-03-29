from draw import *
from elements import *  

class GameState:
    def __init__(self, player_position, level):
        self.board = board  # Current board configurationx
        #GameLevel.find_atom_player_position
        self.player_position = player_position  # Tuple representing player's position (x, y)
        self.level = level  # Current level

    def is_goal(self): #same as GameLevel.check_all_connections_filled
        for element in self.board:
            # Check if the element is an instance of Atom
            if isinstance(element, Atom):
                if len(element.connection) < element.max_connection:
                    return False
        # All atoms have their connections filled - GOAL STATE
        return True
    
    def get_possible_moves(self):
        moves = []
        # Check each direction: up, down, left, right
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            #verificar se a move é válida
            if GameLevel.is_valid_move(GameLevel.atom_player, dx, dy):
                #adicionar a lista de moves possiveis se for
                moves.append((dx, dy))
        return moves

    def get_neighbors(self): #child_nodes
        # Generate all possible successor states
        neighbors = []
        for move in self.get_possible_moves():
            new_state = self.make_move(move)
            if new_state:
                neighbors.append(new_state)
        return neighbors

    def make_move(self, move):
        dx, dy = move
        GameLevel.move_atom_player(self, dx, dy)


######## ALGORITHMS ########
           
def dfs(game_state):
    stack = [game_state]
    visited = set()

    while stack:
        current_state = stack.pop()
        if current_state in visited:
            continue
        visited.add(current_state)

        if current_state.is_goal():
            return current_state

        for move in current_state.get_possible_moves():
            next_state = current_state.make_move(move)
            stack.append(next_state)

    return None  # No solution found
