import os
import pygame
import pygame_menu

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

 
from hmm.play import Play

HEIGHT = 1000
WIDTH = 900
rows = 6
cols = 6
square_size = WIDTH // cols
 

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GhostBusters')

 
def change_row_size(value):
     global rows, cols, square_size
     rows = int(value)

def change_col_size(value):
     global rows, cols, square_size
     cols = int(value)
     square_size = WIDTH // cols

def start_the_game():
    play = Play(win, rows, cols)
    play.start_playing()



menu = pygame_menu.Menu(height=600,
                        width=600,
                        theme=pygame_menu.themes.THEME_BLUE,
                        title='Welcome')

menu.add_text_input('Row : ', onchange= change_row_size)
menu.add_text_input('Col : ', onchange= change_col_size)

menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

 



if __name__ == '__main__':
    menu.mainloop(win)