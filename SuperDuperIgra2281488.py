import pygame
#привет судьи тут я расскажу про свой проект который я создавал полтары недели
#и все комментарии сделаны не чатом джипити потому что я сам придумал такую идею
pygame.init()

WIDTH, HEIGHT = 800, 600 #это размер шедевро экрана(стандарт размер для пай гейма)
FPS = 60
#все цвета для моих уровней, персонажей, и зомби пупсов(кроме ромы)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
DARK_RED = (139, 0, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)
DARK_GREEN = (0, 100, 0)
GRAY = (169, 169, 169)
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
DARK_BLUE = (0, 0, 139)
DARKER_GREEN = (0, 50, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
#мой гейрой
sudii = {
    "1": {"speed": 3, "health": 1, "damage": 999999999999999999999999999999999}
}

zombie_base_speed = 2
zombie_base_health = 3
zombie_spawn_delay = 0
projectile_speed = 7
projectiles = []
direction = "RIGHT"

kills = 0
npc_appeared = False
in_dungeon = False
paused = False
archmage_appeared = False
special_zombie = False
#создание фона моей шедеврогиперультрамегасупердуперкрутой игры
def create_gradient_background():
    gradient_surface = pygame.Surface((WIDTH, HEIGHT))
    for i in range(HEIGHT):
        ratio = i / HEIGHT
        color = (
            int(SKY_BLUE[0] * (1 - ratio) + DARK_BLUE[0] * ratio),
            int(SKY_BLUE[1] * (1 - ratio) + DARK_BLUE[1] * ratio),
            int(SKY_BLUE[2] * (1 - ratio) + DARK_BLUE[2] * ratio),
        )
        pygame.draw.line(gradient_surface, color, (0, i), (WIDTH, i))
    return gradient_surface

def draw_gradient_background(surface, background_surface):
    surface.blit(background_surface, (0, 0))
#самое худшее из худших в пай гейме. Я не смог вставить картинку тупую и делал вручную через координаты/позиции
def draw_mage(surface, x, y, color=RED):
    pygame.draw.rect(surface, color, (x + 10, y + 30, 30, 40))
    pygame.draw.rect(surface, DARK_RED, (x + 10, y + 30, 30, 10))
    pygame.draw.rect(surface, color, (x + 17, y + 55, 16, 15))
    pygame.draw.rect(surface, GOLD, (x + 10, y + 60, 30, 5))
    pygame.draw.circle(surface, color, (x + 25, y + 20), 15)
    pygame.draw.circle(surface, BLACK, (x + 25, y + 20), 12)
    pygame.draw.line(surface, color, (x + 10, y + 35), (x, y + 45), 5)
    pygame.draw.line(surface, color, (x + 40, y + 35), (x + 50, y + 45), 5)
    pygame.draw.line(surface, GOLD, (x + 50, y + 45), (x + 50, y + 10), 4)
    pygame.draw.circle(surface, BLUE, (x + 50, y + 10), 6)
    pygame.draw.circle(surface, YELLOW, (x + 50, y + 10), 3)
    pygame.draw.polygon(surface, color, [(x + 10, y + 10), (x + 25, y - 20), (x + 40, y + 10)])
    pygame.draw.line(surface, GOLD, (x + 10, y + 10), (x + 40, y + 10), 3)

def draw_zombie(surface, x, y, special=False):
    pygame.draw.rect(surface, GREEN, (x + 10, y + 30, 30, 40))
    pygame.draw.rect(surface, DARK_GREEN, (x + 10, y + 50, 30, 20))
    pygame.draw.rect(surface, GREEN, (x + 15, y + 10, 20, 20))
    pygame.draw.rect(surface, DARK_GREEN, (x + 15, y + 10, 20, 8))
    pygame.draw.rect(surface, BLACK, (x + 20, y + 15, 5, 5))
    pygame.draw.rect(surface, BLACK, (x + 30, y + 15, 5, 5))
    pygame.draw.line(surface, GRAY, (x + 10, y + 40), (x - 5, y + 45), 5)
    pygame.draw.line(surface, GRAY, (x + 40, y + 40), (x + 55, y + 45), 5)
    if special: #пасхалочка (надеюсь ромы в судьях нету)
        font = pygame.font.Font(None, 24)
        name_text = font.render("Роблоксер Рома", True, WHITE)
        surface.blit(name_text, (x - 20, y - 20))
#хп мои и только мои
def draw_health(surface, health):
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Health: {health}", True, WHITE)
    surface.blit(health_text, (10, HEIGHT - 40))
#количевство моих убитых зомборей
def draw_kills(surface, kills):
    font = pygame.font.Font(None, 36)
    kills_text = font.render(f"Kills: {kills}", True, WHITE)
    surface.blit(kills_text, (WIDTH - 150, HEIGHT - 40))

def draw_dialogue_box(surface, text):
    font = pygame.font.Font(None, 36)
    box_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, HEIGHT // 4)
    pygame.draw.rect(surface, DARK_RED, box_rect)
    pygame.draw.rect(surface, GOLD, box_rect, 3)
    lines = text.split("\n")
    for i, line in enumerate(lines): #для Кости скажу что бы не было притензий енумерейт это счетчик если вкратце
        dialogue_text = font.render(line, True, WHITE)
        surface.blit(dialogue_text, (box_rect.x + 10, box_rect.y + 10 + i * 30))
    pygame.display.flip()
#второй этап игры где шедевро волшебник говорит нам что бы мы пошли в данж
def handle_npc_interaction():
    global in_dungeon
    dialogue_text = "Привет, ты достиг хорошего лвл.\nПоэтому пошли в данж.\n\n1. Пойти в данж\n2. Остаться"
    draw_dialogue_box(screen, dialogue_text)
    pygame.time.wait(1000)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    in_dungeon = True
                    return
                if event.key == pygame.K_2:
                    return
#переход на концовки с помощью архимагов
def handle_archmage_interaction(white_mage):
    draw_dialogue_box(screen, "Ты достиг максимального уровня.\nТеперь ты можешь пойти в сообщество архимагов.\n\n1. Принять\n2. Отказаться")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if white_mage: #переход в стадию джедая пупса
                        screen.fill(WHITE)
                        pygame.display.flip()
                        pygame.time.wait(3000)
                        screen.fill(BLACK)
                        font = pygame.font.Font(None, 72)
                        end_text = font.render("Вы стали прекрасным джедаем", True, WHITE)
                        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2))
                        pygame.display.flip()
                        pygame.time.wait(3000)
                    else:
                        # Переход в стадию ситха ромы
                        screen.fill(BLACK)
                        pygame.display.flip()
                        pygame.time.wait(3000)
                        screen.fill(RED)
                        font = pygame.font.Font(None, 72)
                        end_text = font.render("Вы выбрали путь ситхов", True, BLACK)
                        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2))
                        pygame.display.flip()
                        pygame.time.wait(3000)
                    return
