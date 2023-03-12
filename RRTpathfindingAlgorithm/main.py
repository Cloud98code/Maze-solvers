from maze import *
from functions import get_clicked_pos


def main():
    DIM = 50 # Maze dimension (square)
    step_size = 3 # Max distance from closest node at which new node can be place
    N_OBSTACLES = 30 # Number of obstacles in the map
    # Create a maze instance
    myMaze = Maze(DIM, DIM, N_OBSTACLES, step_size)

    started = False
    run = True

    while run:
        for event in pygame.event.get():  # Detects actions while display ON
            if event.type == pygame.QUIT: 
                run = False

            if pygame.mouse.get_pressed()[0]: # If left mouse button is pressed
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos, DIM) # Retrieve row, col in maze
                spot = myMaze.map[row][col] # Get the node in the clicked position
                # In case the start was not defined, make it
                if not myMaze.start and not spot.is_goal() and not spot.is_obstacle():
                    myMaze.set_startNode(spot)
                # In case the end was not defined, make it
                elif not myMaze.end and not spot.is_start() and not spot.is_obstacle():
                    myMaze.set_endNode(spot)

            elif pygame.mouse.get_pressed()[2]: # If right mouse button is pressed
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos, DIM) # Retrieve row, col in maze
                spot = myMaze.map[row][col] # Get the node in the clicked position
                spot_pos = spot.get_pos()
                # Reset the spot unless it is an obstacle
                if myMaze.start:
                    if norm2(spot.get_pos(), myMaze.start.get_pos()) < myMaze.start.radius:
                        myMaze.start.set_free()
                        print(myMaze.start.color)
                        print(myMaze.start.row, myMaze.start.col)
                        myMaze.map[myMaze.start.row][myMaze.start.col].draw_node()
                        myMaze.start = None
                        pygame.display.update()
                        
                if myMaze.end:
                    if norm2(spot.get_pos(), myMaze.end.get_pos()) < myMaze.end.radius:
                        myMaze.end.set_free()
                        myMaze.map[myMaze.end.row][myMaze.end.col].draw_node()
                        myMaze.end = None
                        pygame.display.update()
            
            if event.type == pygame.KEYDOWN:
                # If start and end are defined and blank space is pressed, start the A* algorithm
                if event.key == pygame.K_SPACE and not started and myMaze.start and myMaze.end:
                    myMaze.RRT_path_finder()

                if event.key == pygame.K_r and myMaze.start and myMaze.end: # If R is pressed on keyboard, reset everything
                    myMaze = Maze(DIM, DIM, N_OBSTACLES, step_size)

    pygame.quit()    

if __name__ == "__main__":
    main()