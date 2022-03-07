from weighted_grid import *

def djikstra( grid):
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
        if grid[curr_node[0]][curr_node[1]].is_goal():
            print("Found it!")
            break
        else:
            for neighbour in grid[curr_node[0]][curr_node[1]].neighbours:
                if not grid[neighbour[0]][neighbour[1]].is_explored():
                    grid[neighbour[0]][neighbour[1]].make_explored()
                   
                    parent[str((neighbour[0],neighbour[1]))] = (curr_node[0],curr_node[1])
                    queue.append(neighbour)
        c +=1
    print(c)
    curr_node = (127,127)
    path_length = 0
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
Grid = obstacle_field_generator(Empty_Grid,win, animate= False, coverage=30)
draw_grid(win,Grid)
djikstra(Grid)
while True:
    draw_grid(win,Grid)
pygame.quit()

