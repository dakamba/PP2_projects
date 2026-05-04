# main.py — Точка входа в приложение Snake Game (TSIS 4)
# Управляет экранами, событиями, состоянием игры и интеграцией с БД

import pygame, sys, random
from config import *                          # Константы[cite: 1]
from game import SnakeGame, _t               # Логика игры[cite: 1]
from db import init_db, save_session, get_leaderboard, get_personal_best  # PostgreSQL[cite: 1]
from settings_manager import load_settings, save_settings  # JSON[cite: 1]

# --- ПАЛИТРА ДИЗАЙНА ---
NEON_CYAN  = (0, 255, 255)
NEON_GREEN = (57, 255, 20)
DEEP_SPACE = (10, 15, 25)
SLATE_BLUE = (30, 40, 60)
ACCENT_RED = (255, 45, 85)

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4 — Cyber Snake")
CLOCK = pygame.time.Clock()

# Шрифты[cite: 1]
FONT_TITLE = pygame.font.SysFont("consolas", 50, bold=True)
FONT_BIG   = pygame.font.SysFont("consolas", 32, bold=True)
FONT_MED   = pygame.font.SysFont("consolas", 24, bold=True)
FONT_SMALL = pygame.font.SysFont("consolas", 18, bold=True)
FONT_TINY  = pygame.font.SysFont("consolas", 14)

S_MENU, S_USERNAME, S_PLAYING = "MENU", "USERNAME", "PLAYING"
S_GAME_OVER, S_LEADERBOARD, S_SETTINGS = "GAME_OVER", "LEADERBOARD", "SETTINGS"

DB_OK = init_db()

class Button:
    """дизайн: 'Ghost Button' с неоновой рамкой и свечением[cite: 1]."""
    def __init__(self, x, y, w, h, text, color=NEON_CYAN):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.base_color = color
        self.alpha = 40 # Прозрачность фона

    def draw(self, surf):
        mx, my = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mx, my)
        
        # Отрисовка полупрозрачного фона при наведении
        bg_col = (*self.base_color, 80 if is_hover else 30)
        temp_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, bg_col, (0, 0, self.rect.width, self.rect.height), border_radius=4)
        surf.blit(temp_surface, self.rect.topleft)

        # Неоновая рамка
        border_w = 3 if is_hover else 1
        pygame.draw.rect(surf, self.base_color, self.rect, border_w, border_radius=4)
        
        # Текст
        txt_col = WHITE if is_hover else self.base_color
        img = FONT_SMALL.render(self.text, True, txt_col)
        surf.blit(img, img.get_rect(center=self.rect.center))

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 
                and self.rect.collidepoint(event.pos))

