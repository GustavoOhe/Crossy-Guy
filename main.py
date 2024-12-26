import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crossy Guy")

# Load backgrounds
backgrounds = [
   {"type": "road", "image": pygame.image.load("1.png")},
   {"type": "track and road", "image": pygame.image.load("3.png")},
   {"type": "long road", "image": pygame.image.load("2.png")},
]

for bg in backgrounds:
   bg["image"] = pygame.transform.scale(bg["image"], (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load player and obstacles
player_image = pygame.image.load("chillguy.png").convert_alpha()
player_image = pygame.transform.smoothscale(player_image, (70, 110))
carleft_image = pygame.image.load("carleft.png").convert_alpha()
carleft_image = pygame.transform.scale(carleft_image, (140, 80))
train_image = pygame.image.load("train.png").convert_alpha()
train_image = pygame.transform.scale(train_image, (400, 60))
deer_image = pygame.image.load("deer.png").convert_alpha()
deer_image = pygame.transform.scale(deer_image, (130, 180))

# Player setup
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 100
player_speed = 15

# Obstacles setup
carleft = []
train = []
deer = {}

# Current background index
current_bg = 0

# Level and score
level = 0
score = 0

# Game state
game_over = False

# Spawn obstacles for the current background
def spawn_obstacles(bg_type):
   global carleft, train, deer
   carleft = []
   train = []
   deer = {}

   if bg_type == "road":
       carleft = [{"x": SCREEN_WIDTH, "y": 600, "speed": 7},
                  {"x": SCREEN_WIDTH + 200, "y": 360, "speed": 7},
                  {"x": SCREEN_WIDTH + 200, "y": 150, "speed": 7}]
   elif bg_type == "track and road":
       train = [{"x": SCREEN_WIDTH, "y": 360, "speed": 15}]
       carleft = [{"x": SCREEN_WIDTH, "y": 560, "speed": 7},
                  {"x": SCREEN_WIDTH + 200, "y": 150, "speed": 7}]
   elif bg_type == "long road":
       deer = {"x": SCREEN_WIDTH // 2, "y": 400,
               "speed": 8, "direction": 1}

# Check pixel-perfect collision
def check_obstacle_collision(player_x, player_y, player_image, obstacles, obstacle_image):
   player_mask = pygame.mask.from_surface(player_image)
   obstacle_mask = pygame.mask.from_surface(obstacle_image)

   for obstacle in obstacles:
       offset = (int(obstacle["x"] - player_x), int(obstacle["y"] - player_y))
       if player_mask.overlap(obstacle_mask, offset):
           return True
   return False

def check_deer_collision(player_x, player_y, player_image, deer):
   if deer:
       player_mask = pygame.mask.from_surface(player_image)
       deer_mask = pygame.mask.from_surface(deer_image)
       offset = (int(deer["x"] - player_x), int(deer["y"] - player_y))
       if player_mask.overlap(deer_mask, offset):
           return True
   return False

# Restart game logic
def restart_game():
   global player_x, player_y, level, score, current_bg, game_over
   player_x = SCREEN_WIDTH // 2
   player_y = SCREEN_HEIGHT - 100
   level = 0
   score = 0
   current_bg = 0
   game_over = False
   spawn_obstacles(backgrounds[current_bg]["type"])

# Spawn initial obstacles
spawn_obstacles(backgrounds[current_bg]["type"])

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
   screen.fill((0, 0, 0))

   # Event handling
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False

   if game_over:
       game_over_image = pygame.image.load("endimage.png").convert_alpha()
       game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
       screen.blit(game_over_image, (0, 0))
       font = pygame.font.Font(None, 72)
       score_text = font.render(f'Score: {score}', True, (255, 255, 255))
       screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
       pygame.display.flip()
       keys = pygame.key.get_pressed()
       if keys[pygame.K_RETURN]:
           restart_game()

   else:
       # Player movement
       keys = pygame.key.get_pressed()
       if keys[pygame.K_UP]:
           player_y -= player_speed
       if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - 100:
           player_y += player_speed
       if keys[pygame.K_LEFT] and player_x > 0:
           player_x -= player_speed
       if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 100:
           player_x += player_speed

       # End game with spacebar
       if keys[pygame.K_SPACE]:
           game_over = True

       # Check if player reached the top of the screen
       if player_y < 0:
           level += 1
           score += 2 ** level
           current_bg = (current_bg + 1) % len(backgrounds)
           player_y = SCREEN_HEIGHT - 100
           spawn_obstacles(backgrounds[current_bg]["type"])

       # Draw current background
       screen.blit(backgrounds[current_bg]["image"], (0, 0))

       # Move and draw obstacles
       for car in carleft:
           car["x"] -= car["speed"]
           if car["x"] < -140:
               car["x"] = SCREEN_WIDTH + random.randint(50, 200)
           screen.blit(carleft_image, (car["x"], car["y"]))
       for t in train:
           t["x"] -= t["speed"]
           if t["x"] < -400:
               t["x"] = SCREEN_WIDTH + 200
           screen.blit(train_image, (t["x"], t["y"]))
       if deer:
           deer["x"] += deer["speed"] * deer["direction"]
           if deer["x"] < 50 or deer["x"] > 550:
               deer["direction"] *= -1
           screen.blit(deer_image, (deer["x"], deer["y"]))

       # Check collisions
       if check_obstacle_collision(player_x, player_y, player_image, carleft, carleft_image) or \
          check_obstacle_collision(player_x, player_y, player_image, train, train_image) or \
          check_deer_collision(player_x, player_y, player_image, deer):
           score = 0
           game_over = True

       # Draw player
       screen.blit(player_image, (player_x, player_y))

       # Prevent player from going out of bounds
       player_x = max(0, min(player_x, SCREEN_WIDTH - 100))
       player_y = min(player_y, SCREEN_HEIGHT - 100)

       # Display score
       font = pygame.font.Font(None, 36)
       score_text = font.render(f"Score: {score}", True, (255, 255, 255))
       screen.blit(score_text, (10, 10))

   # Update display
   pygame.display.flip()
   clock.tick(60)

# Quit Pygame
pygame.quit()