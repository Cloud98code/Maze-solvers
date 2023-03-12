import pygame
from variables import *

WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_WIDTH))
pygame.display.set_caption("Maze solver")

class Node():
    # White nodes are free
    # Black nodes are obstacles
    # Blue node is start
    # Orange node is goal
    # Red nodes are valid nodes
    # Purple nodes are part of final path

    def __init__(self, row, col, radius):
        self.row = row
        self.col = col
        # Variables to draw the circles inside the display
        self.radius = radius//2
        self.x = col*radius
        self.y = row*radius
        # Node color not defined
        self.color = None
    
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

    def set_node(self):
        self.color = RED

    def set_start(self):
        self.color = BLUE

    def set_goal(self):
        self.color = ORANGE

    def set_path(self):
        self.color = PURPLE
    
    def draw_node(self):
        # Draws the node in the display
        pygame.draw.circle(WINDOW, self.color, (self.x,self.y), self.radius)
        pygame.display.update()