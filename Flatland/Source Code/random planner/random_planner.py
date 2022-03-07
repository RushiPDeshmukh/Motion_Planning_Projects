from obstacle_field import *


def random_planner(grid,queue = [], curr_node=(0,0)):
    queue.append(curr_node)
    steps = 0
    while steps<=100000 :
        if grid[curr_node[0]][curr_node[1]].is_goal():
            print("Found it!")
            break
        else:
            neighbour = grid[curr_node[0]][curr_node[1]].neighbours
            #Choose random neighbour to explore
            random_num = random.randint(0,len(neighbour))
            neighbour = neighbour[random_num]
            grid[neighbour[0]][neighbour[1]].make_explored()
            grid[neighbour[0]][neighbour[1]].draw(win)
            pygame.display.update()
            curr_node = neighbour
        steps += 1
    curr_node = (127,127)
    print(steps)
    return 
win = pygame.display.set_mode((width_win,width_win))
pygame.display.set_caption("Title")

Empty_Grid = init_grid()
Grid = obstacle_field_generator(Empty_Grid,win, animate= False, coverage=10)
draw_grid(win,Grid)
random_planner(Grid)
pygame.quit()