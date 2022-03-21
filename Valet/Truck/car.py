import pygame
import numpy as np
from math import *

RED = (255,100,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
BLACK = (0,0,0)


class CAR:
    def __init__(self,max_x = 600,max_y = 600,pos =(0,0),angle_car = 0,angle_trailer1=0,steering_angle = 0,height = 20,width = 30,d=40) -> None:
        self.pos = pos
        self.angle = angle_car
        self.angle_trailer1 = angle_trailer1

        self.x = pos[0]
        self.y = pos[1]
        self.x1 = self.x - d*cos(radians(-self.angle_trailer1))
        self.y1 = self.y - d*sin(radians(-self.angle_trailer1))

        self.height = height
        self.width = width 
        self.L = 20
        self.d = d
        self.max_x = max_y
        self.max_y = max_y
        self.surf = pygame.image.load('car.png')
        self.surf = pygame.transform.scale(self.surf,(width,height))
        self.surf.set_colorkey(WHITE)
        

    def change_state(self,state):
        x,y,angle,angle_trailer1,x1,y1 = state
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.angle = angle
        self.angle_trailer1 = angle_trailer1
        self.x1 = x1
        self.y1 = y1

    def get_state(self):
        return (self.x,self.y,self.angle,self.angle_trailer1,self.x1,self.y1)


    def next_state(self,vel,steer):
        delta_x = vel*cos(radians(-self.angle))
        delta_y = vel*sin(radians(-self.angle))
        delta_angle = degrees(vel*tan(radians(steer))/self.L)
        delta_angle1 = degrees(vel*sin(1*radians(self.angle - self.angle_trailer1))/self.d)
        x = self.x + delta_x
        y = self.y + delta_y
        angle =(self.angle+delta_angle)%360
        angle1 =(self.angle_trailer1 + delta_angle1)%360
        x1 = x - self.d*cos(radians(-angle1))
        y1 = y - self.d*sin(radians(-angle1))
        return (x,y,angle,angle1,x1,y1)

    def get_ref_rects(self,state):
        self.change_state(state)
        surf_car = pygame.transform.rotate(self.surf,angle = self.angle)

        rect1 = surf_car.get_rect()
        rect1.center = self.pos


        surf_trailer1 = pygame.transform.rotate(self.surf,angle = self.angle_trailer1)

        rect2 = surf_trailer1.get_rect()
        rect2.center = (self.x1,self.y1)
        return rect1,rect2
        

    
    def draw(self,win):
    
        surf_car = pygame.transform.rotate(self.surf,angle = self.angle)

        rect1 = surf_car.get_rect()
        rect1.center = self.pos
        win.blit(surf_car,rect1)

        surf_trailer1 = pygame.transform.rotate(self.surf,angle = self.angle_trailer1)

        rect1 = surf_trailer1.get_rect()
        rect1.center = (self.x1,self.y1)
        win.blit(surf_trailer1,rect1)

        pygame.draw.line(win,BLACK,(self.x1,self.y1),self.pos)
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
            state = car.get_state()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_w:
                    state = car.next_state(4,0)
                    
                if ev.key == pygame.K_s:
                    state = car.next_state(-4,0)
                    
                if ev.key == pygame.K_a:
                    state = car.next_state(2,30)
                    
                if ev.key == pygame.K_d:
                    state = car.next_state(2,-30)
            car.change_state(state)
        car.draw(win)
        pygame.display.update()


