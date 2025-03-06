import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Shooting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player settings
player_size = 50
player_x = screen_width // 2 - player_size // 2
player_y = screen_height - player_size - 10
player_speed = 5

# Bullet settings
bullets = []
bullet_radius = 5
bullet_speed = 10
bullet_cooldown = 250  # milliseconds
last_shot_time = 0

# Target settings
targets = []
target_size = 40
target_speed = 2
target_spawn_rate = 1000  # milliseconds
last_spawn_time = 0

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Game state
game_running = True

# Explosion timing
explosion_duration = 200  # milliseconds
explosions = []  # List to track explosion timings

# Clock for controlling frame rate
clock = pygame.time.Clock()

def spawn_target():
    """Create a new target at a random position"""
    x = random.randint(0, screen_width - target_size)
    y = random.randint(-100, -target_size)
    targets.append({"x": x, "y": y, "hit": False})

def draw_player(x, y):
    """Draw the player triangle"""
    points = [
        (x + player_size // 2, y),  # Top
        (x, y + player_size),  # Bottom left
        (x + player_size, y + player_size)  # Bottom right
    ]
    pygame.draw.polygon(screen, GREEN, points)

def shoot_bullet():
    """Create a new bullet at the player's position"""
    bullet_x = player_x + player_size // 2
    bullet_y = player_y
    bullets.append({"x": bullet_x, "y": bullet_y})

def update_bullets():
    """Move bullets and remove those that go off screen"""
    for bullet in bullets[:]:
        bullet["y"] -= bullet_speed
        if bullet["y"] < 0:
            bullets.remove(bullet)

def update_targets():
    """Move targets down and remove those that go off screen"""
    for target in targets[:]:
        if not target["hit"]:
            target["y"] += target_speed
            if target["y"] > screen_height:
                targets.remove(target)
                return False
    return True

def check_collisions():
    """Check for collisions between bullets and targets"""
    global score
    current_time = pygame.time.get_ticks()
    
    for bullet in bullets[:]:
        for target in targets[:]:
            if not target["hit"]:
                # Calculate distance between bullet and target center
                target_center_x = target["x"] + target_size // 2
                target_center_y = target["y"] + target_size // 2
                distance = math.sqrt((bullet["x"] - target_center_x) ** 2 + 
                                    (bullet["y"] - target_center_y) ** 2)
                
                # Check if distance is less than the sum of radii
                if distance < (bullet_radius + target_size // 2):
                    target["hit"] = True
                    if bullet in bullets:
                        bullets.remove(bullet)
                    score += 10
                    # Add explosion with current time
                    explosions.append({"target": target, "start_time": current_time})

def update_explosions():
    """Update explosions and remove targets after animation completes"""
    current_time = pygame.time.get_ticks()
    
    for explosion in explosions[:]:
        if current_time - explosion["start_time"] > explosion_duration:
            # Remove the exploded target
            if explosion["target"] in targets:
                targets.remove(explosion["target"])
            # Remove the explosion
            explosions.remove(explosion)

def draw_game():
    """Draw all game elements"""
    screen.fill(BLACK)
    
    # Draw player
    draw_player(player_x, player_y)
    
    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(screen, BLUE, (int(bullet["x"]), int(bullet["y"])), bullet_radius)
    
    # Draw targets and explosions
    for target in targets:
        if not target["hit"]:
            pygame.draw.rect(screen, RED, (target["x"], target["y"], target_size, target_size))
        else:
            # Draw explosion animation
            pygame.draw.circle(screen, (255, 165, 0), 
                              (int(target["x"] + target_size // 2), 
                               int(target["y"] + target_size // 2)), 
                              target_size // 2)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()

# Main game loop
while game_running:
    current_time = pygame.time.get_ticks()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = False
    
    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
        player_x += player_speed
    
    # Handle shooting
    if keys[pygame.K_SPACE] and current_time - last_shot_time > bullet_cooldown:
        shoot_bullet()
        last_shot_time = current_time
    
    # Spawn targets
    if current_time - last_spawn_time > target_spawn_rate:
        spawn_target()
        last_spawn_time = current_time
    
    # Update game state
    update_bullets()
    game_active = update_targets()
    check_collisions()
    update_explosions()
    
    # Draw everything
    draw_game()
    
    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()