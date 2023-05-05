import pygame
from pygame.locals import *
from sys import exit
from pygame.sprite import Group
import os

diretorio_principal = os.path.dirname(__file__)  #caminho absoluto do script
diretorio_personagem = os.path.join(diretorio_principal,'spritesheet personagem')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

pygame.init()

LARGURA = 800
ALTURA = 640
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("sprite2")
relogio = pygame.time.Clock()

sprite_sheet = pygame.image.load(os.path.join(diretorio_personagem, 'andar.png')).convert_alpha()

class Protagonista(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons,'coin.wav'))
        self.som_pulo.set_volume(1)
        self.imagens_protagonista = []
        for i in range(6):
            img = sprite_sheet.subsurface((i * 87, 0), (87, 160)) #usar spritesheet
            img = pygame.transform.scale(img,(35,70)) #mudar tamanho de cada sprite
            self.imagens_protagonista.append(img) #armazenar sprites em um array

        self.index_lista_andar = 0
        self.index_lista_andar = 0
        self.image = self.imagens_protagonista[self.index_lista_andar] #render
        self.rect = self.image.get_rect() 
        self.rect.center = (50,ALTURA-70) #posição inicial do protagonista
        
        self.limite = 350
        self.no_ar = False #detecção para pulo
        self.pos_y_inicial = ALTURA-70-160//2
        
        self.andamento = False

    
    def andar(self):
        self.andamento = True
        if self.index_lista_andar > 5:    
            self.index_lista_andar = 0 #voltar para primeiro sprite
        self.index_lista_andar += 0.07
  
    def movimentar(self):
        if pygame.key.get_pressed()[K_a]:
            self.andar()
            self.rect.x -= 5
        if pygame.key.get_pressed()[K_d]:
            self.andar()
            self.rect.x += 5

    def pular(self):
        self.no_ar = True
        self.som_pulo.play()
    
    def update(self):
        if self.no_ar == True:
            if self.rect.top <= 250:
                self.no_ar = False
            self.rect.y -= 10
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 10
            else:
                self.rect.y = self.pos_y_inicial
        if self.andamento == True:
            self.andar()
            self.image = self.imagens_protagonista[int(self.index_lista_andar)] #animação
            self.andamento = False


todas_sprites = pygame.sprite.Group()
protagonista = Protagonista()
todas_sprites.add(protagonista)

background = pygame.image.load('back.jpg').convert()
background = pygame.transform.scale(background, (LARGURA, ALTURA))

while True:
    relogio.tick(60)
    TELA.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if pygame.key.get_pressed()[K_SPACE]:
            if protagonista.rect.y <= protagonista.limite:
                pass
            else:
                protagonista.pular()
        '''if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if protagonista.rect.y != protagonista.pos_y_inicial:
                    pass
                else:
                    protagonista.pular()'''
    protagonista.movimentar()
    TELA.blit(background, (0, 0))
    todas_sprites.draw(TELA)
    todas_sprites.update()
    pygame.display.flip()
