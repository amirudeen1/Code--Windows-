import pygame
import sys
import time
from targets import StaticTarget, MovingTarget, ShrinkingTarget
from combo_system import ComboSystem
from menu import Menu
from crosshair import Crosshair
from database_handler import DatabaseHandler

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen_info = pygame.display.Info()
        self.window_size = (self.screen_info.current_w, self.screen_info.current_h)
        self.screen = pygame.display.set_mode(self.window_size, pygame.FULLSCREEN)
        pygame.display.set_caption("Enhanced Aimceps")
        
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        
        self.menu = Menu(self.window_size)
        self.crosshair = Crosshair('mycrosshair.png')
        
        self.game_duration = 60

        self.hit_sound = pygame.mixer.Sound('hit_sound.wav')

        self.total_shots = 0
        self.hits = 0

        self.db = DatabaseHandler()
        self.current_user = None

    def login_screen(self):
        pygame.mouse.set_visible(True)  
        input_box = pygame.Rect(self.window_size[0] // 4, self.window_size[1] // 2, self.window_size[0] // 2, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        password = ''
        entering_password = False
        users = self.db.get_users()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            if not entering_password:
                                entering_password = True
                                text = text.strip()
                            else:
                                if text in users:
                                    if self.db.verify_user(text, password):
                                        return text
                                    else:
                                        password = ''
                                        entering_password = False
                                else:
                                    self.db.add_user(text, password)
                                    return text
                        elif event.key == pygame.K_BACKSPACE:
                            if entering_password:
                                password = password[:-1]
                            else:
                                text = text[:-1]
                        else:
                            if entering_password:
                                password += event.unicode
                            else:
                                text += event.unicode

            self.screen.fill((30, 30, 30))
            
            # Render the input box
            txt_surface = self.font.render(text if not entering_password else '*' * len(password), True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(self.screen, color, input_box, 2)

            # Render the prompt
            prompt = "Enter username:" if not entering_password else "Enter password:"
            prompt_surface = self.font.render(prompt, True, (255, 255, 255))
            self.screen.blit(prompt_surface, (input_box.x, input_box.y - 40))

            # Render existing users
            user_text = "Existing users: " + ", ".join(users)
            user_surface = self.font.render(user_text, True, (255, 255, 255))
            self.screen.blit(user_surface, (input_box.x, input_box.y + 50))

            # Render instructions
            instructions = "Click on the box to start typing. Press Enter to submit."
            instructions_surface = self.font.render(instructions, True, (255, 255, 255))
            self.screen.blit(instructions_surface, (input_box.x, input_box.y + 90))

            pygame.display.flip()
            self.clock.tick(30)

    def show_high_scores(self):
        modes = ["Static", "Moving", "Shrinking"]
        while True:
            self.screen.fill((30, 30, 30))
            y_offset = 50
            for mode in modes:
                scores = self.db.get_high_scores(mode)
                self.draw_text(f"Top 5 {mode} Mode Scores:", (50, y_offset))
                y_offset += 40
                for i, (username, score) in enumerate(scores, 1):
                    self.draw_text(f"{i}. {username}: {score}", (70, y_offset))
                    y_offset += 30
                y_offset += 20

            self.draw_text("Press any key to return to menu", (50, y_offset + 20))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    return

    def run_game(self, mode):
        pygame.mouse.set_visible(False)
        score = 0
        start_time = time.time()
        combo_system = ComboSystem()

        if mode == "Static":
            targets = [StaticTarget(self.window_size) for _ in range(5)]  # Increased from 3 to 5
        elif mode == "Moving":
            targets = [MovingTarget(self.window_size) for _ in range(5)]
        elif mode == "Shrinking":
            targets = [ShrinkingTarget(self.window_size) for _ in range(5)]

        running = True
        while running:
            current_time = time.time()
            elapsed_time = current_time - start_time
            remaining_time = max(0, self.game_duration - int(elapsed_time))

            if remaining_time == 0:
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.total_shots += 1
                    mouse_pos = pygame.mouse.get_pos()
                    hit = False
                    for target in targets:
                        if target.is_hit(mouse_pos):
                            self.hit_sound.play()
                            self.hits += 1
                            hit = True
                            combo_system.hit(pygame.time.get_ticks())
                            score += int(target.points * combo_system.get_score_multiplier())
                            targets.remove(target)
                            new_target = self.create_new_target(mode)
                            targets.append(new_target)
                    if not hit:
                        combo_system.reset()

            self.screen.fill((0, 0, 0))

            for target in targets:
                if isinstance(target, MovingTarget):
                    target.move()
                elif isinstance(target, ShrinkingTarget):
                    target.update()
                target.draw(self.screen)

            combo_system.update(pygame.time.get_ticks())

            self.crosshair.update()
            self.crosshair.draw(self.screen)

            accuracy = (self.hits / self.total_shots * 100) if self.total_shots > 0 else 0
            self.draw_text(f"Score: {score}", (10, 10))
            self.draw_text(f"Time: {remaining_time}", (10, 40))
            self.draw_text(f"Combo: {combo_system.combo}x", (10, 70))
            self.draw_text(f"Accuracy: {accuracy:.1f}%", (10, 100))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.mouse.set_visible(True)
        self.db.add_score(self.current_user, mode, score)
        return score, accuracy

    def create_new_target(self, mode):
        if mode == "Static":
            return StaticTarget(self.window_size)
        elif mode == "Moving":
            return MovingTarget(self.window_size)
        elif mode == "Shrinking":
            return ShrinkingTarget(self.window_size)

    def draw_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, position)

    def show_final_score(self, score, accuracy, high_score):
        self.screen.fill((255, 255, 255))
        final_score_text = self.font.render(f"Final Score: {score}", True, (0, 0, 0))
        accuracy_text = self.font.render(f"Final Accuracy: {accuracy:.1f}%", True, (0, 0, 0))
        high_score_text = self.font.render(f"Your High Score: {high_score}", True, (0, 0, 0))
        score_rect = final_score_text.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 2 - 40))
        accuracy_rect = accuracy_text.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 2))
        high_score_rect = high_score_text.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 2 + 40))
        self.screen.blit(final_score_text, score_rect)
        self.screen.blit(accuracy_text, accuracy_rect)
        self.screen.blit(high_score_text, high_score_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

    def main_loop(self):
        self.current_user = self.login_screen()
        if self.current_user is None:
            return

        while True:
            pygame.mouse.set_visible(True)  # Ensure cursor is visible in the menu
            self.menu.draw(self.screen)
            self.draw_text(f"User: {self.current_user}", (10, 10))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                
                action = self.menu.handle_event(event)
                if action in ["Static Mode", "Moving Mode", "Shrinking Mode"]:
                    mode = action.split()[0]
                    pygame.mouse.set_visible(False)  # Hide cursor during gameplay
                    final_score, accuracy = self.run_game(mode)
                    pygame.mouse.set_visible(True)  # Show cursor after game ends
                    if final_score is None:  # User quit during the game
                        return
                    else:
                        high_score = self.db.get_user_high_score(self.current_user, mode)
                        self.show_final_score(final_score, accuracy, high_score)
                elif action == "High Scores":
                    self.show_high_scores()
                elif action == "Quit":
                    return

if __name__ == "__main__":
    game = Game()
    game.main_loop()
    game.db.close()
    pygame.quit()
    sys.exit()