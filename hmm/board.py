import pygame

pygame.init()

from .constants import HEIGHT, WIDTH, BLACK, YELLOW1, YELLOW2, RED, GRAY, GREEN, BLUE, WHITE
 
 
class Board:
    def __init__(self, win, rows, cols):
        self.win = win
        self.rows = rows
        self.cols = cols
        self.row_size = HEIGHT // (rows+1)
        self.col_size = WIDTH // cols

    def draw_rect(self, row, col, clr):
        pygame.draw.rect(self.win, clr, (col*self.col_size, row *self.row_size, 
            self.col_size, self.row_size)) 
    
    def draw_prob(self, row, col, prob):
        prob = round(prob, 3) 
        font = pygame.font.SysFont('didot.ttc', 25)
        img = font.render(str(prob), True, BLACK)
        self.win.blit(img, (self.col_size*col + self.col_size // 2 - 20,
            self.row_size*row + self.row_size // 2 - 20))
                   
    def draw_time_catch(self):
        self.draw_rect(self.rows,0, BLUE)
        self.draw_rect(self.rows,self.cols-1, WHITE)

        font = pygame.font.SysFont('didot.ttc', 25)
        img = font.render('TIME', True, BLACK)
        self.win.blit(img, (self.col_size*0 + self.col_size // 2 - 20,
            self.row_size*self.rows + self.row_size // 2 - 20))

        font = pygame.font.SysFont('didot.ttc', 25)
        img = font.render('CATCH', True, BLACK)
        self.win.blit(img, (self.col_size*(self.cols-1) + self.col_size // 2 - 20,
            self.row_size*self.rows + self.row_size // 2 - 20))

    def show_result(self, res):
        font = pygame.font.SysFont('didot.ttc', 25)
        img = font.render(res, True, WHITE)
        self.win.blit(img, (self.col_size + self.col_size // 2 - 20,
            self.row_size*self.rows + self.row_size // 2 - 20))

    def clr_res(self):
        self.draw_rect(self.rows, 1, BLACK)



    


    