import pygame
import random
import sys
import math

# Inițializare Pygame
pygame.init()

# Configurații Ecran
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ajut-o pe doamna de info!")

# Culori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (200, 0, 0)
BLUE  = (50, 153, 213)
GOLD  = (255, 215, 0)

# Setări Joc
SNAKE_BLOCK = 20
SNAKE_SPEED = 10

font_style = pygame.font.SysFont("arial", 22)
score_font = pygame.font.SysFont("comicsansms", 25)
end_font = pygame.font.SysFont("arial", 24)


# --- Firework particle system ---
class Particle:
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(30, 60)
        self.color = color

    def update(self):
        self.vy += 0.12
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha = max(0, min(255, int(255 * (self.life / 60.0))))
        s = pygame.Surface((4, 4), pygame.SRCALPHA)
        s.fill((self.color[0], self.color[1], self.color[2], alpha))
        surface.blit(s, (int(self.x), int(self.y)))


class Firework:
    def __init__(self, x, y):
        self.particles = []
        colors = [
            (255, 69, 0), (255, 165, 0), (255, 215, 0),
            (0, 255, 127), (0, 191, 255), (65, 105, 225),
            (255, 105, 180)
        ]
        color = random.choice(colors)
        for _ in range(random.randint(20, 48)):
            self.particles.append(Particle(x, y, color))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

    def is_dead(self):
        return len(self.particles) == 0

# --- end firework system ---

def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    rect = mesg.get_rect(center=(WIDTH / 2, HEIGHT / 2 + y_offset))
    screen.blit(mesg, rect)


