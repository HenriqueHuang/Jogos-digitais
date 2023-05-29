import pygame
from pygame.locals import *
from sys import exit
from pygame.sprite import Group
import random
import os
#Configuração inicial
diretorio_principal = os.path.dirname(__file__)  #caminho absoluto do script
diretorio_personagem = os.path.join(diretorio_principal,'spritesheet personagem')
diretorio_sprites = os.path.join(diretorio_principal,'sprites')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

pygame.init()
LARGURA = 800
ALTURA = 640
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("sprite2")
relogio = pygame.time.Clock()
#Fonte
branco = pygame.font.Font("fonts/vazio.ttf",15)
preto = pygame.font.Font("fonts/cheio.ttf",15)

#pontuação
pontuacao = 0

#Sprites
sprite_protagonista = pygame.image.load(os.path.join(diretorio_personagem, 'andar.png')).convert_alpha()
sprite_tsunami = pygame.image.load(os.path.join(diretorio_sprites, 'tsunami.png')).convert_alpha()
sprite_fireball = pygame.image.load(os.path.join(diretorio_sprites, 'fireball.png')).convert_alpha()

class Protagonista(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #Vida do personagem
        self.vida = 5
        self.coracao_img = pygame.image.load("coracao.png").convert_alpha()
        self.coracao_img = pygame.transform.scale(self.coracao_img,(40,40)) 
        self.coracao_x = 10
        self.coracao_y = 10
        self.espaco_coracao = 40
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))

        #variáveis do pulo
        self.vel_y = 0
        self.is_jumping = False
        self.jump_start_time = 0
        self.JUMP_HEIGHT = -10
        self.MAX_JUMP_TIME = 50  # Tempo máximo de salto em milissegundos
        self.GRAVITY = 0.8
        
        #variáveis do andamento
        self.andamento = False

        #som do pulo
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons,'coin.wav'))
        self.som_pulo.set_volume(1)
        
        #animação
        self.imagens_protagonista = []
        for i in range(6):
            img = sprite_protagonista.subsurface((i * 87, 0), (87, 160)) #usar spritesheet
            img = pygame.transform.scale(img,(30,60)) #mudar tamanho de cada sprite
            self.imagens_protagonista.append(img) #armazenar sprites em um array
        self.index_lista_andar = 0
        self.image = self.imagens_protagonista[self.index_lista_andar] #render
        self.rect = self.image.get_rect() 
        self.rect.center = (100,ALTURA-200) #posição inicial do protagonista

    def andar(self):
        self.andamento = True
        if self.index_lista_andar > 5:    
            self.index_lista_andar = 0 #voltar para primeiro sprite
        self.index_lista_andar += 0.07
    
    def pular(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_start_time = pygame.time.get_ticks()
            
    def movimentar(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.andar()
            self.rect.x -= 4.5
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.andar()
            self.rect.x += 4.5
            
    def update(self):
        # vida do personagem
        if self.vida > 5:
            self.vida = 5
        if self.vida < 0:
            self.vida = 0


        for i in range(self.vida):
            coracao_rect = self.coracao_img.get_rect()
            coracao_rect.x = self.coracao_x + i * self.espaco_coracao
            coracao_rect.y = self.coracao_y
            self.tela.blit(self.coracao_img, coracao_rect)

        # pulo
        if self.is_jumping:
            jump_duration = pygame.time.get_ticks() - self.jump_start_time
            if jump_duration <= self.MAX_JUMP_TIME:
                self.vel_y = self.JUMP_HEIGHT
            else:
                self.is_jumping = False

        self.rect.y += self.vel_y
        self.vel_y += self.GRAVITY

        if self.rect.y >= ALTURA - 100:
            self.rect.y = ALTURA - 100
            self.vel_y = 0

        # andamento
        if self.andamento == True:
            self.andar()
            self.image = self.imagens_protagonista[int(self.index_lista_andar)] #animação
            self.andamento = False
        
class Tsunami(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_tsunami = []
        for i in range(4):
            img = sprite_tsunami.subsurface((i * 213, 0), (213, 204)) #usar spritesheet
            img = pygame.transform.scale(img,(600,750)) #mudar tamanho de cada sprite
            self.imagens_tsunami.append(img) #armazenar sprites em um array

        self.index_lista_aproximar = 0
        self.image = self.imagens_tsunami[self.index_lista_aproximar] #render
        self.rect = self.image.get_rect() 
        self.rect.center = (0,ALTURA-250) #posição inicial do protagonista
        self.velocidade = 0 

    def aproximar(self):
        if self.index_lista_aproximar > 3:    
            self.index_lista_aproximar = 0 #voltar para primeiro sprite
        self.index_lista_aproximar += 0.02

        self.velocidade += 0.25

        if self.velocidade == 1:
            self.velocidade = 0
            self.rect.x += 1

        if self.rect.colliderect(protagonista):
            print("morreu")
        
    def update(self):
        self.aproximar()
        self.image = self.imagens_tsunami[int(self.index_lista_aproximar)] #animação

class Mapa(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("back2 (1).png").convert()
        self.image = pygame.transform.scale(self.image,(LARGURA*2,ALTURA)) #mudar tamanho de cada sprite
        self.rect = self.image.get_rect(x=0,y=0)

    def update(self):
        if self.rect.x < -LARGURA:
            self.rect.x = 0
        self.rect.x -= 3

class Fireball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("fireball.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(60,30)) #mudar tamanho de cada sprite
        self.image = pygame.transform.rotate(self.image,180)
        self.pos_init = random.randrange(50,ALTURA-100)
        self.velocidade = random.randrange(2,7)
        self.rect = self.image.get_rect(x=LARGURA,y=self.pos_init)
        self.rect.y = random.randrange(50,ALTURA-100)
    
    def voltar(self):
        self.rect.x = LARGURA
        self.rect.y= random.randrange(50,ALTURA-70)
        self.velocidade = random.randrange(2,7)

    def update(self):
        if self.rect.topright[0] < 0:
            self.voltar()
        elif self.rect.colliderect(protagonista):
            self.voltar()
            global pontuacao
            pontuacao -= 200
            protagonista.vida -= 1
        self.rect.x -= self.velocidade

class Star(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("coracao.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,40)) #mudar tamanho de cada sprite
        self.pos_init = random.randrange(50,ALTURA-100)
        self.velocidade = random.randrange(1,7)
        self.rect = self.image.get_rect(x=LARGURA,y=self.pos_init)
        self.rect.y = random.randrange(50,ALTURA-100)

    def voltar(self):
        self.rect.x = LARGURA
        self.rect.y= random.randrange(50,ALTURA-70)
        self.velocidade = random.randrange(2,7)

    def update(self):
        if self.rect.topright[0] < 0:
            self.voltar()
        elif self.rect.colliderect(protagonista):
            self.voltar()
            global pontuacao
            pontuacao += 300
            protagonista.vida += 1
        self.rect.x -= self.velocidade

#Criar imagens
todas_sprites = pygame.sprite.Group()
protagonista = Protagonista()
mapa = Mapa()
todas_sprites.add(mapa, protagonista)
for i in range(6):
    fireball = Fireball()
    todas_sprites.add(fireball)

for i in range(5):
    star = Star()
    todas_sprites.add(star)

#Play
while True:
    relogio.tick(60)
    TELA.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                protagonista.pular()
    
    pontos = preto.render("Pontos:{}".format(pontuacao),False,(0,0,0))
    protagonista.movimentar()
    todas_sprites.draw(TELA)
    todas_sprites.update()
    TELA.blit(pontos,(650,20))
    pygame.display.flip()
