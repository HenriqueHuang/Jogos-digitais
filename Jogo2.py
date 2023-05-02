import pygame

pygame.init()

# 设置游戏窗口大小和标题
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("游戏开始界面")

# 加载背景图像并调整大小以填充整个屏幕
background_image = pygame.image.load("background1.jpg")
background_image = pygame.transform.scale(background_image, (800, 600))

# 设置字体和按钮颜色
font = pygame.font.SysFont("Helvetica", 35)
button_color = (255, 255, 255)
hover_color = (200, 200, 200)

# 设置开始游戏按钮
start_button = pygame.Rect(300, 200, 200, 50)
start_text = font.render("Start", True, (255, 0, 0))

# 设置设置按钮
settings_button = pygame.Rect(300, 300, 200, 50)
settings_text = font.render("Configure", True, (0, 255, 0))

# 设置退出按钮
quit_button = pygame.Rect(300, 400, 200, 50)
quit_text = font.render("Quit", True, (0, 0, 255))

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取鼠标位置
    mouse_pos = pygame.mouse.get_pos()

    # 判断鼠标是否在按钮上方
    
    start_hovered = start_button.collidepoint(mouse_pos)
    settings_hovered = settings_button.collidepoint(mouse_pos)
    quit_hovered = quit_button.collidepoint(mouse_pos)

    # 判断是否应该更改按钮颜色
    if start_hovered:
        start_color = hover_color
    else:
        start_color = button_color

    if settings_hovered:
        settings_color = hover_color
    else:
        settings_color = button_color

    if quit_hovered:
        quit_color = hover_color
    else:
        quit_color = button_color

    # 绘制背景和按钮
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, start_color, start_button)
    pygame.draw.rect(screen, settings_color, settings_button)
    pygame.draw.rect(screen, quit_color, quit_button)

    # 绘制文字
    screen.blit(start_text, (320, 210))
    screen.blit(settings_text, (330, 310))
    screen.blit(quit_text, (340, 410))

    # 更新屏幕显示
    pygame.display.update()

pygame.quit()