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

    def find_child(self,car):
        car.change_state(self.pos[0],self.pos[1],self.angle)
        child = []
        child.append((node(car.next_state(1,1),parent=self),10))
        child.append((node(car.next_state(-1,-1),parent=self),20))
        child.append((node(car.next_state(1,-1),parent=self),30))
        child.append((node(car.next_state(-1,1),parent=self),30))
        return child


car = CAR(pos=(300,200))
run = True
pygame.init()
width_win = 600
height_win = 400
win = pygame.display.set_mode((width_win,height_win))
pygame.display.set_caption("Title")

win.fill(WHITE)

queue = deque()
root_node = node(car.get_state())
queue.append((root_node,0))
visited = []
x,y,angle = root_node.state
visited.append((x,y,angle))
while len(queue)>0:
    queue = sorted(queue,key = lambda x:x[1])
    curr_node,cost = queue.pop(0)
    child_nodes = curr_node.find_child(car)
    for child_node,cost in child_nodes:
        x,y,angle = child_node.state

        if (x,y,angle) not in visited and 0<=x<600 and 0<=y<400 and 0<=angle<=360:
            curr_node.add_child(child_node,cost)
            visited.append(child_node.state)
            print(angle)
            pygame.draw.circle(win,BLUE,center=(x,y),radius=2,width=2)
    
            pygame.time.delay(5)
            pygame.display.update()
            queue.append((child_node,cost))
            


queue = deque()
queue.append(root_node,0)
while run:
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            run = False
            pygame.quit()

    curr_node,_ = queue.popleft()
    x,y = curr_node.pos
    child_nodes = curr_node.get_child()
    for child in child_node:
        queue.append(child)

    pygame.draw.circle(win,BLUE,center=(x,y),radius=2,width=2)
    
    pygame.time.delay(50)
    pygame.display.update()
    if len(queue)==0:
        run = False

