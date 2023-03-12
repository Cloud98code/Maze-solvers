from node import *
import random
import math
from functions import norm2

class Maze():
  def __init__(self, ROWS, COLUMNS,N_OBSTACLES,step_size):
    self.map = [] # Initialize map
    # Store map dimensions
    self.rows = ROWS 
    self.cols = COLUMNS
    # Number of obstacles to be initialized
    self.obstacles_number = N_OBSTACLES
    # No start and end node set yet
    self.start = None
    self.end = None
    # Max distance of the new node from its nearest node
    self.step_size = step_size
    self.goal_found = False
    # Dictionary for RRT algorithm
    self.AlgTable = {}
    self.rad = WINDOW_WIDTH // ROWS

    # Creates an empty map
    for row in range(ROWS):
      rowList = []
      for col in range(COLUMNS):
        node = Node(row, col, self.rad)
        node.set_free()
        rowList.append(node) # Append white node
      self.map.append(rowList)
    # Display empty map
    WINDOW.fill(WHITE)
    # Add obstacles to map
    self.add_obstacles()
    pygame.display.update()
   
  def set_startNode(self,node):
    # Sets the start node and draws it
    self.start = node
    node.set_start()
    node.draw_node()
    pygame.display.update()

  def set_endNode(self,node):
    # Sets the goal node and draws it
    self.end = node
    node.set_goal()
    node.draw_node()
    pygame.display.update()

  def add_obstacles(self):
    # Generates the number of obstacles decided by the user and draws them on the map

    cur_obstacles_number = 0 # Tracks number of obstacles generated
    while cur_obstacles_number < self.obstacles_number:
      # Initialize top left vertex, rectangle dimensions randomly
      row_ver, col_ver = random.randint(0,self.rows), random.randint(0,self.cols)
      WIDTH, HEIGHT = random.randint(0,int(self.cols/5)), random.randint(0,int(self.rows/5)) # Limit the dimension of the obstacles
      # Perform a check on width and height to avoid getting out of map boundaries
      WIDTH = min(WIDTH, self.cols-col_ver)
      HEIGHT = min(HEIGHT, self.rows-row_ver)
      # Set all nodes in the rectangle region to obstacles
      for row in range(row_ver, row_ver+HEIGHT):
        for col in range(col_ver, col_ver+WIDTH):
          self.map[row][col].set_obstacle()
      # Draw the obstacle on the map
      pygame.draw.rect(WINDOW, BLACK, (col_ver*self.rad,row_ver*self.rad,WIDTH*self.rad,HEIGHT*self.rad))
      pygame.display.update()
      # Update current number of obstacles
      cur_obstacles_number += 1

  def find_nearest(self,rand_node):
    # Given a randomly generated node (as a tuple with its coordinates (x,y)), finds its closest node and corresponding distance
    min_dis = (self.rows**2+self.cols**2)**0.5 # Initialized at maximum possible given grid dimension
    for node in self.AlgTable.keys():
      dis = norm2(rand_node, node)
      if dis < min_dis:
        min_dis = dis
        nearest_node = node
    return nearest_node, min_dis  

  def obstacles_on_the_way(self, rand_node, nearest_node, dis):
    # Checks if there are obstacles between two given nodes coordinates
    row_rand, col_rand = rand_node
    row_node, col_node = nearest_node

    # The distance between the new nodes is discretized in 20 points (trial and error) and each sampled point is checked to see if it is an obstacle
    for i in range(1,50):
      step = i/50
      col_new = round(col_node*step + col_rand*(1-step))
      row_new = round(row_node*step + row_rand*(1-step))
      if self.map[row_new][col_new].is_obstacle():
        return True

  def add_new_node(self, rand_node, nearest_node, dis):
    # Given the randomly generated node and its closest node and its distance, the new node to be added position is computed
    row_rand, col_rand = rand_node
    row_node, col_node = nearest_node

    # If the nodes are closer than the step size, directly use the randomly generated node
    if dis < self.step_size:
      row_new, col_new = rand_node
    # Otherwise, place the node at a distance step size from nearest node along the direction connecting the randomly generated node and its closest
    else:
      th = math.atan2(row_rand - row_node, col_rand - col_node)
      col_new = round(col_node + self.step_size*math.cos(th))
      row_new = round(row_node + self.step_size*math.sin(th))

    if self.map[row_new][col_new].is_obstacle(): # In case during the check (due to roundings) this exact spot went unnoticed
      return
  
    # If the new node is close enough to the goal node, directly use the goal node
    if norm2((row_new, col_new), self.end.get_pos()) < self.step_size:
      row_new, col_new = self.end.get_pos()
      self.goal_found = True

    # Add the newly found node to the table, draw it and connect it to its closest node
    self.AlgTable[(row_new,col_new)] = nearest_node
    self.map[row_new][col_new].set_node()
    self.map[row_new][col_new].draw_node()
    pygame.draw.line(WINDOW, RED, (self.map[row_new][col_new].x ,self.map[row_new][col_new].y) , (self.map[row_node][col_node].x ,self.map[row_node][col_node].y))
    pygame.display.update()

  def retrieve_path(self):
    current = self.end.get_pos()
    while current != self.start.get_pos():
      self.map[current[0]][current[1]].set_path()
      self.map[current[0]][current[1]].draw_node()
      pygame.draw.line(WINDOW, PURPLE, (self.map[current[0]][current[1]].x, self.map[current[0]][current[1]].y), (self.map[self.AlgTable[current][0]][self.AlgTable[current][1]].x, self.map[self.AlgTable[current][0]][self.AlgTable[current][1]].y))
      current = self.AlgTable[current]
      pygame.display.update()

  def RRT_path_finder(self):
    # Implements RRT algorithm
    # Only active node at the start is the start node
    self.AlgTable[self.start.get_pos()] = None

    while not self.goal_found:
      # Initialize a random node
      row_rand, col_rand = random.randint(0,self.rows-1), random.randint(0,self.cols-1)
      # Verify it is not an obstacle
      if self.map[row_rand][col_rand].is_obstacle() or (row_rand, col_rand) in self.AlgTable.keys():
        continue
      # Find its nearest node
      nearest_node, distance = self.find_nearest((row_rand,col_rand))
      # Verify there are no obstacles on the way
      if self.obstacles_on_the_way((row_rand,col_rand), nearest_node, distance):
        continue
      # Add new node to the tree
      self.add_new_node((row_rand,col_rand), nearest_node, distance)
      # When goal is found, retrieve entire path
      if self.goal_found:
        self.retrieve_path()