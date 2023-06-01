import pygame
import sys
import random
import os

#Configuração inicial
diretorio_principal = os.path.dirname(__file__)  #caminho absoluto do script
diretorio_personagem = os.path.join(diretorio_principal,'spritesheet')
diretorio_sprites = os.path.join(diretorio_principal,'sprites')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

# 初始化Pygame
pygame.init()

# 窗口尺寸
LARGURA = 900
ALTURA = 740
TELA = pygame.display.set_mode((LARGURA, ALTURA))

# 创建窗口
window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("游戏开始界面")

# 背景音乐
pygame.mixer.music.load("sons/bgm.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)  # 循环播放背景音乐

# 字体设置
selected_font = pygame.font.Font("fonts/vazio.ttf", 50)
selected_font.set_bold(True)
unselected_font = pygame.font.Font("fonts/cheio.ttf", 50)
poit_font = pygame.font.Font("fonts/cheio.ttf", 15)

# 选项列表
options = ["START", "RANK", "SOUND", "QUIT"]
selected_option = 0

# 游戏是否开启音效
sound_enabled = True

# 游戏开始界面类
class StartMenu:
    def __init__(self):
        self.pontuacao = 0
        self.background = pygame.image.load("backgrounds/back1.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background,(LARGURA,ALTURA))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.select_option((selected_option - 1) % len(options))
            elif event.key == pygame.K_DOWN:
                self.select_option((selected_option + 1) % len(options))
            elif event.key == pygame.K_RETURN:
                self.execute_option(selected_option)

    def select_option(self, option):
        global selected_option
        selected_option = option

    def execute_option(self, option):
        if option == 0:
            game = Game()
            game.start()
        elif option == 1:
            rank = Rank()
            rank.show()
        elif option == 2:
            self.toggle_sound()
        elif option == 3:
            pygame.quit()
            sys.exit()

    def toggle_sound(self):
        global sound_enabled
        sound_enabled = not sound_enabled
        if sound_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def draw(self, window):
        window.blit(self.background,(0, 0))

        for i, option in enumerate(options):
            if i == selected_option:
                text_surface = selected_font.render(option, True, (0,0,0))
            else:
                text_surface = unselected_font.render(option, True, (0,0,0))

            text_rect = text_surface.get_rect()
            text_rect.center = (LARGURA / 2, 200 + i * 80)
            window.blit(text_surface, text_rect)

        pygame.display.flip()

class Protagonista(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #Vida do personagem
        self.sprite_protagonista = pygame.image.load('spritesheet/andar.png').convert_alpha()
        self.vida = 5
        self.pontuacao = 0
        self.coracao_img = pygame.image.load("sprites/coracao.png").convert_alpha()
        self.coracao_img = pygame.transform.scale(self.coracao_img,(40,40)) 
        self.coracao_rect = self.coracao_img.get_rect()
        self.coracao_x = 10
        self.coracao_y = 10
        self.espaco_coracao = 40
        self.tela = TELA

        #variáveis do pulo
        self.vel_y = 0
        self.is_jumping = False
        self.jump_start_time = 0
        self.JUMP_HEIGHT = -10
        self.MAX_JUMP_TIME = 40  # Tempo máximo de salto em milissegundos
        self.GRAVITY = 0.8
        
        #variáveis do andamento
        self.andamento = False

        #som do pulo
        self.som_pulo = pygame.mixer.Sound('sons/jump.wav')
        self.som_pulo.set_volume(1)
        
        #animação
        self.imagens_protagonista = []
        for i in range(6):
            img = self.sprite_protagonista.subsurface((i * 87, 0), (87, 160)) #usar spritesheet
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
        self.som_pulo.play()
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

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/boss.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(100,100))
        self.image = pygame.transform.rotate(self.image, 50)
        self.rect = self.image.get_rect(x=LARGURA-150,y=70)

    def update(self):
        pass

class Mapa(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("backgrounds/back2.png").convert()
        self.image = pygame.transform.scale(self.image,(LARGURA*2,ALTURA)) #mudar tamanho de cada sprite
        self.rect = self.image.get_rect(x=0,y=0)

    def update(self):
        if self.rect.x < -LARGURA:
            self.rect.x = 0
        self.rect.x -= 3

class Fireball(pygame.sprite.Sprite):
    def __init__(self,obj):
        pygame.sprite.Sprite.__init__(self)
        self.obj = obj
        self.image = pygame.image.load("sprites/fireball.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(60,30)) #mudar tamanho de cada sprite
        self.image = pygame.transform.rotate(self.image,180)
        self.pos_init = random.randrange(50,ALTURA-100)
        self.velocidade = random.randrange(2,7)
        self.rect = self.image.get_rect(x=LARGURA,y=self.pos_init)
        self.rect.y = random.randrange(50,ALTURA-100)
    
    def voltar(self):
        self.rect.x = LARGURA
        self.rect.y= random.randrange(0,ALTURA-70)
        self.velocidade = random.randrange(2,7)

    def update(self):
        if self.rect.topright[0] < 0:
            self.voltar()
        elif self.rect.colliderect(self.obj):
            self.voltar()
            self.obj.vida -= 1
            self.obj.pontuacao -= 200
            self.obj.image = pygame.image.load("spritesheet/sofrer.png").convert_alpha()
            self.obj.image = pygame.transform.scale(self.obj.image,(30,60))
            pygame.mixer.Sound("sons/fireball.wav").play()
        self.rect.x -= self.velocidade

class Food(pygame.sprite.Sprite):
    def __init__(self,obj):
        pygame.sprite.Sprite.__init__(self)
        self.obj = obj
        self.image = pygame.image.load("sprites/food.png").convert_alpha()
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
        elif self.rect.colliderect(self.obj):
            self.voltar()
            self.obj.vida += 1
            self.obj.pontuacao += 300
            pygame.mixer.Sound("sons/food.wav").play()
        self.rect.x -= self.velocidade
# Game
class Game:
    def __init__(self):
        #iniciação dos sprites
        self.over = False
        self.todas_sprites = pygame.sprite.Group()
        self.background = pygame.image.load("backgrounds/back1.jpg").convert()
        self.protagonista = Protagonista()
        self.boss = Boss()
        self.mapa = Mapa()
        self.pontos = poit_font.render("Pontos:{}".format(self.protagonista.pontuacao), False, (0, 0, 0))
        self.todas_sprites.add(self.mapa, self.protagonista,self.boss)
        for i in range(6):
            fireball = Fireball(self.protagonista)
            self.todas_sprites.add(fireball)

        for i in range(5):
            food = Food(self.protagonista)
            self.todas_sprites.add(food)

    def update(self):
        self.pontos = poit_font.render("Pontos:{}".format(self.protagonista.pontuacao), False, (0, 0, 0))
        self.protagonista.movimentar()
        self.todas_sprites.update()
        if self.protagonista.vida <= 0:
            self.over = True

    def draw(self):
        if self.over == False:
            self.game()
        if self.over == True:
            self.gameOver()

    def game(self):
        self.todas_sprites.draw(TELA)
        TELA.blit(self.pontos, (LARGURA-180, 20))
        for i in range(self.protagonista.vida):
            self.coracao_rect = self.protagonista.coracao_img.get_rect()
            self.protagonista.coracao_rect.x = self.protagonista.coracao_x + i * self.protagonista.espaco_coracao
            self.protagonista.coracao_rect.y = self.protagonista.coracao_y
            TELA.blit(self.protagonista.coracao_img, self.protagonista.coracao_rect)
        pygame.display.flip()

    def gameOver(self):
        gameover_text = unselected_font.render("GAME OVER", False, (255, 255, 255))
        restart_text = poit_font.render("Press Enter to reset", False, (255, 255, 255))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.protagonista.vida = 5
                        self.over = False
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            TELA.fill((0, 0, 0))
            TELA.blit(gameover_text, (290, 300))
            TELA.blit(restart_text, (340, 380))
            pygame.display.flip()

    def start(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.protagonista.pular()
            self.update()
            self.draw()
            clock.tick(60)

class GameOver():
    def __init__(self):
        self.gameover = unselected_font.render("GAME OVER",False,(255,255,255))
        self.reinciar = poit_font.render("Press Enter para to reset",False,(255,255,255))
    def gameover(self):
        TELA.fill(0,0,0)
        TELA.blit(self.gameover,(500,ALTURA/2))
        TELA.blit(self.reinciar,(500,ALTURA/2+100))

#Rank
class Rank:
    def __init__(self):
        pass

    def show(self):
        print("Ranking")


# StartMenu
start_menu = StartMenu()
game_started = True

#Looping
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_started:
            start_menu.handle_event(event)
            
    if game_started:
        start_menu.draw(window)
        
    else:
        start_menu.execute_option(0)
