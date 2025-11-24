import pygame
import sys
import time
import os
import math
from game_logic import Tile, initialise, reveal_tile, flag_tile
import settings
import file_manager

class MineSweeperBoard:

    def __init__(self):
        self.difficulty_settings = settings.difficulty_settings
        self.tile_size = settings.tile_size
        
        pygame.init()
        pygame.display.set_caption("Minesweeper")
        self.screen = None 
        self.clock = pygame.time.Clock()
        
        self.font_small = pygame.font.Font(None, int(self.tile_size * 0.8))
        self.font_status = pygame.font.Font(None, 24)
        self.font_popup_title = pygame.font.Font(None, 48)
        self.font_popup_text = pygame.font.Font(None, 30)
        self.font_difficulty = pygame.font.Font(None, 20)


        self.start_time = 0.0 
        self.best_time = None 

        self.dropdown_active = False
        self.dropdown_box = None 
        self.dropdown_options_rects = {}
        
        self.flag_count = 0
        self.mines_left = 0
        
        #assets
        self.flower = None
        self.win_bgm = None
        self.boom = None
        self.sound_flag = None
        self.music_started = False
        self.flower_animation_time = 0
        
        self.load_assets()
        self.apply_difficulty('Easy')

    def load_assets(self):
        try:
            pygame.mixer.init()
            if os.path.exists('flower.png'):
                self.flower = pygame.image.load('flower.png').convert_alpha()
                self.flower = pygame.transform.smoothscale(self.flower, (int(self.tile_size * 0.8), int(self.tile_size * 0.8)))

            if os.path.exists(f'assets/win.mp3'):
                self.win_bgm = pygame.mixer.Sound(f'assets/win.mp3')

            if os.path.exists(f'assets/explode.mp3'):
                self.boom = pygame.mixer.Sound(f'assets/explode.mp3')
            
            if os.path.exists(f'assets/flag.mp3'):
                self.sound_flag = pygame.mixer.Sound(f'assets/flag.mp3')
            
            if os.path.exists(f'assets/bg_music.mp3'):
                pygame.mixer.music.load(f'assets/bg_music.mp3')
                pygame.mixer.music.set_volume(0.8)
        except Exception as e:
            print(f"Asset loading warning: {e}")

    def get_best_time(self, difficulty_name):
        return f'rec/best_time_{difficulty_name}.txt'

    def load_best_time(self, difficulty_name):
        filename = self.get_best_time(difficulty_name)
        val = file_manager.load_best_time(filename)
        if val == "N/A":
            return None
        try:
            return float(val)
        except ValueError:
            return None


    def save_best_time(self, new_best_time):
        filename = self.get_best_time(self.difficulty_name)
        try:
            saved_val = file_manager.save_best_time(new_best_time, filename)
            self.best_time = saved_val
            print(f"🎉 New best time for {self.difficulty_name}: {new_best_time:.2f}s")
        except Exception as e:
            print(f"Error saving best time")

    def apply_difficulty(self, name):
        w, h, m = self.difficulty_settings[name]

        self.GRID_W = w
        self.GRID_H = h
        self.mc = m
        self.GAME_W = self.GRID_W * self.tile_size
        self.GAME_H = self.GRID_H * self.tile_size + 50
        self.difficulty_name = name
        
        self.best_time = self.load_best_time(name)
        
        self.screen = pygame.display.set_mode((self.GAME_W, self.GAME_H))
        
        self.tiles = self.create_empty_board()
        self.is_initial_click = True
        self.game_over = False
        self.game_won = False
        self.start_time = 0.0
        self.current_time = 0.0
        self.timer_running = False
        self.restart_button = None
        self.dropdown_active = False
        
        self.flag_count = 0
        self.mines_left = self.mc
        self.flower_animation_time = 0
        
    def create_empty_board(self):
        return [[Tile(x, y) for y in range(self.GRID_H)] for x in range(self.GRID_W)]

    def update_mine_counter(self):
        flag_count = sum(t.state == 'flagged' for row in self.tiles for t in row)
        self.flag_count = flag_count
        self.mines_left = max(0, self.mc - flag_count)

    def check_win(self):
        total_tiles = self.GRID_W * self.GRID_H
        target_reveals = total_tiles - self.mc
        
        revealed_safe_tiles = sum(
            1 for row in self.tiles 
            for tile in row 
            if tile.value != -1 and not tile.clickable
        )
        
        if revealed_safe_tiles >= target_reveals:
            self.timer_running = False
            if self.start_time > 0:
                self.current_time = time.time() - self.start_time
            else:
                self.current_time = 0.0
            
            self.game_won = True
            self.game_over = True
            
            if self.win_bgm:
                self.win_bgm.play()
            try:
                pygame.mixer.music.stop()
            except:
                pass
            
            self.flower_animation_time = time.time()
            
            for row in self.tiles:
                for tile in row:
                    if tile.value == -1:
                        tile.state = 'flower'
            
            if self.best_time is None or self.current_time < self.best_time:
                self.save_best_time(self.current_time)

    def draw_flower(self, rect, animated=False):
        if self.flower:
            if animated and self.flower_animation_time > 0:
                elapsed = time.time() - self.flower_animation_time
                pulse = 0.9 + 0.1 * abs(math.sin(elapsed * 3))
                size = int(self.tile_size * 0.8 * pulse)
                img = pygame.transform.smoothscale(self.flower, (size, size))
            else:
                img = self.flower
            
            center_x, center_y = rect.center
            x = center_x-img.get_width() // 2
            y = center_y-img.get_height() // 2
            self.screen.blit(img, (x, y))
        else:
            center_x, center_y = rect.center
            petal_color = (255, 105, 180)
            center_color = (255, 215, 0)
            radius = int(self.tile_size * 0.15)
            for angle in range(0, 360, 72):
                rad = math.radians(angle)
                px = center_x + int(radius * 1.5 * math.cos(rad))
                py = center_y + int(radius * 1.5 * math.sin(rad))
                pygame.draw.circle(self.screen, petal_color, (px, py), radius)
            pygame.draw.circle(self.screen, center_color, (center_x, center_y), radius)

    def draw_flag(self, rect, icon_mode=False):
        center_x, center_y = rect.center
        flag_size = self.tile_size * 0.8 if not icon_mode else 15
        
        if icon_mode:
            pole_start = (center_x, center_y - flag_size * 0.6)
            pole_end = (center_x, center_y + flag_size * 0.6)
            pygame.draw.line(self.screen, (255, 255, 255), pole_start, pole_end, 1)
            flag_points = [
                (center_x, center_y - flag_size * 0.6),
                (center_x, center_y + flag_size * 0.1 + 1),
                (center_x - flag_size * 0.5 - 5, center_y - flag_size * 0.1)
            ]
            pygame.draw.polygon(self.screen, settings.COLOR_FLAG, flag_points)
        else:
            pole_start = (center_x, center_y - flag_size * 0.4)
            pole_end = (center_x, center_y + flag_size * 0.6)
            pygame.draw.line(self.screen, settings.COLOR_FLAG_POLE, pole_start, pole_end, 3)
            flag_points = [
                (center_x, center_y - flag_size * 0.4),
                (center_x, center_y + flag_size * 0.1),
                (center_x - flag_size * 0.5, center_y - flag_size * 0.1)
            ]
            pygame.draw.polygon(self.screen, settings.COLOR_FLAG, flag_points)
            pygame.draw.polygon(self.screen, settings.COLOR_TEXT, flag_points, 1)

    def draw_mine(self, rect, is_hit=False):
        if not hasattr(self, 'bomb'):
            if os.path.exists('assets/bomb.png'):
                self.bomb = pygame.image.load('assets/bomb.png').convert_alpha()
                self.bomb = pygame.transform.smoothscale(self.bomb, (self.tile_size, self.tile_size))
            else:
                self.bomb = None

        if self.bomb:
            self.screen.blit(self.bomb, rect.topleft)
        else:
            center_x, center_y = rect.center
            radius = self.tile_size * 0.3
            pygame.draw.circle(self.screen, settings.COLOR_BOMB, (center_x, center_y), int(radius))
            pygame.draw.circle(self.screen, settings.COLOR_TEXT, (center_x, center_y), int(radius), 1)

        if is_hit:
            r = int(self.tile_size * 0.5)
            center_x, center_y = rect.center
            pygame.draw.circle(self.screen, (255, 255, 0), (center_x, center_y), r, 3)

    def draw_clock(self, rect):
        center_x, center_y = rect.center
        radius = 12
        pygame.draw.circle(self.screen, settings.COLOR_ICON, (center_x, center_y), radius)
        pygame.draw.circle(self.screen, (255, 255, 255), (center_x, center_y), radius, 1)
        pygame.draw.line(self.screen, (0, 0, 0), (center_x, center_y), (center_x, center_y - 8), 1)
        pygame.draw.line(self.screen, (0, 0, 0), (center_x, center_y), (center_x + 7, center_y), 1)

    def draw_dropdown_menu(self):
        dropdown_w = self.dropdown_box.width
        dropdown_y = self.dropdown_box.bottom
        self.dropdown_options_rects = {}

        for i, name in enumerate(self.difficulty_settings.keys()):
            option_rect = pygame.Rect(10, dropdown_y + (i * 26), dropdown_w, 26)
            self.dropdown_options_rects[name] = option_rect
            
            bg_color = settings.COLOR_UNCLICKED_LIGHT if name != self.difficulty_name else settings.COLOR_STATUS_BAR
            if self.dropdown_active and option_rect.collidepoint(pygame.mouse.get_pos()):
                 bg_color = (190, 230, 100)

            pygame.draw.rect(self.screen, bg_color, option_rect, border_radius=0)
            pygame.draw.rect(self.screen, settings.COLOR_TEXT, option_rect, 1)

            text_color = settings.COLOR_TEXT if name != self.difficulty_name else (255, 255, 255)
            diff_text = self.font_difficulty.render(name, True, text_color)
            self.screen.blit(diff_text, (option_rect.x + 5, option_rect.y + 7))

    def draw_dropdown(self):
        self.dropdown_box = pygame.Rect(10, 12, 100, 26)
        bg_color = (255, 255, 255)
        if self.dropdown_active:
             bg_color = (190, 230, 100)
             
        pygame.draw.rect(self.screen, bg_color, self.dropdown_box, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), self.dropdown_box, 1, border_radius=5)
        
        diff_text = self.font_difficulty.render(self.difficulty_name, True, settings.COLOR_TEXT)
        self.screen.blit(diff_text, (self.dropdown_box.x + 5, self.dropdown_box.y + 7))
        
        arrow_x, arrow_y = self.dropdown_box.right - 15, self.dropdown_box.center[1]
        arrow_color = settings.COLOR_TEXT
        pygame.draw.polygon(self.screen, arrow_color, 
                            [(arrow_x - 5, arrow_y - 2), (arrow_x + 5, arrow_y - 2), (arrow_x, arrow_y + 3)])

        if self.dropdown_active:
            self.draw_dropdown_menu()

    def draw_status_bar(self):
        pygame.draw.rect(self.screen, settings.COLOR_STATUS_BAR, (0, 0, self.GAME_W, 50))
        self.draw_dropdown()

        center_x = self.GAME_W // 2

        flag_count = sum(t.state == 'flagged' for row in self.tiles for t in row)
        mines_left = max(0, self.mc - flag_count)
        
        flag_x = center_x - 70 
        mine_text_x = flag_x + 30 
        
        flag_icon_rect = pygame.Rect(flag_x, 10, 30, 30)
        self.draw_flag(flag_icon_rect, icon_mode=True)
        
        mine_text = self.font_status.render(str(mines_left).zfill(3), True, (255, 255, 255)) 
        self.screen.blit(mine_text, (mine_text_x, 15))

        timer_display = str(min(int(self.current_time), 999)).zfill(3)
        clock_x = center_x + 10
        timer_text_x = clock_x + 30
        
        clock_icon_rect = pygame.Rect(clock_x, 10, 30, 30)
        self.draw_clock(clock_icon_rect)
        
        timer_text = self.font_status.render(timer_display, True, (255, 255, 255))
        self.screen.blit(timer_text, (timer_text_x, 15))

    def draw_board(self):
        for x in range(self.GRID_W):
            for y in range(self.GRID_H):
                tile = self.tiles[x][y]
                left = x * self.tile_size
                top = y * self.tile_size + 50
                rect = pygame.Rect(left, top, self.tile_size, self.tile_size)
                
                if (x + y) % 2 == 0:
                    revealed_color = settings.COLOR_REVEALED_LIGHT
                    unclicked_color = settings.COLOR_UNCLICKED_LIGHT
                else:
                    revealed_color = settings.COLOR_REVEALED_DARK
                    unclicked_color = settings.COLOR_UNCLICKED_DARK

                tile_color = unclicked_color if tile.clickable else revealed_color
                pygame.draw.rect(self.screen, tile_color, rect)
                
                if self.game_over:
                    if tile.state == 'flower':
                        self.draw_flower(rect, animated=True)
                    elif tile.value == -1:
                        if tile.state == 'mine_hit':
                            pygame.draw.rect(self.screen, settings.COLOR_MINE, rect)
                            self.draw_mine(rect, is_hit=True)
                        elif tile.state == 'flagged':
                            self.draw_flag(rect)
                        else:
                            pygame.draw.rect(self.screen, settings.COLOR_MINE, rect)
                            self.draw_mine(rect, is_hit=False)
                    elif tile.state == 'flagged':
                        self.draw_flag(rect)
                        x_color = (255, 0, 0)
                        x_thickness = 3
                        x_margin = 5
                        pygame.draw.line(self.screen, x_color,
                                       (rect.left + x_margin, rect.top + x_margin),
                                       (rect.right - x_margin, rect.bottom - x_margin),
                                       x_thickness)
                        pygame.draw.line(self.screen, x_color,
                                       (rect.right - x_margin, rect.top + x_margin),
                                       (rect.left + x_margin, rect.bottom - x_margin),
                                       x_thickness)
                    elif not tile.clickable and tile.value > 0:
                        text = str(tile.value)
                        color = settings.NUMBER_COLORS.get(tile.value, settings.COLOR_TEXT)
                        text_surface = self.font_small.render(text, True, color)
                        text_rect = text_surface.get_rect(center=rect.center)
                        self.screen.blit(text_surface, text_rect)
                else:
                    if tile.clickable and tile.state == 'flagged':
                        self.draw_flag(rect)
                    elif not tile.clickable and tile.value > 0:
                        text = str(tile.value)
                        color = settings.NUMBER_COLORS.get(tile.value, settings.COLOR_TEXT)
                        text_surface = self.font_small.render(text, True, color)
                        text_rect = text_surface.get_rect(center=rect.center)
                        self.screen.blit(text_surface, text_rect)
        
    def draw_pop_up(self):
        popup_width = 300
        popup_height = 220
        popup_x = (self.GAME_W - popup_width) // 2
        popup_y = (self.GAME_H - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        
        pygame.draw.rect(self.screen, settings.COLOR_POPUP_BG, popup_rect, border_radius=10)
        pygame.draw.rect(self.screen, settings.COLOR_TEXT, popup_rect, 3, border_radius=10)
        
        title_text = "VICTORY!" if self.game_won else "GAME OVER!"
        title_color = (0, 255, 0) if self.game_won else settings.COLOR_MINE
        title_surface = self.font_popup_title.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(popup_x + popup_width // 2, popup_y + 35))
        self.screen.blit(title_surface, title_rect)

        time_display = "{:.2f}s".format(self.current_time)
        time_text = self.font_popup_text.render(f"Time: {time_display}", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 90))
        self.screen.blit(time_text, time_rect)
        
        if self.game_won:
            best_time_display = "{:.2f}s".format(self.best_time) if self.best_time else "N/A"
            is_new_record = self.best_time is not None and abs(self.current_time - self.best_time) < 0.01
            
            if is_new_record:
                best_time_summary = "🎉 NEW RECORD! 🎉"
                best_color = (255, 215, 0)
            else:
                best_time_summary = f"Best: {best_time_display}"
                best_color = (200, 200, 50)
            
            best_time_text = self.font_popup_text.render(best_time_summary, True, best_color)
            best_time_rect = best_time_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 130))
            self.screen.blit(best_time_text, best_time_rect)

        button_width, button_height = 150, 40
        button_x = popup_x + (popup_width - button_width) // 2
        button_y = popup_y + popup_height - 55
        self.restart_button = pygame.Rect(button_x, button_y, button_width, button_height)
        
        mouse_pos = pygame.mouse.get_pos()
        button_color = settings.COLOR_BUTTON_HOVER if self.restart_button.collidepoint(mouse_pos) else settings.COLOR_BUTTON
        
        pygame.draw.rect(self.screen, button_color, self.restart_button, border_radius=8)
        pygame.draw.rect(self.screen, settings.COLOR_TEXT, self.restart_button, 2, border_radius=8)

        button_label = self.font_popup_text.render("PLAY AGAIN", True, (255, 255, 255))
        label_rect = button_label.get_rect(center=self.restart_button.center)
        self.screen.blit(button_label, label_rect)

    def reset_game(self):
        self.apply_difficulty(self.difficulty_name)

    
