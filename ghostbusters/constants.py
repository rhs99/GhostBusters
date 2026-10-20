"""Window geometry, board limits and colours shared by the UI code."""

WIDTH = 900
HEIGHT = 1000
FPS = 60

DEFAULT_ROWS = 6
DEFAULT_COLS = 6
MIN_ROWS, MAX_ROWS = 2, 15
# The bottom control bar needs three columns: TIME, message, CATCH.
MIN_COLS, MAX_COLS = 3, 15

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 140, 0)
GRAY = (200, 200, 200)
YELLOW1 = (255, 204, 153)
YELLOW2 = (255, 178, 102)