#пауза что бы сходить в туалет
def handle_pause():
    font = pygame.font.Font(None, 72)
    paused_text = font.render("Paused", True, WHITE)
    screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2 - paused_text.get_height() // 2))
    pygame.display.flip()
#и основная игра которую я создавал 3-4 дня
def start_game(hero_key):
    global kills, paused, npc_appeared, archmage_appeared, in_dungeon, projectiles, special_zombie
    player = pygame.Rect(400, 300, 50, 70)
    speed = sudii[hero_key]["speed"]
    health = sudii[hero_key]["health"]
    damage = sudii[hero_key]["damage"]

    enemy = pygame.Rect(500, 100, 50, 70)
    enemy_alive = True
    enemy_level = 1
    enemy_health = zombie_base_health

    npc = pygame.Rect(200, 300, 50, 70)
    white_mage = pygame.Rect(100, 100, 50, 70)
    black_mage = pygame.Rect(600, 100, 50, 70)

    last_zombie_spawn_time = pygame.time.get_ticks()
    gradient_background = create_gradient_background()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        handle_pause()
                if event.key == pygame.K_SPACE:
                    projectile_rect = pygame.Rect(player.x + 25, player.y + 25, 10, 10)
                    projectiles.append({"rect": projectile_rect, "direction": direction}) #есть предупреждение но не ломает игру)))

        if paused:
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= speed
            direction = "LEFT"
        if keys[pygame.K_RIGHT]:
            player.x += speed
            direction = "RIGHT"
        if keys[pygame.K_UP]:
            player.y -= speed
            direction = "UP"
        if keys[pygame.K_DOWN]:
            player.y += speed
            direction = "DOWN"

        for projectile in projectiles[:]:
            if projectile["direction"] == "RIGHT":
                projectile["rect"].x += projectile_speed
            elif projectile["direction"] == "LEFT":
                projectile["rect"].x -= projectile_speed
            elif projectile["direction"] == "UP":
                projectile["rect"].y -= projectile_speed
            elif projectile["direction"] == "DOWN":
                projectile["rect"].y += projectile_speed

            if projectile["rect"].colliderect(enemy) and enemy_alive:
                enemy_health -= damage
                projectiles.remove(projectile)
                if enemy_health <= 0:
                    enemy_alive = False
                    kills += 1
                    if kills % 5 == 0:
                        damage += 1
                    if kills % 10 == 0:
                        special_zombie = True
                    else:
                        special_zombie = False
                    if kills == 30:
                        npc_appeared = True
                    if kills == 100:
                        archmage_appeared = True

        if enemy_alive:
            if player.colliderect(enemy):
                health -= 1
                if health <= 0:
                    return
            enemy.x += zombie_base_speed
            if enemy.x > WIDTH:
                enemy.x = 0
        else:
            if pygame.time.get_ticks() - last_zombie_spawn_time >= zombie_spawn_delay:
                enemy_level += 1
                enemy_health = zombie_base_health + enemy_level
                enemy_alive = True
                last_zombie_spawn_time = pygame.time.get_ticks()

        if npc_appeared and player.colliderect(npc):
            handle_npc_interaction()
            npc_appeared = False

        if archmage_appeared and in_dungeon:
            if player.colliderect(white_mage):
                handle_archmage_interaction(white_mage=True)
                return
            if player.colliderect(black_mage):
                handle_archmage_interaction(white_mage=False)
                return

        if in_dungeon:
            screen.fill(DARKER_GREEN)
            if archmage_appeared:
                draw_mage(screen, white_mage.x, white_mage.y, color=WHITE)
                draw_mage(screen, black_mage.x, black_mage.y, color=BLACK)
        else:
            draw_gradient_background(screen, gradient_background)

        draw_mage(screen, player.x, player.y)
        if enemy_alive:
            draw_zombie(screen, enemy.x, enemy.y, special=special_zombie)
        for projectile in projectiles:
            pygame.draw.circle(screen, BLUE, (projectile["rect"].x, projectile["rect"].y), 5)
        draw_health(screen, health)
        draw_kills(screen, kills)

        if npc_appeared:
            draw_mage(screen, npc.x, npc.y, color=BLUE)

        pygame.display.flip()

def main_menu():
    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 72)
        title_text = font.render("My Game", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        font = pygame.font.Font(None, 48)
        start_text = font.render("Press ENTER to Start", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))

        quit_text = font.render("Press ESC to Quit", True, WHITE)
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

while True:
    main_menu()
    hero_key = "1"
    start_game(hero_key)
#и сделаю предсказания судей: Констянтин: думаю неплохо как для человека что тупит над любой задачей но игра пиксельная - 1 балл
#Дмитро Деметєєв: структура фиговая, игра пиксельная - 0  баллов
#Яцура Андрій (приятного аппетита кстате): нуууууууууууууууууууууууууууууууууууууууууууу норм но структуры нету нормальной - 0.3333333333334 баллов
#Сусло Валентина: ничего не предскажу - -10 баллов
#ну остальных я не особо знаю поэтому только скажу что я слил 100 процентов а ну и приятного аппетита кто кушает
#ну и по подсчетом я получаю +- нифига и всем пока
#а этот комментарий я делаю только из-за того что я суверщик и люблю не четное количевство