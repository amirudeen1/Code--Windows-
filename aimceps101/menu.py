import pygame

class Menu:
    def __init__(self, window_size):
        self.window_size = window_size
        self.font = pygame.font.Font(None, int(window_size[1] / 20))
        button_width = int(window_size[0] / 4)
        button_height = int(window_size[1] / 12)
        
        start_x = (window_size[0] - button_width) // 2
        start_y = window_size[1] // 2 - 2.5 * button_height

        self.buttons = [
            Button(start_x, start_y, button_width, button_height, "Static Mode", (0, 255, 0), (0, 0, 0), self.font),
            Button(start_x, start_y + button_height * 1.5, button_width, button_height, "Moving Mode", (255, 255, 0), (0, 0, 0), self.font),
            Button(start_x, start_y + button_height * 3, button_width, button_height, "Shrinking Mode", (0, 255, 255), (0, 0, 0), self.font),
            Button(start_x, start_y + button_height * 4.5, button_width, button_height, "High Scores", (255, 165, 0), (0, 0, 0), self.font),
            Button(start_x, start_y + button_height * 6, button_width, button_height, "Quit", (255, 0, 0), (0, 0, 0), self.font)
        ]

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.is_clicked(pos):
                    return button.text
        return None

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)