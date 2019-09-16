from cfg import *

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTGREY = (155, 155, 155)


# BORDERS
BORDER_BOTTOM = HEIGHT - BORDER_WIDTH * 1000
BORDER_TOP = BORDER_WIDTH * 1000
BORDER_LEFT = BORDER_WIDTH * 1000
BORDER_RIGHT = WIDTH - BORDER_WIDTH * 1000

# DISTANCES
DISTANCE_BTW_BALL_AND_CUE = 16
CUE_LENGTH = 400
SCALE_COEFFICIENT = 1300 * SCALE
GRAPHICAL_RADIUS = int(RADIUS * SCALE_COEFFICIENT)

BALLS = []