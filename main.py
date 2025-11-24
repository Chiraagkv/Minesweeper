import pygame
import sys
import time
from game_logic import initialise, reveal_tile, flag_tile
import settings
from board import MineSweeperBoard
import file_manager

class MineSweeperGame(MineSweeperBoard):
    def __init__(self):
        super().__init__()
    def handle_click(self, pos, button):
        x, y = pos

        if self.game_over:
            if self.restart_button and self.restart_button.collidepoint(pos) and button == 1:
                self.reset_game()
            return

        if button == 1:
            if self.dropdown_active:
                clicked_difficulty = None
                for name, rect in self.dropdown_options_rects.items():
                    if rect.collidepoint(pos):
                        clicked_difficulty = name
                        break
                
                if clicked_difficulty:
                    self.apply_difficulty(clicked_difficulty)
                    return
                else:
                    if not self.dropdown_box or not self.dropdown_box.collidepoint(pos):
                        self.dropdown_active = False
            
            if self.dropdown_box and self.dropdown_box.collidepoint(pos):
                self.dropdown_active = not self.dropdown_active
                return

        col = x // self.tile_size
        row = (y - 50) // self.tile_size
        
        if not (0 <= col < self.GRID_W and 0 <= row < self.GRID_H):
            return

        tile = self.tiles[col][row]
        
        if self.is_initial_click:
            if button == 1:
                if not self.music_started:
                    try:
                        pygame.mixer.music.play(-1)
                        self.music_started = True
                    except:
                        pass
                
                self.tiles, seed = initialise(self.tiles, tile, self.mc)
                file_manager.save_game_seed(seed)

                
                self.is_initial_click = False
                self.start_time = time.time()
                self.timer_running = True
                
                if tile.value > 0 and tile.clickable:
                    tile.clickable = False
                    tile.state = 'revealed'
            return

        if button == 1:
            if tile.state == 'flagged':
                return
            
            result = reveal_tile(self.tiles, tile)
            if result == "mine":
                if self.boom:
                    self.boom.play()
                self.game_over = True
                self.timer_running = False
            else:
                self.check_win()
        
        elif button == 3:
            if self.sound_flag:
                self.sound_flag.play()
            flag_tile(tile)
            self.update_mine_counter()
        
    def run(self):
        running = True
        while running:
            if self.timer_running and not self.game_over:
                self.current_time = time.time() - self.start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos, event.button)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                
            self.screen.fill(settings.COLOR_REVEALED_LIGHT)
            self.draw_board()
            self.draw_status_bar()
            
            if self.game_over:
                self.draw_pop_up()
            else:
                 self.restart_button = None 

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = MineSweeperGame()
    game.run()