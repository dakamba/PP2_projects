import pygame
import sys
import json
import os
from game import Game
from db import Database
from config import *

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, font):
        self.rect = pygame.Rect(x - width//2, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=5)
        
        text_img = self.font.render(self.text, True, BLACK if current_color != BLACK else WHITE)
        text_rect = text_img.get_rect(center=self.rect.center)
        screen.blit(text_img, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class MainApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game: TSIS 4")
        self.clock = pygame.time.Clock()
        
        self.db = Database()
        self.settings_file = 'settings.json'
        self.load_settings()
        
        self.state = 'MENU'
        self.username = ""
        self.current_game = None
        
        # Шрифты
        self.font = pygame.font.SysFont("Verdana", 24)
        self.big_font = pygame.font.SysFont("Verdana", 48, bold=True)
        self.small_font = pygame.font.SysFont("Verdana", 18)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {"snake_color": [0, 255, 0], "grid": True, "sound": True}
            self.save_settings()

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

    def draw_text(self, text, font, color, x, y, center=False):
        img = font.render(text, True, color)
        rect = img.get_rect()
        if center: rect.center = (x, y)
        else: rect.topleft = (x, y)
        self.screen.blit(img, rect)

    def menu_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("SNAKE ADVENTURE", self.big_font, GREEN, WINDOW_WIDTH//2, 80, True)
        
        # Отрисовка поля ввода
        input_rect = pygame.Rect(WINDOW_WIDTH//2 - 150, 180, 300, 40)
        pygame.draw.rect(self.screen, GRAY, input_rect, border_radius=5)
        self.draw_text(f"Name: {self.username}", self.font, WHITE, WINDOW_WIDTH//2, 200, True)

        # Кнопки
        btn_play = Button("PLAY", WINDOW_WIDTH//2, 260, 200, 50, GREEN, (0, 200, 0), self.font)
        btn_lead = Button("LEADERBOARD", WINDOW_WIDTH//2, 330, 250, 50, YELLOW, (200, 200, 0), self.font)
        btn_sett = Button("SETTINGS", WINDOW_WIDTH//2, 400, 200, 50, WHITE, (200, 200, 200), self.font)
        btn_quit = Button("QUIT", WINDOW_WIDTH//2, 470, 200, 50, RED, (200, 0, 0), self.font)

        btn_play.draw(self.screen)
        btn_lead.draw(self.screen)
        btn_sett.draw(self.screen)
        btn_quit.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            # Логика нажатий на кнопки
            if btn_play.is_clicked(event) and self.username:
                player_id = self.db.get_or_create_player(self.username)
                pb = self.db.get_personal_best(player_id)
                self.current_game = Game(self.settings, player_id, pb)
                self.state = 'GAME'
            if btn_lead.is_clicked(event): self.state = 'LEADERBOARD'
            if btn_sett.is_clicked(event): self.state = 'SETTINGS'
            if btn_quit.is_clicked(event): pygame.quit(); sys.exit()

            # Логика ввода текста (теперь буквы не вызывают другие экраны)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif event.key == pygame.K_RETURN and self.username:
                    player_id = self.db.get_or_create_player(self.username)
                    pb = self.db.get_personal_best(player_id)
                    self.current_game = Game(self.settings, player_id, pb)
                    self.state = 'GAME'
                else:
                    if len(self.username) < 12 and event.unicode.isprintable():
                        self.username += event.unicode

    def settings_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("SETTINGS", self.big_font, YELLOW, WINDOW_WIDTH//2, 80, True)
        
        grid_status = "ON" if self.settings["grid"] else "OFF"
        btn_grid = Button(f"Grid: {grid_status}", WINDOW_WIDTH//2, 200, 250, 50, WHITE, GRAY, self.font)
        
        color_name = "GREEN" if self.settings["snake_color"] == [0, 255, 0] else "BLUE"
        btn_color = Button(f"Color: {color_name}", WINDOW_WIDTH//2, 280, 250, 50, WHITE, GRAY, self.font)
        
        btn_back = Button("SAVE & BACK", WINDOW_WIDTH//2, 450, 250, 50, GREEN, (0, 200, 0), self.font)

        btn_grid.draw(self.screen)
        btn_color.draw(self.screen)
        btn_back.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if btn_grid.is_clicked(event):
                self.settings["grid"] = not self.settings["grid"]
            if btn_color.is_clicked(event):
                self.settings["snake_color"] = [0, 0, 255] if self.settings["snake_color"] == [0, 255, 0] else [0, 255, 0]
            if btn_back.is_clicked(event):
                self.save_settings()
                self.state = 'MENU'

    def leaderboard_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("TOP 10", self.big_font, YELLOW, WINDOW_WIDTH//2, 60, True)
        
        scores = self.db.get_top_scores()
        for i, (name, score, level, date) in enumerate(scores):
            txt = f"{i+1}. {name:<10} | Score: {score} | Lvl: {level}"
            self.draw_text(txt, self.font, WHITE, 100, 150 + i*35)
            
        btn_back = Button("BACK", WINDOW_WIDTH//2, 550, 150, 40, GREEN, (0, 200, 0), self.font)
        btn_back.draw(self.screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if btn_back.is_clicked(event): self.state = 'MENU'

    def game_over_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.big_font, RED, WINDOW_WIDTH//2, 150, True)
        
        btn_retry = Button("RETRY", WINDOW_WIDTH//2, 300, 200, 50, GREEN, (0, 200, 0), self.font)
        btn_menu = Button("MENU", WINDOW_WIDTH//2, 380, 200, 50, WHITE, GRAY, self.font)
        
        btn_retry.draw(self.screen)
        btn_menu.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if btn_retry.is_clicked(event):
                pb = self.db.get_personal_best(self.current_game.player_id)
                self.current_game = Game(self.settings, self.current_game.player_id, pb)
                self.state = 'GAME'
            if btn_menu.is_clicked(event):
                self.state = 'MENU'

    def run(self):
        while True:
            if self.state == 'MENU': self.menu_screen()
            elif self.state == 'SETTINGS': self.settings_screen()
            elif self.state == 'LEADERBOARD': self.leaderboard_screen()
            elif self.state == 'GAMEOVER': self.game_over_screen()
            elif self.state == 'GAME':
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                
                running = self.current_game.update(events)
                self.current_game.draw(self.screen)
                
                if not running:
                    self.db.save_score(self.current_game.player_id, self.current_game.score, self.current_game.level)
                    self.state = 'GAMEOVER'
                self.clock.tick(self.current_game.speed)
            
            pygame.display.flip()

if __name__ == "__main__":
    app = MainApp()
    app.run()