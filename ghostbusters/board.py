"""Drawing primitives for the grid and the control bar below it."""

import pygame

from .constants import BLACK, BLUE, HEIGHT, WHITE, WIDTH


class Board:
    """Knows how to map grid cells to pixels and draw things in them.

    The window holds ``rows + 1`` rows: the last one is the control bar
    with the TIME button on the left and the CATCH button on the right.
    """

    FONT_SIZE = 25

    def __init__(self, win: pygame.Surface, rows: int, cols: int):
        self.win = win
        self.rows = rows
        self.cols = cols
        self.cell_w = WIDTH // cols
        self.cell_h = HEIGHT // (rows + 1)
        self.font = pygame.font.SysFont("didot.ttc", self.FONT_SIZE)

    def cell_rect(self, row: int, col: int) -> pygame.Rect:
        return pygame.Rect(col * self.cell_w, row * self.cell_h, self.cell_w, self.cell_h)

    def cell_at(self, pos) -> tuple:
        """Grid coordinates (row, col) of a pixel position."""
        x, y = pos
        return y // self.cell_h, x // self.cell_w

    def draw_cell(self, row: int, col: int, colour, label: str = "", text_colour=BLACK) -> None:
        rect = self.cell_rect(row, col)
        pygame.draw.rect(self.win, colour, rect)
        if label:
            self.draw_text(rect, label, text_colour)

    def draw_text(self, rect: pygame.Rect, text: str, colour) -> None:
        img = self.font.render(text, True, colour)
        self.win.blit(img, img.get_rect(center=rect.center))

    def draw_controls(self, message: str = "") -> None:
        self.draw_cell(self.rows, 0, BLUE, "TIME")
        self.draw_cell(self.rows, self.cols - 1, WHITE, "CATCH")
        if message:
            self.draw_text(self.cell_rect(self.rows, 1), message, WHITE)
