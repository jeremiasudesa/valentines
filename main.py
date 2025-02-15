import pygame
import sys
import random

pygame.init()

clock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Valentine's Pygame")

pygame.mixer.music.load("assets/background_music.mp3")
pygame.mixer.music.play(-1)

def load_animation(sheet, row, frame_width, frame_height, num_frames, scale_factor=1):
    frames = []
    for i in range(num_frames):
        rect = pygame.Rect(i * frame_width, row * frame_height, frame_width, frame_height)
        frame = sheet.subsurface(rect)
        if scale_factor != 1:
            frame = pygame.transform.scale(frame, (int(frame_width * scale_factor), int(frame_height * scale_factor)))
        frames.append(frame)
    return frames

sprite_sheet = pygame.image.load("assets/sprite_sheet.png").convert_alpha()
SCALE_FACTOR = 2.5
running_right_images = load_animation(sprite_sheet, 3, 80, 64, 8, SCALE_FACTOR)
running_left_images = load_animation(sprite_sheet, 8, 80, 64, 8, SCALE_FACTOR)
standing_right_images = load_animation(sprite_sheet, 0, 80, 64, 10, SCALE_FACTOR)
standing_left_images = load_animation(sprite_sheet, 5, 80, 64, 10, SCALE_FACTOR)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y - 10
        self.vx = 0
        self.speed = 2
        self.state = "stand_right"
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_delay = 120

    def update(self, dt):
        self.x += self.vx * self.speed * (dt / 1000)
        frames = self.get_current_frames()
        if frames:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_delay:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % len(frames)

    def get_current_frames(self):
        return {
            "run_right": running_right_images,
            "run_left": running_left_images,
            "stand_right": standing_right_images,
            "stand_left": standing_left_images
        }.get(self.state, standing_right_images)

    def get_current_image(self):
        frames = self.get_current_frames()
        return frames[self.anim_index] if frames else pygame.Surface((80, 64), pygame.SRCALPHA)

    def draw(self, surface, camera_x):
        surface.blit(self.get_current_image(), (self.x - camera_x, self.y))

heart_image = pygame.image.load("assets/heart.png").convert_alpha()

class Heart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = random.uniform(50, 150)
        self.vx = random.uniform(-30, 30)
        scale = random.uniform(0.5, 1.5)
        self.image = pygame.transform.scale(heart_image, (int(heart_image.get_width() * scale), int(heart_image.get_height() * scale)))

    def update(self, dt):
        self.y += self.vy * (dt / 1000)
        self.x += self.vx * (dt / 1000)

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.x - camera_x, self.y))

hearts = []
heart_spawn_timer = 0

def pseudo_random(x):
    x = int(x)
    x = (x << 13) ^ x
    return ((x * (x * x * 15731 + 789221) + 1376312589) & 0x7fffffff) / 0x7fffffff

pygame.font.init()
available_fonts = pygame.font.get_fonts()
preferred_fonts = ["brushscriptmt", "papyrus", "comicsansms", "scriptina", "algerian", "mistral"]
selected_font = None

for font_name in preferred_fonts:
    if font_name in available_fonts:
        selected_font = font_name
        break

if selected_font:
    font = pygame.font.SysFont(selected_font, 100)
else:
    font = pygame.font.Font(None, 100)
    font.set_bold(True)
    font.set_italic(True)

text = font.render("para mari", True, (238, 75, 43))
text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))

start_screen = True
while start_screen:
    screen.fill((255, 223, 226))
    screen.blit(text, text_rect)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            start_screen = False

    clock.tick(60)

messages = [
    "",
    "puedo galopar las praderas",
    "bajo cielos azules",
    "a través de montañas imponentes",
    "cruzando desiertos solitarios",
    "y nunca encontrar alguien como vos"
]

message_timer = 0
current_message_index = 0
message_font = pygame.font.Font(None, 50)
message_color = (255, 255, 255) 

placeholder_image = pygame.Surface((WIDTH, HEIGHT))
placeholder_image.fill((255, 223, 226))  
final_text = font.render("te amo chiqui", True, (238, 75, 43))  
final_text_rect = final_text.get_rect(center=(WIDTH//2, HEIGHT//2))

running = True
player = Player(WIDTH // 2, HEIGHT - 150)
show_picture = False

while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.vx = -1
                player.state = "run_left"
            elif event.key == pygame.K_RIGHT:
                player.vx = 1
                player.state = "run_right"
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.vx = 0
                player.state = "stand_left" if player.state == "run_left" else "stand_right"
                player.anim_index = 0

    player.update(dt)
    camera_x = player.x + player.get_current_image().get_width() // 2 - WIDTH // 2

    heart_spawn_timer += dt
    if heart_spawn_timer >= 1000:
        heart_spawn_timer = 0
        spawn_x = random.uniform(camera_x - 100, camera_x + WIDTH + 100)
        spawn_y = random.uniform(-150, -10)
        hearts.append(Heart(spawn_x, spawn_y))
    hearts = [heart for heart in hearts if heart.y < HEIGHT + 100]

    for heart in hearts:
        heart.update(dt)

    screen.fill((135, 206, 235))
    
    for heart in hearts:
        heart.draw(screen, camera_x)

    ground_y = HEIGHT - 50
    num_segments = 100
    segment_width = WIDTH / num_segments
    points = []
    for i in range(num_segments + 1):
        world_x = camera_x + i * segment_width
        noise = pseudo_random(world_x) * 10 - 5
        screen_x = i * segment_width
        points.append((screen_x, ground_y + noise))
    pygame.draw.polygon(screen, (34, 139, 34), points + [(WIDTH, HEIGHT), (0, HEIGHT)])
    pygame.draw.lines(screen, (0, 100, 0), False, points, 3)
    
    player.draw(screen, camera_x)

    if not show_picture:
        message_timer += dt
        if message_timer >= 10000:  
            message_timer = 0
            current_message_index += 1
            if current_message_index >= len(messages):
                show_picture = True

        if current_message_index < len(messages):
            message_surface = message_font.render(messages[current_message_index], True, message_color)
            message_rect = message_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(message_surface, message_rect)

    if show_picture:
        screen.blit(placeholder_image, (0, 0))
        screen.blit(final_text, final_text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()