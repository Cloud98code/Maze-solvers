from variables import WINDOW_WIDTH

def get_clicked_pos(pos, rows):
        # Returns the row and column in the pygame window corresponing to the clicked position

        gap = WINDOW_WIDTH//rows
        y,x = pos
        row = y//gap
        col = x//gap
        return (row,col)