import pygame 
from obstacle_field import *

width_win = 1000
win = pygame.display.set_mode((width_win,width_win))
pygame.display.set_caption("Title")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
TURQUISE = (64,224,208)
ORANGE = (255,165,0)
GREY = (150,150,150)

class Nodes:
    def __init__(self,row,col,total_nodes,width_node):
        self.row = row
        self.col = col
        self.x = row * width_node
        self.y = col * width_node
        self.color = WHITE
        self.neighbours = []
        self.width = width_node
        self.total_nodes = total_nodes

    def get_pos(self):
        return self.row,self.col
    
    def is_explored(self):
        return self.color == RED
    
    def is_obstacle(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == BLUE

    def is_goal(self):
        return self.color == GREEN

    def make_explored(self):
        self.color = RED
    
    def make_obstacle(self):
        self.color = BLACK

    def start_node(self):
        self.color = BLUE
    
    def goal_node(self):
        self.color = GREEN

    def reset(self):
        self.color = WHITE

    def make_path(self):
        self.color = TURQUISE

    def draw(self,win):
        pygame.draw.rect(win,color=self.color,rect=(self.x,self.y, self.width, self.width))

    def add_neighbors(self,grid):
        pass


def grid_converter(grid):
    row_grid, col_grid = grid.shape
    Grid = np.empty((row_grid,col_grid),dtype= Nodes)
    for i in range(row_grid):
        for j in range(col_grid):
            node = Nodes(i,j,row_grid*col_grid, width_win/row_grid)
            if grid[i][j] == 1:
                node.make_obstacle()
            Grid[i][j] = node
    
    return Grid

def draw_grid(win, grid, width_win):
    row_grid, col_grid = grid.shape
    for i in range(row_grid):
        for j in range(col_grid):
            node = grid[i][j]
            if node is not None:
                node.draw(win)
    for i in range(int(128)):
        pygame.draw.line(win,GREY,(0,i*width_win/128),(width_win,i*width_win/128))
        pygame.draw.line(win,GREY,(i*width_win/128,0),(i*width_win/128,width_win))
    pygame.display.update()


grid = obstacle_field_generator()
Grid = grid_converter(grid)
while(1):
    draw_grid(win,Grid,width_win)



