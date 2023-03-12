from maze import *
from functions import get_clicked_pos

def main():
    DIM = 50 # Maze dimension (square)
    SPARSITY = 0.8 # Index of obstacles density
    # Create a maze instance
    myMaze = Maze(DIM, DIM, SPARSITY)

    # Variables to check maze solver status
    run = True
    started = False

    while run:
        myMaze.draw_maze()
        for event in pygame.event.get():  # Detects actions while display ON
            if event.type == pygame.QUIT: 
                run = False

            if pygame.mouse.get_pressed()[0]: # If left mouse button is pressed
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos, DIM) # Retrieve row, col in maze
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
                    myMaze = Maze(DIM, DIM, SPARSITY)



    pygame.quit()

if __name__ == '__main__':
    main()