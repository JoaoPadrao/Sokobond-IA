from elements import *
from boards import *
from memory_profiler import profile
import heapq
from collections import deque

class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
        

@profile   
def dfs(current_state):
    current_node = TreeNode(current_state)
    stack = [(current_node, [])] 
    visited = set()
    
    while stack:
        print("Length of stack: ", len(stack))
        current_node, path = stack.pop()
        current_state = current_node.state  # Get the current state from the current node

        if current_state.is_goal():
            current_state.game_level.show_message("Level complete! Press Enter to choose the next level.")
            return path
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        
        neighbors = current_state.get_neighbors()
        print("Length of neighbors: ", len(neighbors))
        for neighbor_state, move in neighbors:
            if neighbor_state.is_goal():
                path = path + [move]
                neighbor_state.game_level.show_message("Level complete! Press Enter to choose the next level.")                
                return path
            visited_flag = False
            for visited_node in visited:
                if visited_node.state == neighbor_state:
                    visited_flag = True
            if not visited_flag:
                neighbor_node = TreeNode(neighbor_state)
                current_node.add_child(neighbor_node)
                stack.append((neighbor_node, path + [move]))
    return None

@profile
def bfs(current_state):
    current_node = TreeNode(current_state)
    queue = [(current_node, [])] 
    visited = set()
    
    while queue:
        print("Length of queue: ", len(queue))
        current_node, path = queue.pop(0)
        current_state = current_node.state  # Get the current state from the current node

        if current_state.is_goal():
            current_state.game_level.show_message("Level complete! Press Enter to choose the next level.")
            return path
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        
        neighbors = current_state.get_neighbors()
        print("Length of neighbors: ", len(neighbors))
        for neighbor_state, move in neighbors:
            if neighbor_state.is_goal():
                path = path + [move]
                neighbor_state.game_level.show_message("Level complete! Press Enter to choose the next level.")                
                return path
            visited_flag = False
            for visited_node in visited:
                if visited_node.state == neighbor_state:
                    visited_flag = True
            if not visited_flag:
                neighbor_node = TreeNode(neighbor_state)
                current_node.add_child(neighbor_node)
                queue.append((neighbor_node, path + [move]))
    return None

def iterative_deepening(current_state):
    depth = 0
    while True:
        result = depth_limited_dfs(current_state, depth)
        if result is not None:
            return result
        depth += 1


def depth_limited_dfs(current_state, depth):
    current_node = TreeNode(current_state)
    stack = [(current_node, [], 0)] 
    visited = set()
    
    while stack:
        print("Length of stack: ", len(stack))
        current_node, path, current_depth = stack.pop()
        current_state = current_node.state  # Get the current state from the current node

        if current_state.is_goal():
            current_state.game_level.show_message("Level complete! Press Enter to choose the next level.")
            return path
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        
        neighbors = current_state.get_neighbors()
        print("Length of neighbors: ", len(neighbors))
        for neighbor_state, move in neighbors:
            if neighbor_state.is_goal():
                path = path + [move]
                neighbor_state.game_level.show_message("Level complete! Press Enter to choose the next level.")                
                return [path, current_depth]
            visited_flag = False
            for visited_node in visited:
                if visited_node.state == neighbor_state:
                    visited_flag = True
            if not visited_flag and current_depth < depth:
                neighbor_node = TreeNode(neighbor_state)
                current_node.add_child(neighbor_node)
                stack.append((neighbor_node, path + [move], current_depth + 1))
    return None



def greedy_search(initial_state):
    frontier = [(initial_state, 0, [])]  # Initialize frontier with initial state and cost
    explored = set()  # Initialize an empty set to keep track of explored states
    
    while frontier:
        state, heur, path = frontier.pop(0)  # Get the state with the lowest heuristic value
        print("heur: ", heur)
        if state.is_goal():  # Check if the current state is the goal state
            return state  # Return the goal state
        
        explored.add(state)  # Add the current state to the explored set
        
        # Get the neighbors of the current state
        neighbors = state.get_neighbors()
        
        # Add unexplored neighbors to the frontier
        for neighbor, move in neighbors:
            if neighbor.is_goal():
                neighbor.game_level.show_message("Level complete! Press Enter to choose the next level.")                
                path = path + [move]
                return path
        
            visited_flag = False
            for visited_state in explored:
                if visited_state == neighbor:
                    visited_flag = True
            if not visited_flag:
                frontier.append((neighbor, heuristic(neighbor),path + [move]))  # Add neighbor and its heuristic value to frontier

        frontier.sort(key=lambda x: x[1], reverse=True)

    return None  # If no solution is found, return None

def heuristic(state):
    # Get the player's position
    player_x, player_y = state.game_level.atom_player.x, state.game_level.atom_player.y
    # Get the goal position
    goal_x, goal_y = state.game_level.find_atom_goal_position()
    
    # Calculate the Manhattan distance between player and goal
    manhattan_distance = abs(player_x - goal_x) + abs(player_y - goal_y)

    # Adjust the distance to account for walls
    for y in range(min(player_y, goal_y), max(player_y, goal_y) + 1):
        for x in range(min(player_x, goal_x), max(player_x, goal_x) + 1):
            if state.game_level.level_data[y][x] == '#':  # Check if there's a wall at this position
                manhattan_distance += 1  # Increase the distance by 1 for each wall encountered

    return manhattan_distance


def a_star_search(initial_state):
    frontier = [(initial_state, 0, [])]  # Initialize frontier with initial state and cost
    explored = set()  # Initialize an empty set to keep track of explored states
    
    while frontier:
        state, cost, path = frontier.pop(0)  # Get the state with the lowest cost
        print("cost: ", cost)
        if state.is_goal():  # Check if the current state is the goal state
            return state  # Return the goal state
        
        explored.add(state)  # Add the current state to the explored set
        
        # Get the neighbors of the current state
        neighbors = state.get_neighbors()
        
        # Add unexplored neighbors to the frontier
        for neighbor, move in neighbors:
            if neighbor.is_goal():
                neighbor.game_level.show_message("Level complete! Press Enter to choose the next level.")                
                path = path + [move]
                return path
        
            visited_flag = False
            for visited_state in explored:
                if visited_state == neighbor:
                    visited_flag = True
            if not visited_flag:
                frontier.append((neighbor, cost + 1, path + [move]))  

        frontier.sort(key=lambda x: x[1] + heuristic(x[0]))

    return None  