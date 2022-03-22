from car import *
from c_space_generator import *

pygame.init()
width_win = 600
height_win = 600
win = pygame.display.set_mode((width_win,height_win))
pygame.display.set_caption("Title")

def heuristic_cost(state,goal):
    s_x,s_y,s_angle,_,s_x1,s_y1 = state
    g_x,g_y,g_angle,_,g_x1,g_y1 = goal
    cost = ((s_x-g_x)**2 + (s_y-g_y)**2 + (s_x1-g_x1)**2 + (s_y1 - s_y1)**2 + (s_angle-s_angle)/2**2)**0.5
    return cost

def draw_path(path):
    [pygame.draw.circle(win,RED,center=(x,y),radius=2,width=2) for x,y,_,_,_,_ in path]
    return


def collision(car_rect,obs):
    collide = False
    for obstacle in obs:
        collide = pygame.Rect.colliderect(obstacle,car_rect)
        if collide == True:
            break   
    return  collide

def check_goal(state,goal_rect):
    rect1,rect2 = car.get_ref_rects(state)
    return pygame.Rect.contains(goal_rect,rect1) and pygame.Rect.contains(goal_rect,rect2)



def find_path(root_node,goal_state):
    queue = []
    queue.append((root_node,0))
    goal_rect = pygame.Rect(0,0,120,60)
    goal_rect.center = (goal_state[0],goal_state[1])
    pygame.draw.rect(win,RED,goal_rect,1)
    visited = []
    visited.append(root_node.state)
    pygame.time.delay(2000)
    while len(queue)>0:
        queue = sorted(queue,key = lambda x:x[1])
        curr_node,cost = queue.pop(0)
        pygame.draw.circle(win,RED,center=(goal_state[0],goal_state[1]),radius=2,width=2)#goal point
        obstacle1 = pygame.Rect(0,0,200,200)
        obstacle1.center = (300,300)
        car1 = pygame.Rect(0,0,30,20)
        car1.center = (50,550)
        pygame.draw.rect(win,BLUE,obstacle1)
        pygame.draw.rect(win,BLUE,car1)
        obs = [obstacle1,car1]

        rect1,rect2 = car.get_ref_rects(curr_node.state)
        print(heuristic_cost(curr_node.state,goal_state))
        if pygame.Rect.contains(goal_rect,rect1) and pygame.Rect.contains(goal_rect,rect2) and abs(curr_node.angle-goal_state[2]) <10:
            print("Done!!")
            print(curr_node.state)
            goal_state = curr_node
            break
        child_nodes = curr_node.find_child(car,root_node.state)
        for child_node,cost in child_nodes:
            x,y,angle,angle1,x1,y1 = child_node.state
            rect1,rect2 = car.get_ref_rects(child_node.state)
            if (x,y,angle,angle1,x1,y1) not in visited and not collision(rect1,obs) and not collision(rect2,obs):
                curr_node.add_child(child_node,cost)
                visited.append(child_node.state)
                print(heuristic_cost(curr_node.state,goal_state))
                
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
        path.append(node.state)
        node = node.parent
    return path


if __name__ == "__main__":
    car = CAR(pos=(50,100),angle_car=-90,angle_trailer1=-90)
   
    win.fill(WHITE)
    
    goal_state = (150,550,0,0,50,550)
    queue = deque()
    root_node = node(car.get_state())
    obstacle1 = pygame.Rect(0,0,200,200)
    obstacle1.center = (300,300)
    car1 = pygame.Rect(0,0,30,20)
    car1.center = (50,550)
        
    path = find_path(root_node,goal_state)
    for state in reversed(path):
        win.fill(WHITE)
        pygame.draw.rect(win,BLUE,obstacle1)
        pygame.draw.rect(win,BLUE,car1)
        draw_path(path)
        print("here")
        car.change_state(state)
        car.draw(win)
        pygame.time.wait(200)
        # pygame.draw.circle(win,RED,center=(x,y),radius=2,width=2)
        pygame.display.update()


