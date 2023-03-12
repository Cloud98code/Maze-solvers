from node import *
import numpy as np
from queue import PriorityQueue


class Maze():
    def __init__(self, ROWS,COLUMNS,SPARSITY):
    # Creates a Maze of ROWSxCOLUMNS. Sparsity is an index between 0 and 1 to measure the amount of obstacles (the lower, the lesser)
        
        self.map = [] # Will contain the maze
        # Store maze parameters
        self.rows = ROWS
        self.cols = COLUMNS
        self.sparsity = SPARSITY
        # Dictionary initialization, will be used in A*
        self.AlgorithmTable = {}
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
                # For each entry create a dictionary whose key is the node position, value a list [g_score, f_score, previous_node]
                self.AlgorithmTable[(row,col)] = [float("inf"), float("inf"), None]
            self.map.append(rowList)
        

    def set_startNode(self, node):
        self.start = node
        # Change the node into a start node
        node.set_start()

    def set_endNode(self, node):
        self.end = node
        # Change the node into a start node
        node.set_goal()
        # Once end node is defined, it is possible to update f_score of start node
        self.AlgorithmTable[self.start.get_pos()] = [0, self.Manhattan(self.start), None]

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

    def Manhattan(self, node):
      # Computes the Manhattan distance of a given node with respect to the goal node
        return abs(node.row - self.end.row) + abs(node.col - self.end.col)

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
    
    def retrieve_path(self):
        current = self.end
        current.set_path()

        while current.get_pos() != self.start.get_pos():
            current = self.AlgorithmTable[current.get_pos()][2]
            current.set_path()
            self.draw_maze()

    def A_star_pathFinder(self):
        # Variable to track the order of elements in priority queue
        # In case two elements have same f_score, the priority will go to node inserted earlier
        count = 0

        # Initialize priority queue of positions to visit adding 
        q = PriorityQueue()
        q.put((self.AlgorithmTable[self.start.get_pos()][1], count, self.start))
        # Set to check whether a node has already been visited
        q_hash = {self.start}

        while not q.empty():
            # Allow user to quit algorithm
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            current_pos = q.get()[2] # Retrieve the position of the active node
            q_hash.remove(current_pos)
            
            # If active node is the end node, retrieve the path and terminate the algorithm
            if current_pos.get_pos() == self.end.get_pos():
                self.retrieve_path()
                return True
            # Retrieve available neighbors of active node
            self.getNeighbors(current_pos)
        
            # If current node is not the end node, check his neighbors
            for neighbor in current_pos.neighbors:
                # The g_score for the current neighbor is the g_score of the active node + 1
                new_g_score = self.AlgorithmTable[current_pos.get_pos()][0] + 1

                if new_g_score < self.AlgorithmTable[neighbor.get_pos()][0]:
                    # If current path is shorter than what already saved, update g_score, f_score, previous step
                    self.AlgorithmTable[neighbor.get_pos()][0] = new_g_score #update g_score
                    self.AlgorithmTable[neighbor.get_pos()][1] = new_g_score + self.Manhattan(neighbor) # update f_score
                    self.AlgorithmTable[neighbor.get_pos()][2] = current_pos # update previous step
                    # In case the neighbor has not been visited, insert it in the queue
                    if neighbor not in q_hash:
                        # Increase the queue counter
                        count += 1
                        # Add neighbor to queue
                        q.put((self.AlgorithmTable[neighbor.get_pos()][1], count, neighbor))
                        q_hash.add(neighbor)
                        neighbor.set_to_visit() # Change its color so it can be displayed

            self.draw_maze()
            # Update the current node to visited
            if current_pos.get_pos() != self.start.get_pos():
                current_pos.set_visited()        
                # Update the maze in the display
                
        return False