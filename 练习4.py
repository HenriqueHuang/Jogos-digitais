import pygame
from pygame.locals import *
from random import *

pygame.init()

# definição inicial
fonte = pygame.font.SysFont('roboto',40,True,True) 
WIDTH,HEIGHT = 600,600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
relogio = pygame.time.Clock()

BGM = pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.set_volume(0.02)
pygame.mixer.music.play(-1) #-1 deixa musica repetir
colid_sound = pygame.mixer.Sound('coin.wav')

x_cobra,y_cobra = WIDTH/2,HEIGHT/2
x_maca,y_maca= randint(30,WIDTH),randint(30,HEIGHT)

speed = 5
x_controle = 20
y_controle = 0

lista_cobra = []
comprimento_inicial = 5

pontos = 0

# funções
def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        #XeY = [x,y], #XeY[0] = x, #XeY[1] = y
        
        pygame.draw.rect(screen,(0,255,0),(XeY[0],XeY[1],20,20))

# rodar o jogo
running = True
while running:
    relogio.tick(60)
    screen.fill("white")
    # ponto
    msg = f'Pontos: {pontos}'
    texto_format = fonte.render(msg,True,(0,0,0)) 

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_controle==speed:
                    pass
                else:
                    x_controle = -speed
                    y_controle = 0
               
            if event.key == K_d:
                if x_controle==-speed:
                    pass
                else:
                    x_controle = speed
                    y_controle = 0
            if event.key == K_w:
                if y_controle==speed:
                    pass
                else:
                    x_controle = 0
                    y_controle = -speed
            if event.key == K_s:
                if y_controle==speed:
                    pass
                else:
                    x_controle = 0
                    y_controle = speed
    x_cobra = x_cobra + x_controle
    y_cobra = y_cobra + y_controle
                
    # movimento
    '''
    if pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_LEFT]:
        x_cobra-=speed
    if pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_RIGHT]:
        x_cobra+=speed
    if pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_UP]:
        y_cobra-=speed
    if pygame.key.get_pressed()[K_s] or pygame.key.get_pressed()[K_DOWN]:
        y_cobra+=speed
    '''

    cobra = pygame.draw.rect(screen,(0,255,0),(x_cobra,y_cobra,20,20))
    maca = pygame.draw.rect(screen,(255, 0, 0),(x_maca,y_maca,20,20))
    # colisao
    if cobra.colliderect(maca):
        x_maca,y_cobra= randint(0,WIDTH),randint(0,HEIGHT)
        pontos += 1
        comprimento_inicial +=1
        colid_sound.play()
    
    if x_cobra == WIDTH:
        x_cobra=0
    elif x_cobra < -50:
        x_cobra=WIDTH
    elif y_cobra == HEIGHT:
        y_cobra=0
    elif y_cobra < -50:
        y_cobra=HEIGHT

    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)
    
    lista_cobra.append(lista_cabeca)

    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)

    screen.blit(texto_format,(400,50))

    pygame.display.update()