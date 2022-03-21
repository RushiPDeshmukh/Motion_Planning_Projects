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
        child.append((node(car.next_state(-1,1),parent=self),cost+2))
        child.append((node(car.next_state(1,-1),parent=self),cost+2))
        return child
    

