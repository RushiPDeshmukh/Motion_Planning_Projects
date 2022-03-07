
from obstacle_field import *
def cost(grid):
    x,y = grid.shape
    cost_grid = np.zeros((x,y))
    for i in range(x):
        for j in range(y):
            if grid[i][j].is_obstacle():
                cost_grid[i][j] = -1
                if i+1 <=127:
                    cost_grid[i+1][j] = 100#Down
                if j+1 <=127:
                    cost_grid[i][j+1] = 100#right
                if i+1 <=127 and j+1 <=127:
                    cost_grid[i+1][j+1] = 100#downright
                if i-1 >=0:
                    cost_grid[i-1][j] = 100#up
              
                if i-1 >=0 and j+1 <=127:
                    cost_grid[i-1][j+1] = 100#upright
                
                if i-1 >=0 and j-1>=0:
                    cost_grid[i-1][j-1] = 100#upleft
                
                if i+1 <=127 and j-1>=0:
                    cost_grid[i+1][j-1] = 100#downleft
                
                if j-1 >=0:
                    cost_grid[i][j-1] = 100#left
                
                
    return cost_grid


def djikstra( grid,cost_grid):
    queue = []
    curr_node = (0,0)
    queue.append((curr_node[0],curr_node[1],0))
    c = 0
    parent = {}
    while queue:
        queue.sort(key = lambda x:x[2])
        curr_node = queue.pop(0)
        grid[curr_node[0]][curr_node[1]].draw(win)
        pygame.display.update()
        #check if the current node is end node
        if grid[curr_node[0]][curr_node[1]].is_goal():
            print("Found it!")
            break
        #if not then explore the node and find its neighbours
        else:
            for neighbour in grid[curr_node[0]][curr_node[1]].neighbours:
                if not grid[neighbour[0]][neighbour[1]].is_explored():
                    grid[neighbour[0]][neighbour[1]].make_explored()
                   
                    parent[str(neighbour)] = (curr_node[0],curr_node[1])
                    queue.append((neighbour[0],neighbour[1],cost_grid[neighbour[0]][neighbour[1]]))
        c +=1
    print(c)
    curr_node = (127,127)
    path_length = 0
    #Trace the path using parent
    while True:
        path_length +=1
        a = parent[str(curr_node)]
        grid[a[0]][a[1]].make_path()
        grid[a[0]][a[1]].draw(win)
        pygame.display.update()
        if a == (0,0):
            break
        else:
            curr_node = a
    print(path_length)
    return 

win = pygame.display.set_mode((width_win,width_win))
pygame.display.set_caption("Title")



Empty_Grid = init_grid()
#Create a grid with coverage area of 10%
Grid = obstacle_field_generator(Empty_Grid,win, animate= False, coverage=30)
cost_grid = cost(Grid)
draw_grid(win,Grid)

djikstra(Grid,cost_grid=cost_grid)
pygame.quit()

