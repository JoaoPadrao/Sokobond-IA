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

        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        if current_state.is_goal():
            print("found goal")
            return path
        
        neighbors = current_state.get_neighbors()
        print("Length of neighbors: ", len(neighbors))
        for neighbor_state, move in neighbors:
            visited_flag = False
            for visited_node in visited:
                if visited_node.state == neighbor_state:
                    visited_flag = True
            if not visited_flag:
                neighbor_node = TreeNode(neighbor_state)
                current_node.add_child(neighbor_node)
                stack.append((neighbor_node, path + [move]))
    return None