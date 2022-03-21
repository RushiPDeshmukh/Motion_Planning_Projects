import pygame
from car import *
import numpy as np
from collections import deque


class node:
    def __init__(self,state,parent=None) -> None:
        self.state = state
        self.pos = (state[0],state[1])
        self.angle = state[2]
        self.angle_trailer = state[3]
        self.pos_trailer = (state[4],state[5])
        self.parent = parent
        self.child = []
    
    def add_child(self,child,cost):
        self.child.append((child,cost))

    def get_child(self):
        return self.child
    
    def remove_child(self,child,cost):
        self.child.remove((child,cost))

    def find_child(self,car,root):
        car.change_state(self.state)
        child = []
        cost = heuristic_cost(self.state,root)/1.5
        child.append((node(car.next_state(10,0),parent=self),cost+1))
        child.append((node(car.next_state(-10,0),parent=self),cost+20))
        child.append((node(car.next_state(10,30),parent=self),cost+30))
        child.append((node(car.next_state(10,-30),parent=self),cost+30))
        return child
    

def heuristic_cost(state,goal):
    s_x,s_y,s_angle,_,s_x1,s_y1 = state
    g_x,g_y,g_angle,_,g_x1,g_y1 = goal
    cost = ((s_x-g_x)**2 + (s_y-g_y)**2 + (s_x1-g_x1)**2 + (s_y1 - g_y1)**2 + (s_angle-g_angle)/2**2)**0.5
    return cost

def draw_path(path):
    [pygame.draw.circle(win,RED,center=(x,y),radius=2,width=2) for x,y,_,_,_,_ in path]
    return

car = CAR(pos=(300,200),angle_car=-90)
run = True
pygame.init()
width_win = 600
height_win = 400
win = pygame.display.set_mode((width_win,height_win))
pygame.display.set_caption("Title")

win.fill(WHITE)
goal_state = (370,300,0,0,330,300)
goal_rect = pygame.Rect(270,250,200,50)
goal_rect.center = (350,300)
pygame.draw.circle(win,RED,center=(goal_state[0],goal_state[1]),radius=2,width=2)
pygame.draw.rect(win,RED,goal_rect,1)
queue = deque()
root_node = node(car.get_state())
queue.append((root_node,0))
visited = []
state = root_node.state
visited.append(state)

def check_goal(state,goal_rect):
    rect1,rect2 = car.get_ref_rects(state)
    return pygame.Rect.contains(goal_rect,rect1) and pygame.Rect.contains(goal_rect,rect2)

while len(queue)>0:
    queue = sorted(queue,key = lambda x:x[1])
    curr_node,cost = queue.pop(0)
    print(heuristic_cost(curr_node.state,goal_state))

    #if curr_node.state == goal_state or heuristic_cost(curr_node.state,goal_state)<10 and curr_node.state[2]-goal_state[2]<10:
    if check_goal(curr_node.state,goal_rect):
        print("Done!!")
        print(curr_node.state)
        goal_state = curr_node
        break
    child_nodes = curr_node.find_child(car,root_node.state)
    for child_node,cost in child_nodes:
        x,y,angle,angle1,x1,y1 = child_node.state

        if (x,y,angle,angle1,x1,y1) not in visited and 0<=x<600 and 0<=y<400 and 0<=angle<=360:
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
    print(node.state)

run = True
while run:
    win.fill(WHITE)
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            run = False
            pygame.quit()
        state = car.get_state()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_r:
                for state in reversed(path):
                    win.fill(WHITE)
                    draw_path(path)
                    car.change_state(state)
                    car.draw(win)
                    pygame.time.wait(200)
                    pygame.display.update()
    car.draw(win)
    pygame.display.update()


# queue = deque()
# queue.append(root_node,0)
# while run:
#     events = pygame.event.get()
#     for ev in events:
#         if ev.type == pygame.QUIT:
#             run = False
#             pygame.quit()

#     curr_node,_ = queue.popleft()
#     x,y = curr_node.pos
#     child_nodes = curr_node.get_child()
#     for child in child_node:
#         queue.append(child)

#     pygame.draw.circle(win,BLUE,center=(x,y),radius=2,width=2)
    
#     pygame.time.delay(50)
#     pygame.display.update()
#     if len(queue)==0:
#         run = False

