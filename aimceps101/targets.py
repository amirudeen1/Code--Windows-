import pygame
import random
import math

class Target:
    def __init__(self, window_size):
        self.window_size = window_size
        self.radius = int(30 * 1.5)  # Increased base radius by 1.5x
        self.position = self.get_random_position()
        self.color = (0, 255, 255)  # Cyan
        self.points = 1

    def get_random_position(self):
        x = random.randint(self.radius, self.window_size[0] - self.radius)
        y = random.randint(self.radius, self.window_size[1] - self.radius)
        return [x, y]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), int(self.radius))

    def is_hit(self, click_pos):
        distance = math.sqrt((self.position[0] - click_pos[0])**2 + (self.position[1] - click_pos[1])**2)
        return distance <= self.radius

class StaticTarget(Target):
    def __init__(self, window_size):
        super().__init__(window_size)
        self.color = (0, 255, 0)  # Green

class MovingTarget(Target):
    def __init__(self, window_size):
        super().__init__(window_size)
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, 2 * math.pi)
        self.color = (255, 255, 0)  # Yellow
        self.points = 2

    def move(self):
        self.position[0] += math.cos(self.angle) * self.speed
        self.position[1] += math.sin(self.angle) * self.speed

        if self.position[0] <= self.radius or self.position[0] >= self.window_size[0] - self.radius:
            self.angle = math.pi - self.angle
        if self.position[1] <= self.radius or self.position[1] >= self.window_size[1] - self.radius:
            self.angle = -self.angle

class ShrinkingTarget(Target):
    def __init__(self, window_size):
        super().__init__(window_size)
        self.max_radius = int(45 * 1.5)  # Increased max radius by 1.5x
        self.min_radius = int(7.5 * 1.5)  # Increased min radius by 1.5x
        self.radius = self.max_radius
        self.shrink_speed = 0.1  # Reduced from 0.2 to 0.1 to shrink slower
        self.color = (255, 0, 255)  # Magenta
        self.points = 3

    def update(self):
        self.radius -= self.shrink_speed
        if self.radius < self.min_radius:
            self.radius = self.max_radius
            self.position = self.get_random_position()

    def is_hit(self, click_pos):
        if super().is_hit(click_pos):
            self.points = max(1, int((self.max_radius - self.radius) / 5) + 1)
            return True
        return False