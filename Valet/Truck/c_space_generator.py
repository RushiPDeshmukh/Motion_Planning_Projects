import pygame
from car import *
import numpy as np
from collections import deque
from a_star_planner import heuristic_cost

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
        child.append((node(car.next_state(10,0),parent=self),cost+10))
        child.append((node(car.next_state(-10,0),parent=self),cost+40))
        child.append((node(car.next_state(10,30),parent=self),cost+30))
        child.append((node(car.next_state(10,-30),parent=self),cost+30))
        return child
    


