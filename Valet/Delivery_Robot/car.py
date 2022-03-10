import pygame
import numpy as np
from math import *

RED = (255,0,0)
WHITE = (255,255,255)


class CAR:
    def __init__(self,max_x = 600,max_y = 400,pos =(0,0),angle = 0,r = 1/2*pi,L = 20,height = 36,width = 20) -> None:
        self.pos = pos
        self.angle = angle
        self.x = pos[0]
        self.y = pos[1]
        self.height = height
        self.width = width 
        self.centery = self.height//2
        self.centerx = 0
        self.midbottomx = self.height//2
        self.midbottomy = self.width//2
        self.r = r
        self.L = L
        self.max_x = max_y
        self.max_y = max_y
        self.surf = pygame.Surface((self.height,self.width))
        self.surf.set_colorkey(WHITE)
        self.surf.fill(RED)


    def next_state(self,vel_l,vel_r):
        delta_x = self.r*(vel_r + vel_l)*cos(self.angle)/2
        delta_y = self.r*(vel_r + vel_l)*sin(self.angle)/2
        delta_angle = self.r*(vel_r-vel_l)/self.L

        self.x = self.x + delta_x
        self.y = self.y + delta_y
        self.angle = self.angle +delta_angle

    def T_mat(self):
        T = np.array([[sin(self.angle), -cos(self.angle),self.x],
                                [cos(self.angle),sin(self.angle),self.y],
                                [0,0,1]])
        return T

    def transform_center(self):
        x = np.matmul(self.T_mat(),np.array([self.centerx,self.centery,1]).T)
        return x[0],x[1]
    
    def transform_midbottom(self):
        x = np.matmul(self.T_mat(),np.array([self.midbottomx,self.midbottomy,1]).T)

        return x[0],x[1]

    def reset(self):
        self.centerx = self.height//2
        self.centery = 0
    
    def draw(self,win):
    
        surf = pygame.transform.rotate(self.surf,angle = np.rad2deg(self.angle))
        rect1 = surf.get_rect()
        rect1.center = self.transform_center()
        rect1.midbottom = self.transform_midbottom()
        win.blit(surf,rect1)
        pygame.draw.rect(win,(0,255,0),rect1,width = 1)
        pygame.draw.circle(win,(0,255,0),self.transform_center(),2)

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
    car.draw(win)
    car.next_state(2*pi,2*pi)
    pygame.time.delay(1000)
    pygame.display.update()


