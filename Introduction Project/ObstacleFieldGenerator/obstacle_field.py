import numpy as np
from numpy import random
import matplotlib.pyplot as plt
empty_grid = np.zeros((128,128))
 
obstacle1 = [1,1,1,1]
obstacle2 = [[1,0,0],[1,1,1]]
obstacle3 = [[0,0,1],[1,1,1]]
obstacle4 = [[1,1],[1,1]]
obstacle5 = [[0,1,1],[1,1,0]]
obstacle6 = [[1,1,0],[0,1,1]]
obstacle7 = [[0,1,0],[1,1,1]]
obstacles = {'1':obstacle1,'2':obstacle2,'3':obstacle3,'4':obstacle4,'5':obstacle5,'6':obstacle6,'7':obstacle7}

def obstacle_field_generator(grid,obstacles,coverage=10):
    """AI is creating summary for obstacle_field_generator

    Args:
        grid ([numpy array of 128x128]): This arg contains the grid before it is populated with given obstacles
        obstacles ([Dictionary]): This arg contains different obstacle shapes that we want to deploy in the grid
        coverage (int, optional): This arg tell the total coverage of grid that needs to be populated with obstacles. Defaults to 10.

    Returns:
        [numpy array of 128x128]: grid populated with obstacles with given coverage
    """
    curr_coverage = 0
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
                    grid[random_x][random_y + y] = obstacle[y]
                    occupied_field.append((random_x+x,random_y))
            else:
                for x in range(shape_obstacle[0]):
                    for y in range(shape_obstacle[1]):
                        grid[random_x + x][random_y + y] = obstacle[x][y]
                        occupied_field.append((random_x+x,random_y+y))
            #update the current coverage variable
            curr_coverage = (grid.sum()/(128*128))*100
            
    return grid

    


grid = obstacle_field_generator(empty_grid,obstacles,10)
f = plt.figure()
f.set_size_inches(10,10)
plt.imshow(grid,cmap='BuPu', aspect=1)
plt.savefig('10percent.png')
plt.show()

