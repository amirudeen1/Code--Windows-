import pygame
import sys
import math # For distance between mouse click and target to register click
import random # Repositioning of targets after each hits
import time # Time aspect of the game 

# Initialize Pygame
pygame.init()

# Create a display surface for game with size 800x600
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Aimceps")

# Define target
target_color = (0, 255, 255) # Cyan targets
target_radius = 25

# Initialize the score
score = 0
font = pygame.font.Font(None, 36)

# Game duration
game_duration = 30
start_time = time.time()

# Function to get random position
def get_random_position(window_size, radius):
    x = random.randint(radius, window_size[0] - radius)
    y = random.randint(radius, window_size[1] - radius)
    return (x, y)

# Initial target position
target_position = get_random_position(window_size, target_radius)

def is_target_hit(target_pos, click_pos, radius):
    # pythagoras for distance bnetween click and target
    distance = math.sqrt((target_pos[0] - click_pos[0]) ** 2 + (target_pos[1] - click_pos[1]) ** 2)
    return distance <= radius 

# Main game loop
running = True
while running:
    current_time = time.time()
    elapsed_time = current_time - start_time
    remaining_time = max(0, game_duration - int(elapsed_time))

    if remaining_time == 0:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if is_target_hit(target_position, mouse_pos, target_radius):
                score += 1
                target_position = get_random_position(window_size, target_radius)

    # Fill screen with black
    screen.fill((0, 0, 0)) # Black in RGB values

    # Draw target
    pygame.draw.circle(screen, target_color, target_position, target_radius)

    # Show score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Render remaining time
    timer_text = font.render(f"Time: {remaining_time}", True, (255, 255, 255))
    screen.blit(timer_text, (10, 40))

    # Update display
    pygame.display.flip()

# Displaying final score
screen.fill((255, 255, 255))
final_score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
screen.blit(final_score_text, (window_size[0] // 2 - final_score_text.get_width() // 2, window_size[1] //2))
pygame.display.flip()

# Wait for a few seconds before quitting, 5000 ms = 5 seconds
pygame.time.wait(5000) 

# Quit 
pygame.quit()
sys.exit()