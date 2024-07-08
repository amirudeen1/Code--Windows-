import pygame

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        pygame.mouse.set_visible(False)  # Hide the default cursor

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def draw(self, screen):
        screen.blit(self.image, self.rect)