""" This file will contain a main simulation file that will run global and local planner to guide the firetruck to the wildfires.
    This code will track time and accordingly trigger fires and record the results for each planner type."""
from environment import *
from utils import *
from firetruck import *
from global_planner_astar import *
if __name__ == "__main__":
    truck = Firetruck()
    width_win = 500
    win = pygame.display.set_mode((width_win,width_win))
    pygame.display.set_caption("Title")
    pygame.font.init()
    font = pygame.font.Font('freesansbold.ttf',10)
    text = font.render("T",True,BLACK)
    textrect = text.get_rect()
    textrect.topleft = (450,10)
    
    run = True
    pos = (0,0)
    f = Forest(coverage=10)
    f.create()
    graph = tree(f)
    t_last = time.time()
    t = 0   
    random_x = np.random.randint(0,50)
    random_y = np.random.randint(0,50)
    while graph[random_x][random_y].type != "drivable":
        random_x = np.random.randint(0,50)
        random_y = np.random.randint(0,50)
    start_state = graph[random_x][random_y]
    truck.change_state((start_state.pos[0],start_state.pos[1],start_state.angle))

    print("Truck starts at ",random_x,random_y)
    while t <= 3600 and run:
        win.fill(WHITE)
        truck.draw(win)
        pygame.display.update()
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.QUIT:
                run = False
                pygame.quit()
        if t%60 == 0:
            goal,fire_goal=f.trigger_fire(t)
        f.draw(win)
    
        path = find_path(start_state,goal,graph=graph)
        print(path)
        path = reversed(path)
        for state in path:
            win.fill(WHITE)
            truck.change_state(state)
            curr_state = truck.get_state()
            truck.draw(win)
            pygame.display.update()
            pygame.time.wait(500)
            if fire_goal.is_nearby(truck.ref_rect(curr_state)):
                fire_goal.extinguish_fire(t)
                start_state = graph[curr_state[0]//10][curr_state[1]//10]
                break
        #Spreading fire is too quick
        if t%20 == 0:
             f.spread_fire(t)
        f.draw(win)
        text = font.render("Time: "+str(t),True,BLACK)
        win.blit(text,textrect) 
        pygame.display.update()
        t += int(time.time() - t_last)
        t_last = time.time()
        print(t)


 