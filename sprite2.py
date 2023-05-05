import pygame
from pygame.locals import *
from sys import exit
from pygame.sprite import Group
import os

diretorio_principal = os.path.dirname(__file__) #caminho absoluto do script
diretorio_personagem = os.path.join(diretorio_principal,'spritesheet personagem')
diretorio_sons = os.path.join(diretorio_principal,'sons')

pygame.init()

LARGURA = 640
ALTURA = 480
TELA = pygame.display.set_mode((LARGURA,ALTURA))
pygame.display.set_caption("sprite1")
relogio = pygame.time.Clock()

sprite_sheet = pygame.pygame.image.load(os.path.join(diretorio_personagem,'andar.png')).convert_alpha()
pygame.Surface.convert_alpha() #deixa sem background

class Protagonista(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_protagonista = []
        for i in range(6):
            img = sprite_sheet.subsurface((i*87,0),(87,160))
            self.imagens_protagonista.append(img)

        self.index_lista = 0
        self.image = self.imagens_protagonista[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (100,100)
    
    def update(self):
        if self.index_lista > 5:
            self.index_lista += 0
        self.index_lista += 0.25
        self.image = self.imagens_protagonista[int(self.index_lista)]

todas_sprites = pygame.sprite.Group()
protagonista = Protagonista()
todas_sprites.add(protagonista)

background = pygame.image.load('background1.jpg').convert_alpha()
background = pygame.transform.scale(background,(LARGURA,ALTURA))

while True:
    relogio.tick(60)
    TELA.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    TELA.blit(background,(0,0))     
    todas_sprites.draw(TELA)
    todas_sprites.update()
    pygame.display.flip()