from node import *
import numpy as np
import queue

class Maze():
    def __init__(self, ROWS,COLUMNS,SPARSITY):
    # Creates a Maze of ROWSxCOLUMNS. Sparsity is an index between 0 and 1 to measure the amount of obstacles (the lower, the lesser)
        
        self.map = [] # Will contain the maze
        # Store maze parameters
        self.rows = ROWS
        self.cols = COLUMNS
        self.sparsity = SPARSITY
        # At initialization no start/finish defined
        self.start = None
        self.end = None

        # Cubicle dimension of a spot, assuming ROWS = COLUMNS (square maze)
        gap = WINDOW_WIDTH // ROWS
        
        for row in range(ROWS):
            rowList = []
            for col in range(COLUMNS):
                # If random number is 0, generate free position, if it is 1, generate an obstacle
                if not np.random.choice([0, 1], 1, p=[SPARSITY, 1-SPARSITY]):
                  # Create a free node istance and append it to the maze 
                  node = Node(row, col, gap)
                  node.set_free()
                  rowList.append(node) # Append white node
                else:
                  # Create an obstacle node istance and append it to the maze
                  node = Node(row, col, gap)
                  node.set_obstacle()
                  rowList.append(node) # Append black node
            self.map.append(rowList)
        

    def set_startNode(self, node):
        self.start = node
        # Change the node into a start node
        node.set_start()

    def set_endNode(self, node):
        self.end = node
        # Change the node into a start node
        node.set_goal()

    def getNeighbors(self, node):
        # Given a certain node, find its free neighbors
        # ASSUMPTION: no diagonal moves allowed

        # Check previous row
        if node.row-1 >= 0 and not self.map[node.row-1][node.col].is_obstacle():
            node.neighbors.append(self.map[node.row-1][node.col])

        # Check successive row
        if node.row+1 < self.rows and not self.map[node.row+1][node.col].is_obstacle():
            node.neighbors.append(self.map[node.row+1][node.col]) 

        # Check previous column
        if node.col-1 >= 0 and not self.map[node.row][node.col-1].is_obstacle():
            node.neighbors.append(self.map[node.row][node.col-1]) 

        # Check successive column
        if node.col+1 < self.cols and not self.map[node.row][node.col+1].is_obstacle():
            node.neighbors.append(self.map[node.row][node.col+1])  

    def draw_maze_grid(self):
        # Draws the grid in which the nodes are displayed

        gap = WINDOW_WIDTH // self.rows
        for i in range(self.rows):
            # Draw horizontal line for each row
            pygame.draw.line(WINDOW, GREY, (0,i*gap),(WINDOW_WIDTH, i*gap))
            for j in range(self.rows):
                # Draw vertical line for each column
                pygame.draw.line(WINDOW, GREY, (j*gap, 0), (j*gap, WINDOW_WIDTH))

    def draw_maze(self):
        # Draws the nodes and the grid of the maze

        # At beginning of every frame, we paint over the maze and re-draw from scratch
        WINDOW.fill(WHITE)
        # Draw each node
        for row in self.map:
            for spot in row:
                spot.draw()
        # Draw the grid
        self.draw_maze_grid()
        pygame.display.update()
    
    def retrieve_path(self, parent_nodes):
        current = self.end
        current.set_path()

        while current.get_pos() != self.start.get_pos():
            current = parent_nodes[current.get_pos()]
            current.set_path()
            self.draw_maze()

    
    def Depth_First_search(self):
        # Initialize set to contain visited nodes
        visited_nodes = set()
        self.goalFound = False

        def recursive_dfs(current_node):
            # Skip node if already visited
            if current_node in visited_nodes:
                return True
            # Retrieve path if goal is found
            if current_node.get_pos() == self.end.get_pos():
                self.goalFound = True
                return True
            # Stop exploring if goal has been found
            if self.goalFound:
                return True
            # If none of above, add current node to visited nodes
            visited_nodes.add(current_node)
            current_node.set_visited()
            # Retrieve nodes neighbors
            self.getNeighbors(current_node)
            # Recursively check neighbors
            for neighbor in current_node.neighbors:
                self.draw_maze()
                recursive_dfs(neighbor)

        recursive_dfs(self.start)
        return False

    def Breadth_first_search(self):
        q = queue.Queue()
        q.put(self.start)
        visited = {self.start}
        parent_nodes = {self.start.get_pos(): None}

        while not q.empty():
            current_node = q.get()
            if not current_node.is_start():
                current_node.set_visited()
            if current_node.get_pos() == self.end.get_pos():
                self.retrieve_path(parent_nodes)
                return True
            self.getNeighbors(current_node)
            for neighbor in current_node.neighbors:
                if neighbor not in visited:
                    q.put(neighbor)
                    parent_nodes[neighbor.get_pos()] = current_node
                    visited.add(neighbor)
                    neighbor.set_to_visit()
            self.draw_maze()
        return False