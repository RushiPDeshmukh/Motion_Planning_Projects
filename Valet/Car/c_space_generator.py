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
        self.parent = parent
        self.child = []
    
    def add_child(self,child,cost):
        self.child.append((child,cost))

    def get_child(self):
        return self.child
    
    def remove_child(self,child,cost):
        self.child.remove((child,cost))

    def find_child(self,car,root_node):
        
        cost = 0
        car.change_state(self.state)
        child = []
        child.append((node(car.next_state(10,0),parent=self),cost+10))
        child.append((node(car.next_state(-10,0),parent=self),cost+40))
        child.append((node(car.next_state(6,60),parent=self),cost+20))
        child.append((node(car.next_state(6,-60),parent=self),cost+20))
    
        return child
    
