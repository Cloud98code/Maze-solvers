from queue import PriorityQueue
import numpy as np
import pygame

# Set up the display
WINDOW_WIDTH = 800 # Square dimension
WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_WIDTH))
pygame.display.set_caption("Maze solver")


# Colors for path finder visualization
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)

class Node():
    # White nodes are free
    # Black nodes are obstacles
    # Blue node is start
    # Orange node is finish
    # Red nodes have been visited
    # Green nodes are in the queue
    # Purple nodes are part of final path


    def __init__(self, row, col, cube_width):
        self.row = row
        self.col = col
        # Variables to draw the cube inside the display
        self.width = cube_width
        self.y = col*cube_width
        self.x = row*cube_width 
        # Node color not defined
        self.color = None
        # Stores accessible neighbors
        self.neighbors = []
    
    def get_pos(self):
      # Outputs coordinates as a tuple

      return (self.row,self.col)

    def is_free(self):
        return self.color == WHITE
    
    def is_obstacle(self):
        return self.color == BLACK

    def is_start(self):
      return self.color == BLUE

    def is_goal(self):
        return self.color == ORANGE

    def set_free(self):
        self.color = WHITE
    
    def set_obstacle(self):
        self.color = BLACK

    def set_visited(self):
        self.color = RED
        
    def set_to_visit(self):
        self.color = GREEN

    def set_start(self):
        self.color = BLUE

    def set_goal(self):
        self.color = ORANGE

    def set_path(self):
        self.color = PURPLE
    
    def draw(self, WIN):
      # Draws the node in the display
      pygame.draw.rect(WIN, self.color, (self.x,self.y,self.width, self.width))

class Maze():
    def __init__(self, ROWS,COLUMNS,SPARSITY, WIN_WIDTH):
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
        gap = WIN_WIDTH // ROWS
        
        for row in range(ROWS):
            rowList = []
            for col in range(COLUMNS):
                # If random number is 0, generate free position, if it is 1, generate an obstacle
                if  np.random.choice([0, 1], 1, p=[SPARSITY, 1-SPARSITY]):
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

    def draw_maze_grid(self, WIN, WIN_WIDTH):
        # Draws the grid in which the nodes are displayed

        gap = WIN_WIDTH // self.rows
        for i in range(self.rows):
            # Draw horizontal line for each row
            pygame.draw.line(WIN, GREY, (0,i*gap),(WIN_WIDTH, i*gap))
            for j in range(self.rows):
                # Draw vertical line for each column
                pygame.draw.line(WIN, GREY, (j*gap, 0), (j*gap, WIN_WIDTH))

    def draw_maze(self, WIN, WIN_WIDTH):
        # Draws the nodes and the grid of the maze

        # At beginning of every frame, we paint over the maze and re-draw from scratch
        WIN.fill(WHITE)
        # Draw each node
        for row in self.map:
            for spot in row:
                spot.draw(WIN)
        # Draw the grid
        self.draw_maze_grid(WIN, WIN_WIDTH)
        pygame.display.update()
    
    def retrieve_path(self):
        current = self.end
        current_pos = self.end.get_pos()
        
        while current_pos != self.start.get_pos():
            current = self.AlgorithmTable[current_pos][2]
            current_pos = self.AlgorithmTable[current_pos][2].get_pos()
            current.set_path()
            self.draw_maze(WINDOW, WINDOW_WIDTH)


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

            self.draw_maze(WINDOW, WINDOW_WIDTH)
            # Update the current node to visited
            if current_pos.get_pos() != self.start.get_pos():
                current_pos.set_visited()        
                # Update the maze in the display
                
        return False
    
def get_clicked_pos(pos, WIN_WIDTH, rows):
        # Returns the row and column in the pygame window corresponing to the clicked position

        gap = WIN_WIDTH//rows
        y,x = pos
        row = y//gap
        col = x//gap
        return (row,col)

def main():
    DIM = 50 # Maze dimension (square)
    SPARSITY = 0.2 # Index of obstacles density
    # Create a maze instance
    myMaze = Maze(DIM, DIM, SPARSITY, WINDOW_WIDTH)

    # Variables to check maze solver status
    run = True
    started = False

    while run:
        myMaze.draw_maze(WINDOW, WINDOW_WIDTH)
        for event in pygame.event.get():  # Detects actions while display ON
            if event.type == pygame.QUIT: 
                run = False

            if pygame.mouse.get_pressed()[0]: # If left mouse button is pressed
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos, WINDOW_WIDTH, DIM) # Retrieve row, col in maze
                spot = myMaze.map[row][col] # Get the node in the clicked position
                # In case the start was not defined, make it
                if not myMaze.start and not spot.is_obstacle() and not spot.is_goal():
                    myMaze.set_startNode(spot)
                
                # In case the end was not defined, make it
                elif not myMaze.end and not spot.is_obstacle() and not spot.is_start():
                    myMaze.set_endNode(spot)

            elif pygame.mouse.get_pressed()[2]: # If right mouse button is pressed
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos, WINDOW_WIDTH, DIM) # Retrieve row, col in maze
                spot = myMaze.map[row][col] # Get the node in the clicked position
                
                # Reset the spot unless it is an obstacle
                if spot.is_start():
                    myMaze.start = None
                    spot.set_free()

                elif spot.is_goal():
                    myMaze.end = None
                    spot.set_free()
            
            if event.type == pygame.KEYDOWN:
                # If start and end are defined and blank space is pressed, start the A* algorithm
                if event.key == pygame.K_SPACE and not started and myMaze.start and myMaze.end:
                    myMaze.A_star_pathFinder()

                if event.key == pygame.K_r and myMaze.start and myMaze.end: # If R is pressed on keyboard, reset everything
                    myMaze = Maze(DIM, DIM, SPARSITY, WINDOW_WIDTH)



    pygame.quit()

if __name__ == '__main__':
    main()