import pygame
from pygame.locals import *
from sys import exit

pygame.init()

WIDTH,HEIGHT = 500,500

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Projeto")

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    #tela,cor,(x,y,altura,largura)
    pygame.draw.rect(screen,(0,255,255),(250,250,50,50))
    
    #tela,cor,(x,y),raio)
    pygame.draw.circle(screen,(0,50,18),(100,250),30)

    #tela,cor,1°pongo,2°ponto,espesura
    pygame.draw.line(screen,(255,255,255),(10,10),(100,100),5)
    pygame.display.update()