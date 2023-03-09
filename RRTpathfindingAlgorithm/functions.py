from variables import WINDOW_WIDTH

def get_clicked_pos(pos, rows):
        # Returns the row and column in the pygame window corresponing to the clicked position

        gap = WINDOW_WIDTH//rows
        x,y = pos
        row = y//gap
        col = x//gap
        return (row,col)

def norm2(node1,node2):
  row1,col1 = node1
  row2,col2 = node2
  # Computes pitagorean distance among two nodes
  return (((row2-row1)**2+(col2-col1)**2)**0.5)