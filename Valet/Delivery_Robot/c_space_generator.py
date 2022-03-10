import pygame
from car import *
import numpy as np


class graph_node:
    def __init__(self,state,parent,cost) -> None:
        self.state = state
        self.pos = tuple(state[0:1])
        self.angle = state[2]
        self.parent = parent
        self.child = []
        self.cost = cost

    
    def add_children(self,child):
        self.child.append(child)

    def get_child(self):
        return self.child
    


    

