import pygame

width = 500
win = pygame.display.set_mode((width,width))
win.fill((255,255,255))

pygame.draw.rect(win,(0,0,0),(250,250,100,100))
pygame.draw.circle(win,(0,0,0),(100,100),20)

while True:
    pygame.display.update()
