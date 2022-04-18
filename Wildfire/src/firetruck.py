"""This python code defines a firetruck class.
    - Variables of the firetruck.
    - kinematics based next state calculator.
    - draw function to draw the firetruck on pygame window.
    - other utility functions like change_state, get_state,etc

"""
import pygame
import numpy as np
from utils import *
from math import *
class Firetruck:
    def __init__(self,max_x = 500,max_y = 500,pos =(0,0),angle = 0,steering_angle = 0,height = 10,width = 6,L=6) -> None:
        self.pos = pos
        self.angle = angle
        self.x = pos[0]
        self.y = pos[1]
        self.height = height
        self.width = width 
        self.L = L
    
        self.steering_angle = steering_angle
        self.max_x = max_y
        self.max_y = max_y
        self.surf = pygame.image.load('src/utils/firetruck.png')
        self.surf = pygame.transform.scale(self.surf,(height,width))
        self.surf.set_colorkey(WHITE)

    def change_state(self,state):
        x,y,angle = state
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.angle = angle

    def get_state(self):
        return (self.x,self.y,self.angle)


    def next_state(self,vel,steer):
        delta_x = vel*cos(radians(-self.angle))
        delta_y = vel*sin(radians(-self.angle))
        delta_angle = degrees(vel*tan(radians(steer))/self.L)
        self.steering_angle = steer
        x = self.x + delta_x
        y = self.y + delta_y
        angle =(self.angle+delta_angle)%360
        return (x,y,angle)
    
    def ref_rect(self,state):
        x,y,angle = state
        surf = pygame.transform.rotate(self.surf,angle = angle)
        rect1 = surf.get_rect()
        rect1.center = (self.x+7*cos(radians(-self.angle)),self.y+7*sin(radians(-self.angle)))

        return rect1

    
    def draw(self,win):
    
        surf = pygame.transform.rotate(self.surf,angle = self.angle)

        rect1 = surf.get_rect()
        rect1.center = (self.x+3*cos(radians(-self.angle)),self.y+3*sin(radians(-self.angle)))

        
        win.blit(surf,rect1)
        # pygame.draw.rect(win,(0,255,0),rect1,width = 1)
        # pygame.draw.circle(win,(0,255,0),self.pos,2)

        return 


if __name__ == '__main__':
    pygame.init()
    width_win = 600
    win = pygame.display.set_mode((width_win,width_win))
    pygame.display.set_caption("Title")

    car = Firetruck(pos=(300,300))
    run = True
    while run:
        win.fill(WHITE)
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.QUIT:
                run = False
                pygame.quit()
            x,y,angle = car.get_state()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_w:
                    x,y,angle = car.next_state(20,0)
                    print(x,y,angle)
                    
                if ev.key == pygame.K_s:
                    x,y,angle = car.next_state(-20,0)
                    print(x,y,angle)
                    
                if ev.key == pygame.K_a:
                    x,y,angle = car.next_state(10,50)
                    print(x,y,angle)

                if ev.key == pygame.K_d:
                    x,y,angle = car.next_state(10,-50)
                    print(x,y,angle)
                
            car.change_state((x,y,angle))
        car.draw(win)
        pygame.display.update()


