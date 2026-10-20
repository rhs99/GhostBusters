"""Start-up menu and application entry point."""

import os
import sys

import pygame
import pygame_menu

from .constants import (
    DEFAULT_COLS,
    DEFAULT_ROWS,
    HEIGHT,
    MAX_COLS,
    MAX_ROWS,
    MIN_COLS,
    MIN_ROWS,
    WIDTH,
)
from .play import Play


def clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def main() -> None:
    os.environ.setdefault("SDL_VIDEO_CENTERED", "1")
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("GhostBusters")

    menu = pygame_menu.Menu("GhostBusters", 600, 600, theme=pygame_menu.themes.THEME_BLUE)
    rows_input = menu.add.text_input(
        "Rows: ", default=DEFAULT_ROWS, input_type=pygame_menu.locals.INPUT_INT, maxchar=2
    )
    cols_input = menu.add.text_input(
        "Cols: ", default=DEFAULT_COLS, input_type=pygame_menu.locals.INPUT_INT, maxchar=2
    )

    def start_game() -> None:
        rows = clamp(rows_input.get_value(), MIN_ROWS, MAX_ROWS)
        cols = clamp(cols_input.get_value(), MIN_COLS, MAX_COLS)
        rows_input.set_value(rows)
        cols_input.set_value(cols)
        back_to_menu = Play(win, rows, cols).run()
        if not back_to_menu:
            pygame.quit()
            sys.exit(0)

    menu.add.button("Play", start_game)
    menu.add.button("Quit", pygame_menu.events.EXIT)
    menu.add.label(f"Rows {MIN_ROWS}-{MAX_ROWS}, cols {MIN_COLS}-{MAX_COLS}. Esc returns here.", font_size=18)

    menu.mainloop(win)


if __name__ == "__main__":
    main()
