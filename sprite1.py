import pygame
from pygame.locals import *
from sys import exit
from pygame.sprite import Group

pygame.init()

largura = 640
altura = 480

tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("sprite1")
relogio = pygame.time.Clock()

class Sapo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('treino sprite/attack_1.png')) #carregar imagem
        self.sprites.append(pygame.image.load('treino sprite/attack_2.png'))
        self.sprites.append(pygame.image.load('treino sprite/attack_3.png'))
        self.sprites.append(pygame.image.load('treino sprite/attack_4.png'))
        self.sprites.append(pygame.image.load('treino sprite/attack_5.png'))
        self.sprites.append(pygame.image.load('treino sprite/attack_6.png'))
        self.sprites.append(pygame.image.load('treino sprite/attack_7.png'))
        self.sprites.append(pygame.image.load('treino sprite/attack_8.png'))
        self.sprites.append(pygame.image.load('treino sprite/attack_9.png'))
        self.sprites.append(pygame.image.load('treino sprite/attack_10.png'))
        
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.rect = self.image.get_rect()
        self.rect.topleft = -30,150

        self.animar = False

    def atacar(self):
        self.animar = True

    def update(self):
        if self.animar == True:
            self.atual += 0.25
            if self.atual >=len(self.sprites):
                self.atual = 1
                self.animar = False
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image,(128*5,64*5)) #mudar tamanho
    

todas_sprites = pygame.sprite.Group()
sapo = Sapo()
todas_sprites.add(sapo)

background = pygame.image.load('background1.jpg').convert()
background = pygame.transform.scale(background,(largura,altura))

while True:
    relogio.tick(60)
    tela.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_j:
                sapo.atacar()

    tela.blit(background,(0,0))     
    todas_sprites.draw(tela)
    todas_sprites.update()
    pygame.display.flip()