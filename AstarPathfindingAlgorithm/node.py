from variables import *
import pygame

WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_WIDTH))
pygame.display.set_caption("Maze solver")

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
    
    def draw(self):
      # Draws the node in the display
      pygame.draw.rect(WINDOW, self.color, (self.x,self.y,self.width, self.width))