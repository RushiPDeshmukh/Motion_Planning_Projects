import google_auth_oauthlib
from car import *
from c_space_generator import *


def heuristic_cost(state,goal):
    s_x,s_y,s_angle = state
    g_x,g_y,g_angle = goal
    cost = ((s_x-g_x)**2 + (s_y-g_y)**2)**0.5
    if cost < 2:
        cost = ((s_x-g_x)**2 + (s_y-g_y)**2 + (s_angle-g_angle)**2)**0.5
    return cost

def draw_path(path):
    [pygame.draw.circle(win,RED,center=(x,y),radius=2,width=2) for x,y,_ in path]
    return

def collision(car_rect,obs):
    collide = False
    for obstacle in obs:
        collide = pygame.Rect.colliderect(obstacle,car_rect)
        if collide == True:
            break   
    return  collide


def find_path(root_node,goal_state):
    queue = []
    queue.append((root_node,0))
    visited = []
    x,y,angle = root_node.state
    goal_rect = pygame.Rect(0,0,60,40)
    goal_rect.center = (goal_state[0],goal_state[1])
    visited.append((x,y,angle))
    pygame.time.delay(2000)
    while len(queue)>0:
        queue = sorted(queue,key = lambda x:x[1])
        curr_node,cost = queue.pop(0)
        pygame.draw.circle(win,RED,center=(goal_state[0],goal_state[1]),radius=2,width=2)#goal point
        obstacle1 = pygame.Rect(0,0,300,300)
        obstacle1.center = (300,300)
        car1 = pygame.Rect(0,0,30,20)
        car1.center = (50,550)
        car2 = pygame.Rect(0,0,30,20)
        car2.center = (150,550)
        pygame.draw.rect(win,BLUE,obstacle1)
        pygame.draw.rect(win,BLUE,car1)
        pygame.draw.rect(win,BLUE,car2)
        obs = [obstacle1,car1,car2]
        rect = car.ref_rect(curr_node.state)
        print(heuristic_cost(curr_node.state,goal_state))
        if pygame.Rect.contains(goal_rect,rect) and abs(curr_node.angle-goal_state[2]) <20:
            print("Done!!")
            print(curr_node.state)
            goal_state = curr_node
            break
        child_nodes = curr_node.find_child(car,root_node.state)
        for child_node,cost in child_nodes:
            x,y,angle = child_node.state
            car_rect = car.ref_rect(child_node.state)

            if (x,y,angle) not in visited and not collision(car_rect,obs):
                curr_node.add_child(child_node,cost)
                visited.append(child_node.state)
                
                pygame.draw.circle(win,BLUE,center=(x,y),radius=2,width=2)

                pygame.time.delay(5)
                pygame.display.update()
                cost = cost + heuristic_cost(child_node.state,goal_state)
                queue.append((child_node,cost))
            
    node = goal_state
    car.change_state(node.state)
    path = []
    while node.parent!=None:
        win.fill(WHITE)
        x,y,_ = node.state
        path.append(node.state)
        node = node.parent
    return path


if __name__ == "__main__":
    car = CAR(pos=(50,50),angle=90)
    pygame.init()
    width_win = 600
    height_win = 600
    win = pygame.display.set_mode((width_win,height_win))
    pygame.display.set_caption("Title")
    win.fill(WHITE)
    
    goal_state = (100,550,0)
    queue = deque()
    root_node = node(car.get_state())
    obstacle1 = pygame.Rect(0,0,300,300)
    obstacle1.center = (300,300)
    car1 = pygame.Rect(0,0,30,20)
    car1.center = (50,550)
    car2 = pygame.Rect(0,0,30,20)
    car2.center = (150,550)
        
    path = find_path(root_node,goal_state)
    for state in reversed(path):
        win.fill(WHITE)
        pygame.draw.rect(win,BLUE,obstacle1)
        pygame.draw.rect(win,BLUE,car1)
        pygame.draw.rect(win,BLUE,car2)
        draw_path(path)
        print("here")
        car.change_state(state)
        car.draw(win)
        pygame.time.wait(200)
        # pygame.draw.circle(win,RED,center=(x,y),radius=2,width=2)
        pygame.display.update()


