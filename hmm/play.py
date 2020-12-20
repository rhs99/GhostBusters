import pygame
pygame.init()

from hmm.game import Game
from .constants import HEIGHT, WIDTH, BLACK, YELLOW1, YELLOW2, RED, GRAY, GREEN
 
 
class Play:
    def __init__(self, win, rows, cols):
        self.win = win
        self.win.fill(BLACK)
        self.FPS = 60
        self.rows = rows
        self.cols = cols
        self.row_size = HEIGHT // (rows+1)
        self.col_size = WIDTH // cols
  

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        row = y // self.row_size
        col = x // self.col_size
        return row, col


    def start_playing(self):
        run = True
        clock = pygame.time.Clock()

        game = Game(self.win, self.rows, self.cols)


        while run:

            clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_row_col_from_mouse(pos)
                    game.handle_click(row, col)
                    
                    # print(row, col)
                
                game.show_prob()

                pygame.display.update()