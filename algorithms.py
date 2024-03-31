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
                return path
            visited_flag = False
            for visited_node in visited:
                if visited_node.state == neighbor_state:
                    visited_flag = True
            if not visited_flag and current_depth < depth:
                neighbor_node = TreeNode(neighbor_state)
                current_node.add_child(neighbor_node)
                stack.append((neighbor_node, path + [move], current_depth + 1))
    return None

