import pygame
import sys
import math # For distance between mouse click and target to register click
import random # Repositioning of targets after each hits

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if is_target_hit(target_position, mouse_pos, target_radius):
                print("Target hit")
                score += 1
                target_position = get_random_position(window_size, target_radius)

    # Fill screen with black
    screen.fill((0, 0, 0)) # Black in RGB values

    # Draw target
    pygame.draw.circle(screen, target_color, target_position, target_radius)

    # Show score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

# Quit 
pygame.quit()
sys.exit

    