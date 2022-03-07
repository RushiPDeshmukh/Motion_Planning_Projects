import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import pygame 

width_win = 640

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
        return self.color == TURQUISE
    
    def is_obstacle(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == BLUE

    def is_goal(self):
        return self.color == GREEN

    def make_explored(self):
        if not self.color == GREEN:
            self.color = TURQUISE
    
    def make_obstacle(self):
        self.color = BLACK

    def start_node(self):
        self.color = BLUE
    
    def goal_node(self):
        self.color = GREEN

    def reset(self):
        self.color = WHITE

    def make_path(self):
        self.color = ORANGE

    def draw(self,win):
        pygame.draw.rect(win,color=self.color,rect=(self.x,self.y, self.width, self.width))

    def add_neighbours(self,grid):
        self.neighbours = []
        x,y = self.get_pos()
        #Down
        if (x+1)<= 127 and not grid[x+1][y].is_obstacle():
            self.neighbours.append((x+1,y,0))
        #Right
        if (y+1) <= 127 and not grid[x][y+1].is_obstacle():
            self.neighbours.append((x,y+1,0))
        #Up
        if (x-1) >= 0 and not grid[x-1][y].is_obstacle():
            self.neighbours.append((x-1,y,10))
        #Left
        if y-1>= 0 and not grid[x][y-1].is_obstacle():
            self.neighbours.append((x,y-1,10))
        

row_grid = 128
col_grid = 128

obstacle1 = [1,1,1,1]
obstacle2 = [[1,0,0],[1,1,1]]
obstacle3 = [[0,0,1],[1,1,1]]
obstacle4 = [[1,1],[1,1]]
obstacle5 = [[0,1,1],[1,1,0]]
obstacle6 = [[1,1,0],[0,1,1]]
obstacle7 = [[0,1,0],[1,1,1]]
obstacles = {'1':obstacle1,'2':obstacle2,'3':obstacle3,'4':obstacle4,'5':obstacle5,'6':obstacle6,'7':obstacle7}

def init_grid():
    Empty_Grid = np.empty((row_grid,col_grid),dtype= Nodes)
    for i in range(128):
        for j in range(128):
            Empty_Grid[i][j] = Nodes(row= i,col = j,total_nodes = 128*128,width_node = width_win/128)
    return Empty_Grid


def obstacle_field_generator(grid,win,obstacles= obstacles,coverage=10, animate = False):
    """AI is creating summary for obstacle_field_generator

    Args:
        grid ([numpy array of 128x128]): This arg contains the grid before it is populated with given obstacles
        obstacles ([Dictionary]): This arg contains different obstacle shapes that we want to deploy in the grid
        coverage (int, optional): This arg tell the total coverage of grid that needs to be populated with obstacles. Defaults to 10.

    Returns:
        [numpy array of 128x128]: grid populated with obstacles with given coverage
    """
    curr_coverage = 0
    coverage_counter = 0
    occupied_field = []

    #Loop till grid coverage is below the desired coverage
    while(int(curr_coverage) < coverage):
        #Randomly choose location on grid to put a obstacle there
        random_x = random.randint(0,127)
        random_y = random.randint(0,127)
        #Randomly choose a obstacle and its orientation
        random_obstacle = str(random.randint(1,8))
        random_orientation = random.randint(1,4)
        obstacle = np.array(obstacles[random_obstacle])
        if len(obstacle.shape) == 1:
            #Change the orientation of obstacle
            obstacle = obstacle.T if random_orientation%2 == 0 else obstacle
        else:
            #Change the orientation of obstacle
            obstacle = np.rot90(obstacle,random_orientation,(0,1))

        shape_obstacle = obstacle.shape
        #Check if the choosen obstacle can fit the grid
        if len(shape_obstacle) == 1:
            flag1 = True
            flag2 = (random_y+shape_obstacle[0]) <=128
        else:
            flag1 = (random_x+shape_obstacle[0]) <=128
            flag2 = (random_y+shape_obstacle[1]) <=128
        #Check if the randomly choosen location is empty
        if (not (random_x,random_y) in occupied_field) and flag1 and flag2:
            #Add the obstacle to the grid
            if len(shape_obstacle) == 1:
                for y in range(shape_obstacle[0]):
                    if obstacle[y]==1:
                        grid[random_x][random_y+y].make_obstacle()
                        coverage_counter += 1
            else:
                for x in range(shape_obstacle[0]):
                    for y in range(shape_obstacle[1]):
                        if obstacle[x][y]==1:
                            grid[random_x + x][random_y + y].make_obstacle()
                            coverage_counter += 1
            #update the current coverage variable
            curr_coverage = (coverage_counter/(128*128))*100
            if animate:
                draw_grid(win,grid)
                pygame.time.delay(5)
            
    grid[0][0].start_node()
    grid[127][127].goal_node()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            grid[i][j].add_neighbours(grid)
    return grid

    

def draw_grid(win, grid):
    row_grid, col_grid = grid.shape
    win.fill(WHITE)
    for i in range(row_grid):
        for j in range(col_grid):
            grid[i][j].draw(win)

    pygame.display.update()

def main():
    win = pygame.display.set_mode((width_win,width_win))
    pygame.display.set_caption("Title")

    Empty_Grid = init_grid()
    Grid = obstacle_field_generator(Empty_Grid,win, animate= True)
    pygame.quit()
    return None



