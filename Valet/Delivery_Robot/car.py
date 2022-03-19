from turtle import width
import pygame
import numpy as np
from math import *

RED = (255,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)


class CAR:
    def __init__(self,max_x = 600,max_y = 600,pos =(0,0),angle = 0,r = 30,L = 20,height = 20,width = 30) -> None:
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
        self.surf = pygame.image.load('Delivery_Bot.png')
        self.surf = pygame.transform.scale(self.surf,(width,height))

    def change_state(self,x,y,angle):
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.angle = angle

    def get_state(self):
        return (self.x,self.y,self.angle)


    def next_state(self,vel_l,vel_r):
        delta_x = self.r*(vel_r + vel_l)*cos(radians(-self.angle))/2
        delta_y = self.r*(vel_r + vel_l)*sin(radians(-self.angle))/2
        delta_angle = self.r*10*(vel_r-vel_l)/self.L
        x = self.x + delta_x
        y = self.y + delta_y
        angle =(self.angle +delta_angle)%360
        return (x,y,angle)

    
    def draw(self,win):
    
        surf = pygame.transform.rotate(self.surf,angle = self.angle)
        rect1 = surf.get_rect()
        rect1.center = self.pos

        
        win.blit(surf,rect1)
        # pygame.draw.rect(win,(0,255,0),rect1,width = 1)
        # pygame.draw.circle(win,(0,255,0),self.pos,2)

        return 


if __name__ == '__main__':
    pygame.init()
    width_win = 600
    win = pygame.display.set_mode((width_win,width_win))
    pygame.display.set_caption("Title")

    car = CAR(pos=(300,300))
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
                    x,y,angle = car.next_state(1,1)
                    
                if ev.key == pygame.K_s:
                    x,y,angle = car.next_state(-1,-1)
                    
                if ev.key == pygame.K_a:
                    x,y,angle = car.next_state(-1,1)
                    
                if ev.key == pygame.K_d:
                    x,y,angle = car.next_state(1,-1)
                print(angle)
            car.change_state(x,y,angle)
        car.draw(win)
        pygame.display.update()


