import pygame
import sys
import random

# Инициализация
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

# Загрузка изображений
racket = pygame.image.load("racket.png")
ball = pygame.image.load("tennis_ball.png")
life_icon = pygame.image.load("tennis_ball.png")

# Размеры и начальные позиции
racket_width, racket_height = racket.get_size()
ball_width, ball_height = ball.get_size()

racket1_x, racket1_y = 20, (HEIGHT - racket_height) // 2
racket2_x, racket2_y = WIDTH - racket_width - 20, (HEIGHT - racket_height) // 2
ball_x, ball_y = (WIDTH - ball_width) // 2, (HEIGHT - ball_height) // 2
ball_speed_x, ball_speed_y = 4, 4

# Жизни игроков
player1_lives = 3
player2_lives = 3

# Счет игроков
player1_score = 0
player2_score = 0

# Уязвимость бота
bot_delay = 0  # Счетчик задержки
bot_mistake_chance = 0.1  # Шанс бота двигаться неправильно

clock = pygame.time.Clock()

# Функция отображения жизней
def draw_lives(lives, x, y):
    for i in range(lives):
        screen.blit(life_icon, (x + i * (ball_width + 5), y))

# Функция отображения счета
def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Бот: {player1_score}  Игрок: {player2_score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Логика движения бота (Игрок 1)
    bot_delay += 1
    if bot_delay > 0:  # Задержка в движении
        if random.random() > bot_mistake_chance:  # Шанс сделать неправильное движение
            if racket1_y + racket_height // 2 < ball_y:
                racket1_y += 4
            elif racket1_y + racket_height // 2 > ball_y:
                racket1_y -= 4
        else:
            # Ошибка: бот движется в неправильном направлении
            if racket1_y + racket_height // 2 < ball_y:
                racket1_y -= 4
            elif racket1_y + racket_height // 2 > ball_y:
                racket1_y += 4
        bot_delay = 0  # Сброс задержки

    # Управление ракеткой игрока 2
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and racket2_y > 0:
        racket2_y -= 6
    if keys[pygame.K_DOWN] and racket2_y < HEIGHT - racket_height:
        racket2_y += 6

    # Движение шарика
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Отскоки от стен
    if ball_y <= 0 or ball_y >= HEIGHT - ball_height:
        ball_speed_y = -ball_speed_y

    # Отскоки от ракеток
    if (ball_x <= racket1_x + racket_width and 
        racket1_y < ball_y + ball_height < racket1_y + racket_height):
        ball_x = racket1_x + racket_width  # Отталкивание мяча от ракетки
        ball_speed_x = abs(ball_speed_x)  # Направление вправо
        player1_score += 1  # Бот отбил мяч

    if (ball_x + ball_width >= racket2_x and 
        racket2_y < ball_y + ball_height < racket2_y + racket_height):
        ball_x = racket2_x - ball_width  # Отталкивание мяча от ракетки
        ball_speed_x = -abs(ball_speed_x)  # Направление влево
        player2_score += 1  # Игрок отбил мяч

    # Проверка выхода за пределы
    if ball_x < 0:  # Игрок 1 пропустил мяч
        player1_lives -= 1
        ball_x, ball_y = (WIDTH - ball_width) // 2, (HEIGHT - ball_height) // 2
        ball_speed_x = random.choice([-4, 4])
        ball_speed_y = random.choice([-4, 4])
    if ball_x > WIDTH:  # Игрок 2 пропустил мяч
        player2_lives -= 1
        ball_x, ball_y = (WIDTH - ball_width) // 2, (HEIGHT - ball_height) // 2
        ball_speed_x = random.choice([-4, 4])
        ball_speed_y = random.choice([-4, 4])

    # Проверка завершения игры
    if player1_lives == 0 or player2_lives == 0:
        winner = "Бот" if player2_lives == 0 else "Игрок"
        font = pygame.font.Font(None, 74)
        result_text = font.render(f"{winner} победил!", True, (255, 255, 255))
        final_score_text = font.render(f"Счет —  Бот: {player1_score} | Игрок: {player2_score}", True, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()
        pygame.time.wait(5000)
        pygame.quit()
        sys.exit()

    # Рендеринг
    screen.fill((0, 0, 0))
    screen.blit(racket, (racket1_x, racket1_y))
    screen.blit(racket, (racket2_x, racket2_y))
    screen.blit(ball, (ball_x, ball_y))

    # Отображение жизней и счета
    draw_lives(player1_lives, 20, 20)
    draw_lives(player2_lives, WIDTH - 20 - 3 * (ball_width + 5), 20)
    draw_score()

    pygame.display.flip()
    clock.tick(60)




