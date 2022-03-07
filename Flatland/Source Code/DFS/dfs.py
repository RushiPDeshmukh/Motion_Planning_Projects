from obstacle_field import *


def dfs(grid,queue = [],path = [], curr_node=(0,0)):
    queue.append(curr_node)
    parent = {}
    steps = 0
    while queue:
        curr_node = queue.pop(-1)
        if grid[curr_node[0]][curr_node[1]].is_goal():
            print("Found it!")
            break
        else:
            for neighbour in grid[curr_node[0]][curr_node[1]].neighbours:
                if not grid[neighbour[0]][neighbour[1]].is_explored():
                    grid[neighbour[0]][neighbour[1]].make_explored()
                    grid[neighbour[0]][neighbour[1]].draw(win)
                    pygame.display.update()
                    queue.append(neighbour)
                    parent[str(neighbour)] = (curr_node[0],curr_node[1])
        steps += 1
    print(steps)
    curr_node = (127,127)
    while True:
        a = parent[str(curr_node)]
        grid[a[0]][a[1]].make_path()
        grid[a[0]][a[1]].draw(win)
        pygame.display.update()
        if a == (0,0):
            break
        else:
            curr_node = a
    return 
win = pygame.display.set_mode((width_win,width_win))
pygame.display.set_caption("Title")

Empty_Grid = init_grid()
Grid = obstacle_field_generator(Empty_Grid,win, animate= False,coverage= 50)
draw_grid(win,Grid)
dfs(Grid)
while True:
    draw_grid(win,Grid)
pygame.quit()