class App:
    def __init__(self):
        self.state = S_MENU
        self.settings = load_settings()
        self.username = ""
        self.typing = ""
        self.snake_game = None
        self.personal_best = 0
        self.last_score = 0
        self.last_level = 1
        self.last_reason = ""
        self.session_saved = False
        self.snake_timer = 0
        self._build_buttons()

    def _build_buttons(self):
        cx = WIDTH // 2
        # Главное меню
        self.btn_play  = Button(cx-110, 280, 220, 50, "INITIALIZE")
        self.btn_lb    = Button(cx-110, 350, 220, 50, "LEADERBOARD")
        self.btn_set   = Button(cx-110, 420, 220, 50, "SETTINGS")
        self.btn_quit  = Button(cx-110, 490, 220, 50, "TERMINATE", ACCENT_RED)

        self.btn_back  = Button(20, 20, 100, 40, "< BACK")

        # Game Over
        self.btn_retry = Button(cx-110, 450, 220, 50, "REBOOT")
        self.btn_menu  = Button(cx-110, 520, 220, 50, "MAIN_MENU")

        # Настройки
        self.btn_grid  = Button(cx-110, 220, 220, 45, "")
        self.btn_sound = Button(cx-110, 280, 220, 45, "")
        self.btn_color = Button(cx-110, 340, 220, 45, "")
        self.btn_save  = Button(cx-110, 480, 220, 50, "APPLY & EXIT", NEON_GREEN)

        self._color_opts  = [[80,200,80],[80,140,255],[240,200,60],[220,80,80],[200,100,255]]
        self._color_names = ["Matrix Green","Plasma Blue","Cyber Gold","System Red","Neon Violet"]
        self._color_idx = 0
        for i, c in enumerate(self._color_opts):
            if c == self.settings["snake_color"]: self._color_idx = i; break

    def run(self):
        while True:
            dt = CLOCK.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if   self.state == S_MENU:        self._ev_menu(event)
                elif self.state == S_USERNAME:    self._ev_username(event)
                elif self.state == S_PLAYING:     self._ev_playing(event)
                elif self.state == S_GAME_OVER:   self._ev_gameover(event)
                elif self.state == S_LEADERBOARD:
                    if self.btn_back.clicked(event): self.state = S_MENU
                elif self.state == S_SETTINGS:    self._ev_settings(event)
            self._update(dt)
            self._draw()

    def _ev_menu(self, ev):
        if   self.btn_play.clicked(ev):  self.state = S_USERNAME; self.typing = self.username
        elif self.btn_lb.clicked(ev):    self.state = S_LEADERBOARD
        elif self.btn_set.clicked(ev):   self.state = S_SETTINGS
        elif self.btn_quit.clicked(ev):  pygame.quit(); sys.exit()

    def _ev_username(self, ev):
        if self.btn_back.clicked(ev): self.state = S_MENU
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                self.username = self.typing.strip() or "USER_404"
                self._start_game()
            elif ev.key == pygame.K_BACKSPACE: self.typing = self.typing[:-1]
            elif ev.unicode.isprintable() and len(self.typing) < 12: self.typing += ev.unicode

    def _ev_playing(self, ev):
        if ev.type == pygame.KEYDOWN:
            k = ev.key
            if k == pygame.K_ESCAPE: self.state = S_MENU
            elif k in (pygame.K_UP,    pygame.K_w): self.snake_game.change_direction("UP")
            elif k in (pygame.K_DOWN,  pygame.K_s): self.snake_game.change_direction("DOWN")
            elif k in (pygame.K_LEFT,  pygame.K_a): self.snake_game.change_direction("LEFT")
            elif k in (pygame.K_RIGHT, pygame.K_d): self.snake_game.change_direction("RIGHT")

    def _ev_gameover(self, ev):
        if   self.btn_retry.clicked(ev): self._start_game()
        elif self.btn_menu.clicked(ev):  self.state = S_MENU

    def _ev_settings(self, ev):
        if   self.btn_grid.clicked(ev):  self.settings["grid_overlay"] = not self.settings["grid_overlay"]
        elif self.btn_sound.clicked(ev): self.settings["sound"] = not self.settings["sound"]
        elif self.btn_color.clicked(ev):
            self._color_idx = (self._color_idx + 1) % len(self._color_opts)
            self.settings["snake_color"] = self._color_opts[self._color_idx]
        elif self.btn_save.clicked(ev):  save_settings(self.settings); self.state = S_MENU
        elif self.btn_back.clicked(ev):  self.state = S_MENU

    def _start_game(self):
        self.personal_best = get_personal_best(self.username) if DB_OK else 0
        self.settings = load_settings()
        self.snake_game = SnakeGame(self.settings, self.username, self.personal_best)
        self.snake_timer = 0
        self.session_saved = False
        self.state = S_PLAYING

    def _update(self, dt):
        if self.state != S_PLAYING or not self.snake_game: return
        step_ms = 1000 // self.snake_game.current_fps
        self.snake_timer += dt
        while self.snake_timer >= step_ms:
            self.snake_timer -= step_ms
            self.snake_game.update()

        if self.snake_game.game_over and not self.session_saved:
            self.last_score, self.last_level = self.snake_game.score, self.snake_game.level
            self.last_reason = self.snake_game.game_over_reason
            if DB_OK: save_session(self.username, self.last_score, self.last_level)
            self.personal_best = get_personal_best(self.username) if DB_OK else self.last_score
            self.session_saved = True
            self.state = S_GAME_OVER

    def _draw_background(self):
        """Рисует статичную сетку на фоне для стиля[cite: 1]."""
        SCREEN.fill(DEEP_SPACE)
        for x in range(0, WIDTH, 40):
            pygame.draw.line(SCREEN, (20, 30, 45), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(SCREEN, (20, 30, 45), (0, y), (WIDTH, y))

    def _draw(self):
        self._draw_background()
        if   self.state == S_MENU:          self._draw_menu()
        elif self.state == S_USERNAME:      self._draw_username()
        elif self.state == S_PLAYING:       self._draw_playing()
        elif self.state == S_GAME_OVER:     self._draw_gameover()
        elif self.state == S_LEADERBOARD:   self._draw_leaderboard()
        elif self.state == S_SETTINGS:      self._draw_settings()
        pygame.display.flip()

    def _draw_menu(self):
        cx = WIDTH // 2
        _t(FONT_TITLE, "CYBER SNAKE", NEON_CYAN, SCREEN, cx, 110, center=True)
        _t(FONT_TINY, "VERSION 1.0.4 // TSIS 4", SLATE_BLUE, SCREEN, cx, 165, center=True)
        if not DB_OK:
            _t(FONT_TINY, "DATABASE OFFLINE - LOCAL MODE", ACCENT_RED, SCREEN, cx, 220, center=True)
        self.btn_play.draw(SCREEN); self.btn_lb.draw(SCREEN)
        self.btn_set.draw(SCREEN);  self.btn_quit.draw(SCREEN)

    def _draw_username(self):
        cx = WIDTH // 2
        _t(FONT_BIG, "IDENTITY INPUT", NEON_CYAN, SCREEN, cx, 200, center=True)
        box = pygame.Rect(cx-160, 280, 320, 50)
        pygame.draw.rect(SCREEN, NEON_CYAN, box, 2, border_radius=5)
        _t(FONT_MED, self.typing + ("_" if pygame.time.get_ticks() % 1000 < 500 else ""),
           WHITE, SCREEN, box.x+15, box.y+10)
        _t(FONT_TINY, "PRESS ENTER TO AUTHORIZE", SLATE_BLUE, SCREEN, cx, 350, center=True)
        self.btn_back.draw(SCREEN)

    def _draw_playing(self):
        if self.snake_game:
            self.snake_game.draw(SCREEN)
            self.snake_game.draw_hud(SCREEN, FONT_MED, FONT_SMALL)

    def _draw_gameover(self):
        cx = WIDTH // 2
        _t(FONT_TITLE, "SYSTEM HALT", ACCENT_RED, SCREEN, cx, 130, center=True)
        _t(FONT_SMALL, f">> {self.last_reason}", WHITE, SCREEN, cx, 190, center=True)
        
        stats_rect = pygame.Rect(cx-150, 230, 300, 140)
        pygame.draw.rect(SCREEN, (20, 20, 30), stats_rect, border_radius=10)
        
        _t(FONT_MED,   f"SCORE: {self.last_score}", NEON_CYAN, SCREEN, cx, 260, center=True)
        _t(FONT_SMALL, f"LVL: {self.last_level}", WHITE, SCREEN, cx, 300, center=True)
        _t(FONT_SMALL, f"BEST: {self.personal_best}", NEON_GREEN, SCREEN, cx, 335, center=True)
        
        self.btn_retry.draw(SCREEN); self.btn_menu.draw(SCREEN)

    def _draw_leaderboard(self):
        cx = WIDTH // 2
        _t(FONT_BIG, "GLOBAL TOP 10", NEON_CYAN, SCREEN, cx, 60, center=True)
        if not DB_OK:
            _t(FONT_SMALL, "CONNECTION ERROR", ACCENT_RED, SCREEN, cx, HEIGHT//2, center=True)
        else:
            data = get_leaderboard(10)
            xs = [40, 100, 300, 380, 460]
            header_y = 130
            for i, h in enumerate(["#", "USER", "PTS", "LVL", "DATE"]):
                _t(FONT_TINY, h, SLATE_BLUE, SCREEN, xs[i], header_y)
            
            y = 170
            for rank, uname, score, lvl, dt in data:
                time_str = dt.strftime("%H:%M") if dt else "---"
                _t(FONT_SMALL, str(rank), NEON_CYAN, SCREEN, xs[0], y)
                _t(FONT_SMALL, uname[:12].upper(), WHITE, SCREEN, xs[1], y)
                _t(FONT_SMALL, str(score), NEON_GREEN, SCREEN, xs[2], y)
                _t(FONT_SMALL, str(lvl), WHITE, SCREEN, xs[3], y)
                _t(FONT_TINY,  time_str, SLATE_BLUE, SCREEN, xs[4], y+4)
                y += 40
        self.btn_back.draw(SCREEN)

    def _draw_settings(self):
        cx = WIDTH // 2
        _t(FONT_BIG, "CONFIGURATION", NEON_CYAN, SCREEN, cx, 120, center=True)
        self.btn_grid.text  = f"GRID_FX: {'ENABLED' if self.settings['grid_overlay'] else 'DISABLED'}"
        self.btn_sound.text = f"AUDIO:   {'ONLINE' if self.settings['sound'] else 'OFFLINE'}"
        self.btn_color.text = f"HUE:     {self._color_names[self._color_idx].upper()}"
        
        for btn in [self.btn_grid, self.btn_sound, self.btn_color, self.btn_save]: btn.draw(SCREEN)
        
        # Индикатор цвета
        preview = pygame.Rect(cx-70, 400, 140, 6)
        pygame.draw.rect(SCREEN, self.settings["snake_color"], preview, border_radius=3)

if __name__ == "__main__":
    app = App()
    app.run()