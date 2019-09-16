from cfg import *
import pygame
from math import *
import wave
from ball import *
from vector import Vector
from values import *


# WINDOW
window = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface((WIDTH, HEIGHT))
table = screen.subsurface(pygame.Rect(BORDER_LEFT + 2, BORDER_TOP + 2, WIDTH - BORDER_WIDTH * 1000 * 2 - 2, HEIGHT - BORDER_WIDTH * 1000 * 2 - 2))
table_offset = table.get_offset()

# SOUND
pygame.mixer.init(frequency=wave.open('Clack.wav').getframerate())
clack_s = pygame.mixer.Sound("Clack.wav")

ORIGIN = Vector()


def clack():
    """Produces a clack sound"""
    pygame.mixer.Sound.play(clack_s)


def font(size):
    """Changes the size of the font"""
    return pygame.font.SysFont('Verdana', size)


def normalize_vector(vector: [int, int]):
    magnitude: float = sqrt(float(vector[0] * vector[0] + vector[1] * vector[1]))
    vector[0] /= magnitude
    vector[1] /= magnitude


def find_distance(p1: (int, int), p2: (int, int)) -> float:
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def redraw_table(draw_balls=True):
    screen.fill(WHITE)
    pygame.draw.lines(screen, RED, 1,
                      [(BORDER_LEFT, BORDER_TOP), (BORDER_RIGHT, BORDER_TOP), (BORDER_RIGHT, BORDER_BOTTOM),
                       (BORDER_LEFT, BORDER_BOTTOM)], 2)
    if draw_balls:
        for ball in BALLS:
            ball.render(BLACK)


def finish_drawing():
    window.blit(screen, (0, 0))
    pygame.display.flip()
