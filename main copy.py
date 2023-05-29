import pygame
from pygame.locals import *
from sys import exit
from pygame.sprite import Group
import os

pygame.init()
LARGURA = 800
ALTURA = 640
TELA = pygame.display.set_mode((LARGURA, ALTURA))
branco = pygame.font.Font('fonts/pixelart.tff',12)
pontos = branco.render("0",True,(255,0,0))

TELA.blit(pontos, (100, 200))
while True:
    TELA.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    TELA.blit(pontos,(ALTURA-100,LARGURA-100))
    pygame.display.update()