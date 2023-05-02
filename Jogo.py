import pygame

pygame.init()

# 设置屏幕大小
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置窗口标题
pygame.display.set_caption("游戏开始界面")

# 加载背景图片
background_img = pygame.image.load("background1.jpg").convert_alpha()

# 加载开始按钮图片
start_btn_img = pygame.image.load("background1.jpg").convert_alpha()
start_btn_width = start_btn_img.get_width()
start_btn_height = start_btn_img.get_height()

# 设置开始按钮位置
start_btn_x = screen_width // 2 - start_btn_width // 2
start_btn_y = screen_height // 2 - start_btn_height // 2

# 游戏主循环
while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 点击窗口的关闭按钮退出游戏
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # 如果鼠标点击了开始按钮，跳转到游戏界面
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if start_btn_x <= mouse_x <= start_btn_x + start_btn_width and \
                    start_btn_y <= mouse_y <= start_btn_y + start_btn_height:
                    start_btn_img = pygame.image.load("background1.jpg").convert_alpha()                                # TODO: 跳转到游戏界面
    screen.blit(background_img, (0, 0))
    # 绘制开始按钮
    screen.blit(start_btn_img, (start_btn_x, start_btn_y))

    # 更新屏幕
    pygame.display.update()
