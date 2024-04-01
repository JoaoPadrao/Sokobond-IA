from elements import *
from boards import *

class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
        

# Function to perform depth-first search
def dfs(current_state):
    current_node = TreeNode(current_state)
    stack = [(current_node, [])]  # Initialize stack with initial state and path
    visited = set()
    
    while stack:
        current_node, path = stack.pop()
        current_state = current_node.state  # Get the current state from the current node

        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        neighbors = current_state.get_neighbors()

        for neighbor_state, move in neighbors:
            if neighbor_state.is_goal(): # Check if the neighbor state is the goal state
                path = path + [move]
                neighbor_state.game_level.show_message("Level complete! Press Enter to choose the next level.")                
                return path
            visited_flag = False

            for visited_node in visited: # Check if the neighbor state has been visited before
                if visited_node.state == neighbor_state:
                    visited_flag = True

            if not visited_flag:
                neighbor_node = TreeNode(neighbor_state)
                current_node.add_child(neighbor_node)
                stack.append((neighbor_node, path + [move]))
    return None

# Function to perform breadth-first search
def bfs(current_state):
    current_node = TreeNode(current_state)
    queue = [(current_node, [])] # Initialize queue with initial state and path
    visited = set()
    
    while queue:
        current_node, path = queue.pop(0)
        current_state = current_node.state  # Get the current state from the current node
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        neighbors = current_state.get_neighbors()

        for neighbor_state, move in neighbors:
            if neighbor_state.is_goal(): # Check if the neighbor state is the goal state
                path = path + [move]
                neighbor_state.game_level.show_message("Level complete! Press Enter to choose the next level.")                
                return path
            visited_flag = False

            for visited_node in visited: # Check if the neighbor state has been visited before
                if visited_node.state == neighbor_state:
                    visited_flag = True

            if not visited_flag:
                neighbor_node = TreeNode(neighbor_state)
                current_node.add_child(neighbor_node)
                queue.append((neighbor_node, path + [move]))
    return None

# Function to perform depth-limited search
def iterative_deepening(current_state):
    depth = 0 # Initialize depth to 0
    while True:
        result = depth_limited_dfs(current_state, depth) # Perform depth-limited search with the current depth
        if result is not None: # If a solution is found, return the path
            return result
        depth += 1

def depth_limited_dfs(current_state, depth):
    current_node = TreeNode(current_state)
    stack = [(current_node, [], 0)] # Initialize stack with initial state, path, and depth
    visited = set()
    
    while stack:
        current_node, path, current_depth = stack.pop()
        current_state = current_node.state  # Get the current state from the current node

        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        
        neighbors = current_state.get_neighbors()
        for neighbor_state, move in neighbors:
           
            if neighbor_state.is_goal(): # Check if the neighbor state is the goal state
                path = path + [move]
                neighbor_state.game_level.show_message("Level complete! Press Enter to choose the next level.")                
                return [path, current_depth]
            visited_flag = False

            for visited_node in visited: # Check if the neighbor state has been visited before
                if visited_node.state == neighbor_state:
                    visited_flag = True

            if not visited_flag and current_depth < depth: # Check if the neighbor state has been visited before and if the current depth is less than the depth limit
                neighbor_node = TreeNode(neighbor_state)
                current_node.add_child(neighbor_node)
                stack.append((neighbor_node, path + [move], current_depth + 1))
    return None


# Function to perform greedy search using the Manhattan distance heuristic
def greedy_search(initial_state):
    frontier = [(initial_state, 0, [])]  # Initialize frontier with initial state, heuristic value, and path
    visited = set()  
    
    while frontier:
        state, heur, path = frontier.pop(0)  # Get the state with the lowest heuristic value
        
        visited.add(state) 
        
        # Get the neighbors of the current state
        neighbors = state.get_neighbors()
        
        # Add unexplored neighbors to the frontier
        for neighbor, move in neighbors:
            if neighbor.is_goal():
                neighbor.game_level.show_message("Level complete! Press Enter to choose the next level.")                
                path = path + [move]
                return path
        
            visited_flag = False
            for visited_state in visited:
                if visited_state == neighbor:
                    visited_flag = True
            if not visited_flag:
                frontier.append((neighbor, heuristic(neighbor),path + [move]))  # Add neighbor to the frontier with the heuristic value and path

        frontier.sort(key=lambda x: x[1]) # Sort the frontier based on the heuristic value

    return None  

# Heuristic function for the Manhattan distance
def heuristic(state):

    player_x, player_y = state.game_level.atom_player.x, state.game_level.atom_player.y
    goal_x, goal_y = state.game_level.find_atom_goal_position()
    
    # Calculate the Manhattan distance between player and goal
    manhattan_distance = abs(player_x - goal_x) + abs(player_y - goal_y)

    # Adjust the distance to account for walls
    for y in range(min(player_y, goal_y), max(player_y, goal_y) + 1):
        for x in range(min(player_x, goal_x), max(player_x, goal_x) + 1):
            if state.game_level.level_data[y][x] == '#':  # Check if there's a wall at this position
                manhattan_distance += 1  # Increase the distance by 1 for each wall encountered

    return manhattan_distance


# Function to perform A* search using the Manhattan distance heuristic
def a_star_search(initial_state):
    frontier = [(initial_state, 0, [])]  # Initialize frontier with initial state, heuristic value, and path
    visited = set()  
    
    while frontier:
        state, cost, path = frontier.pop(0)  # Get the state with the lowest cost

        visited.add(state)  
        
        neighbors = state.get_neighbors()
        
        # Add unexplored neighbors to the frontier
        for neighbor, move in neighbors:

            if neighbor.is_goal():
                neighbor.game_level.show_message("Level complete! Press Enter to choose the next level.")                
                path = path + [move]
                return path
        
            visited_flag = False
            for visited_state in visited:
                if visited_state == neighbor:
                    visited_flag = True
            if not visited_flag:
                frontier.append((neighbor, cost + 1, path + [move]))   # Add neighbor to the frontier with the cost and path

        frontier.sort(key=lambda x: x[1] + heuristic(x[0])) # Sort the frontier based on the cost and heuristic value

    return None  