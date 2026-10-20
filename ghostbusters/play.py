"""The in-game event loop."""

import pygame

from .constants import FPS
from .game import Game


class Play:
    def __init__(self, win: pygame.Surface, rows: int, cols: int):
        self.win = win
        self.game = Game(win, rows, cols)

    def run(self) -> bool:
        """Run until the player leaves.

        Returns True when the player pressed Esc (go back to the menu) and
        False when they closed the window (quit the app).
        """
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    row, col = self.game.board.cell_at(event.pos)
                    self.game.handle_click(row, col)

            self.game.draw()
            pygame.display.update()
            clock.tick(FPS)
