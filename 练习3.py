import pygame
from pygame.locals import *
from random import *

pygame.init()

WIDTH,HEIGHT = 600,600

#font,tamanho,negrito?,italico?
fonte = pygame.font.SysFont('roboto',40,True,True) 
screen = pygame.display.set_mode((WIDTH,HEIGHT))
relogio = pygame.time.Clock()


BGM = pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1) #-1 deixa musica repetir
colid_sound = pygame.mixer.Sound('coin.wav')

x,y = WIDTH/2,HEIGHT/2
x2,y2= randint(30,WIDTH),randint(30,HEIGHT)
speed = 10
pontos = 0


running = True
while running:
    relogio.tick(60)
    screen.fill("white")
    msg = f'Pontos: {pontos}'
    #msg,serrilhado,cor
    texto_format = fonte.render(msg,True,('black')) 

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    if pygame.key.get_pressed()[K_a]:
        x-=speed
    if pygame.key.get_pressed()[K_d]:
        x+=speed
    if pygame.key.get_pressed()[K_w]:
        y-=speed
    if pygame.key.get_pressed()[K_s]:
        y+=speed

    rect = pygame.draw.rect(screen,(0,255,255),(x,y,50,50))
    rect2 = pygame.draw.rect(screen,(240, 127, 80),(x2,y2,30,30))

    if rect.colliderect(rect2):
        x2,y2= randint(0,WIDTH),randint(0,HEIGHT)
        pontos += 1
        colid_sound.play()

    if x == WIDTH:
        x=0
    elif x < -50:
        x=WIDTH
    elif y == HEIGHT:
        y=0
    elif y < -50:
        y=HEIGHT
    screen.blit(texto_format,(400,50)) #obj,posição
    pygame.display.update()