def draw_teacher(surface, x, y, block_size):
    cx = int(x + block_size / 2)
    cy = int(y + block_size / 2)
    head_radius = int(block_size * 0.45)
    skin = (255, 235, 205)
    hair = (245, 210, 80)
    shirt = (200, 100, 170)
    skirt = (150, 40, 100)
    hair_highlight = (255, 235, 140)
    glasses_color = (140, 140, 140)

    # head
    pygame.draw.circle(surface, skin, (cx, cy - 6), head_radius)
    # hair (longer sides, blonde)
    pygame.draw.ellipse(surface, hair, (cx - head_radius - 2, cy - head_radius - 12, head_radius*2+4, head_radius*2+8))
    pygame.draw.ellipse(surface, hair_highlight, (cx - head_radius//2, cy - head_radius - 8, head_radius+2, head_radius+4), 1)
    # eyes and smile
    pygame.draw.circle(surface, (0, 0, 0), (cx - 5, cy - 8), 2)
    pygame.draw.circle(surface, (0, 0, 0), (cx + 5, cy - 8), 2)
    pygame.draw.arc(surface, (150, 0, 0), (cx - 6, cy - 6, 12, 8), 3.14, 0, 1)
    # glasses
    pygame.draw.circle(surface, glasses_color, (cx - 5, cy - 8), 5, 1)
    pygame.draw.circle(surface, glasses_color, (cx + 5, cy - 8), 5, 1)
    pygame.draw.line(surface, glasses_color, (cx - 1, cy - 8), (cx + 1, cy - 8), 1)
    # body (dress)
    body_rect = (int(x), int(y) + int(block_size * 0.4), block_size, int(block_size * 0.8))
    pygame.draw.rect(surface, shirt, body_rect)
    # skirt (triangle)
    pygame.draw.polygon(surface, skirt, [(cx - int(block_size*0.45), cy + int(block_size*0.25)), (cx + int(block_size*0.45), cy + int(block_size*0.25)), (cx, cy + int(block_size*0.8))])
    # simple necklace
    pygame.draw.circle(surface, (255, 215, 0), (cx, cy + 2), 2)


def draw_diploma(surface, x, y, size):
    pad = 2
    paper_color = (245, 245, 220)
    border = (140, 110, 80)
    ribbon = (180, 20, 60)
    # main paper
    rect = pygame.Rect(int(x)+pad, int(y)+pad, int(size)-pad*2, int(size)-pad*2)
    pygame.draw.rect(surface, paper_color, rect)
    pygame.draw.rect(surface, border, rect, 2)
    # little seal / ribbon on right
    cx = rect.right - int(size*0.15)
    cy = rect.centery
    pygame.draw.circle(surface, ribbon, (cx, cy), int(size*0.18))
    # ribbon tails
    pygame.draw.polygon(surface, ribbon, [(cx-6, cy+6), (cx-2, cy+int(size*0.45)), (cx-12, cy+int(size*0.35))])
    pygame.draw.polygon(surface, ribbon, [(cx+6, cy+6), (cx+2, cy+int(size*0.45)), (cx+12, cy+int(size*0.35))])


def draw_classroom_background(surface):
    wall_color = (220, 220, 200)
    floor_color = (160, 140, 120)
    board_color = (40, 80, 40)
    desk_color = (170, 120, 70)
    chair_color = (120, 80, 50)
    shelf_color = (100, 70, 40)
    window_color = (180, 220, 255)
    glass_color = (210, 245, 255)

    # wall + floor
    surface.fill(wall_color)
    pygame.draw.rect(surface, floor_color, (0, HEIGHT * 0.65, WIDTH, HEIGHT * 0.35))

    # chalkboard
    pygame.draw.rect(surface, board_color, (60, 40, WIDTH - 120, 90))
    pygame.draw.rect(surface, (210, 210, 210), (60, 130, WIDTH - 120, 6))
    pygame.draw.line(surface, WHITE, (70, 55), (WIDTH - 70, 55), 2)
    pygame.draw.line(surface, WHITE, (70, 70), (WIDTH - 70, 70), 2)
    pygame.draw.line(surface, WHITE, (70, 85), (WIDTH - 70, 85), 2)
    pygame.draw.line(surface, WHITE, (70, 100), (WIDTH - 70, 100), 2)

    # windows
    pygame.draw.rect(surface, window_color, (WIDTH - 140, 150, 120, 90))
    pygame.draw.rect(surface, glass_color, (WIDTH - 135, 155, 110, 80))
    pygame.draw.line(surface, window_color, (WIDTH - 80, 150), (WIDTH - 80, 240), 3)
    pygame.draw.line(surface, window_color, (WIDTH - 140, 195), (WIDTH - 20, 195), 3)

    # bookshelf
    pygame.draw.rect(surface, shelf_color, (40, 150, 80, 140))
    for i in range(5):
        pygame.draw.line(surface, wall_color, (40, 170 + i * 25), (120, 170 + i * 25), 3)
    pygame.draw.rect(surface, (200, 90, 90), (50, 160, 20, 20))
    pygame.draw.rect(surface, (90, 180, 90), (80, 160, 20, 20))
    pygame.draw.rect(surface, (90, 90, 180), (50, 190, 20, 20))
    pygame.draw.rect(surface, (180, 180, 80), (80, 190, 20, 20))

    # benches and chairs
    bench_y = HEIGHT * 0.72
    for i in range(3):
        x = 100 + i * 140
        pygame.draw.rect(surface, desk_color, (x, bench_y, 100, 18))
        pygame.draw.rect(surface, chair_color, (x + 20, bench_y + 22, 22, 22))
        pygame.draw.rect(surface, chair_color, (x + 60, bench_y + 22, 22, 22))
        pygame.draw.rect(surface, (120, 120, 120), (x + 10, bench_y + 3, 80, 4))

    # poster or classroom decoration
    pygame.draw.rect(surface, (210, 210, 255), (WIDTH - 160, 260, 110, 80))
    pygame.draw.line(surface, (120, 120, 180), (WIDTH - 150, 280), (WIDTH - 80, 280), 3)
    pygame.draw.line(surface, (120, 120, 180), (WIDTH - 150, 295), (WIDTH - 100, 295), 3)
    pygame.draw.circle(surface, (255, 180, 0), (WIDTH - 90, 320), 10)


def game_loop():
    game_over = False
    game_close = False
    intro = True

    # Poziția de start
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1
    score = 0

    # Poziție diplomă
    foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
    foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0

    clock = pygame.time.Clock()

    while not game_over:

        # Ecran de Start
        while intro:
            screen.fill(BLACK)
            message("Ajut-o pe doamna de info sa găsească cele 10 diplome!", GOLD, -20)
            message("Apasă SPACE pentru a începe", WHITE, 30)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        intro = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        # Ecran Final (Mesaj Special) + fireworks
        fireworks = []
        fw_timer = 0
        while game_close:
            screen.fill((0, 255, 255))

            # spawn fireworks occasionally
            fw_timer += 1
            if fw_timer % 12 == 0 or random.random() < 0.06:
                fx = random.randint(60, WIDTH - 60)
                fy = random.randint(40, HEIGHT // 2)
                fireworks.append(Firework(fx, fy))

            # update and draw fireworks
            for fw in fireworks:
                fw.update()
                fw.draw(screen)
            fireworks = [fw for fw in fireworks if not fw.is_dead()]

            mesg = end_font.render("Va multumim pentru acesti ani frumosi! Ne va fi dor de dumneavoastra", True, WHITE)
            rect = mesg.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 15))
            screen.blit(mesg, rect)
            mesg2 = end_font.render("Press Q to close app", True, WHITE)
            rect2 = mesg2.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 25))
            screen.blit(mesg2, rect2)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    game_over = True
                    game_close = False

            clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # Trecerea prin pereți (Teleportare)
        if x1 >= WIDTH: x1 = 0
        elif x1 < 0: x1 = WIDTH - SNAKE_BLOCK
        if y1 >= HEIGHT: y1 = 0
        elif y1 < 0: y1 = HEIGHT - SNAKE_BLOCK

        x1 += x1_change
        y1 += y1_change
        draw_classroom_background(screen)

        # Desenare Diplomă
        draw_diploma(screen, foodx, foody, SNAKE_BLOCK)
        
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Desenare "Profesora" (Șarpele) - use teacher shape for all segments
        for segment in snake_list:
            draw_teacher(screen, segment[0], segment[1], SNAKE_BLOCK)

        # Afișare Scor
        value = score_font.render("Diplome: " + str(score), True, WHITE)
        screen.blit(value, [10, 10])

        pygame.display.update()

        # Verificare coliziune cu diploma
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
            foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0
            length_of_snake += 1
            score += 1

        # Condiția de final la scorul 10
        if score == 15:
            game_close = True

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    sys.exit()

game_loop()
