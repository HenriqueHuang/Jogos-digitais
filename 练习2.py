import pygame
from pygame.locals import *

pygame.init()

WIDTH,HEIGHT = 600,600

x = WIDTH/2
y = HEIGHT/2
speed = 10
screen = pygame.display.set_mode((WIDTH,HEIGHT))
relogio = pygame.time.Clock()

running = True
while running:
    relogio.tick(60)
    screen.fill("white")
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        """if event.type == KEYDOWN:
            if event.key == K_a:
                x-=speed
            if event.key == K_d:
                x+=speed
            if event.key == K_w:
                y-=speed
            if event.key == K_s:
                y+=speed"""
    if pygame.key.get_pressed()[K_a]:
        x-=speed
    if pygame.key.get_pressed()[K_d]:
        x+=speed
    if pygame.key.get_pressed()[K_w]:
        y-=speed
    if pygame.key.get_pressed()[K_s]:
        y+=speed

    rect = pygame.draw.rect(screen,(0,255,255),(x,y,50,50))
    if x == WIDTH:
        x=0
    elif x < -50:
        x=WIDTH
    elif y == HEIGHT:
        y=0
    elif y < -50:
        y=HEIGHT
    
    pygame.display.update()