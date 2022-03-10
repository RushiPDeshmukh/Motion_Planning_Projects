import pygame
import numpy as np
from math import *

RED = (255,0,0)
WHITE = (255,255,255)


class CAR:
    def __init__(self,max_x = 600,max_y = 400,pos =(0,0),angle = 0,r = 1/2*pi,L = 20,height = 20,width = 20) -> None:
        self.pos = pos
        self.angle = angle
        self.x = pos[0]
        self.y = pos[1]
        self.height = height
        self.width = width 
    
        self.r = r
        self.L = L
        self.max_x = max_y
        self.max_y = max_y
        self.surf = pygame.Surface((self.height,self.width))
        self.surf.set_colorkey(WHITE)
        self.surf.fill(RED)

    def change_state(self,x,y,angle):
        self.x = x
        self.y = y
        self.angle = angle


    def next_state(self,vel_l,vel_r,curr_state):
        delta_x = self.r*(vel_r + vel_l)*cos(self.angle)/2
        delta_y = self.r*(vel_r + vel_l)*sin(self.angle)/2
        delta_angle = self.r*(vel_r-vel_l)/self.L
        x,y,angle = curr_state
        x = self.x + delta_x
        y = self.y + delta_y
        angle = self.angle +delta_angle
        return (x,y,angle)
    
    def draw(self,win):
    
        surf = pygame.transform.rotate(self.surf,angle = np.rad2deg(self.angle))
        rect1 = surf.get_rect()
        rect1.center = self.pos

        
        win.blit(surf,rect1)
        pygame.draw.rect(win,(0,255,0),rect1,width = 1)
        pygame.draw.circle(win,(0,255,0),self.pos,2)

        return 



pygame.init()
width_win = 600
win = pygame.display.set_mode((width_win,width_win))
pygame.display.set_caption("Title")

car = CAR(600,600,(300,300))
run = True
while run:
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            run = False
            pygame.quit()

    
    win.fill(WHITE)
    car.next_state(2*pi,-2*pi)
    car.draw(win)
    
    pygame.time.delay(1000)
    pygame.display.update()


