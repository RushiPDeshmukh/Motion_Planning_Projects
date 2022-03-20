from audioop import reverse
import pygame
from sympy import root
from car import *
import numpy as np
from collections import deque


class node:
    def __init__(self,state,parent=None) -> None:
        self.state = state
        self.pos = (state[0],state[1])
        self.angle = state[2]
        self.parent = parent
        self.child = []
    
    def add_child(self,child,cost):
        self.child.append((child,cost))

    def get_child(self):
        return self.child
    
    def remove_child(self,child,cost):
        self.child.remove((child,cost))

    def find_child(self,car,cost):
        cost = 0
        car.change_state(self.state)
        child = []
        child.append((node(car.next_state(1,1),parent=self),cost+1))
        child.append((node(car.next_state(-1,-1),parent=self),cost+4))
        child.append((node(car.next_state(1,-1),parent=self),cost+2))
        child.append((node(car.next_state(-1,1),parent=self),cost+2))
        return child
    

def heuristic_cost(state,goal):
    s_x,s_y,s_angle = state
    g_x,g_y,g_angle = goal
    cost = ((s_x-g_x)**2 + (s_y-g_y)**2)**0.5
    if cost < 10:
        cost = ((s_x-g_x)**2 + (s_y-g_y)**2 + ((s_angle-g_angle)/1)**2)**0.5
    return cost

def draw_path(path):
    [pygame.draw.circle(win,RED,center=(x,y),radius=2,width=2) for x,y,_ in path]
    return

car = CAR(pos=(300,200))
run = True
pygame.init()
width_win = 600
height_win = 400
win = pygame.display.set_mode((width_win,height_win))
pygame.display.set_caption("Title")

win.fill(WHITE)
pygame.draw.circle(win,RED,center=(30,50),radius=2,width=2)
goal_state = (30,50,0)
queue = deque()
root_node = node(car.get_state())
queue.append((root_node,0))
visited = []
x,y,angle = root_node.state
visited.append((x,y,angle))
while len(queue)>0:
    queue = sorted(queue,key = lambda x:x[1])
    curr_node,cost = queue.pop(0)
    print(heuristic_cost(curr_node.state,goal_state))
    if curr_node == goal_state or heuristic_cost(curr_node.state,goal_state)<3 and curr_node.state[2]==goal_state[2]:
        print("Done!!")
        print(curr_node.state)
        goal_state = curr_node
        break
    child_nodes = curr_node.find_child(car,cost)
    for child_node,cost in child_nodes:
        x,y,angle = child_node.state

        if (x,y,angle) not in visited and 0<=x<600 and 0<=y<400 and 0<=angle<=360:
            curr_node.add_child(child_node,cost)
            visited.append(child_node.state)
            
            pygame.draw.circle(win,BLUE,center=(x,y),radius=2,width=2)
    
            pygame.time.delay(5)
            pygame.display.update()
            cost = cost + heuristic_cost(child_node.state,(30,50,0))
            queue.append((child_node,cost))
            
node = goal_state
car.change_state(node.state)
path = []
while node.parent!=None:
    win.fill(WHITE)
    x,y,_ = node.state
    path.append(node.state)
    node = node.parent
    print(node.state)

for state in reversed(path):
    win.fill(WHITE)
    draw_path(path)
    car.change_state(state)
    car.draw(win)
    pygame.time.wait(200)
    # pygame.draw.circle(win,RED,center=(x,y),radius=2,width=2)
    pygame.display.update()

pygame.time.wait(20000)


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

