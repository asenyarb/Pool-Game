import sys
import pygame
import time
import threading
from math import sqrt
from cfg import *
from vector import Vector
from ball import *
from utils import *

pygame.display.set_caption('Pool by asenyarb')


def run():
    screen.fill(WHITE)
    pygame.draw.lines(screen, RED, 1,
                      [(BORDER_LEFT, BORDER_TOP), (BORDER_RIGHT, BORDER_TOP), (BORDER_RIGHT, BORDER_BOTTOM),
                       (BORDER_LEFT, BORDER_BOTTOM)], 2)
    window.blit(screen, (0, 0))
    pygame.display.flip()


def start_program() -> None:
    while True:
        for event in pygame.event.get():
            redraw_table()
            mouse_pos = pygame.mouse.get_pos()
            if (mouse_pos[0] > BORDER_LEFT + GRAPHICAL_RADIUS) and (mouse_pos[0] < BORDER_RIGHT - GRAPHICAL_RADIUS) and (mouse_pos[1] > BORDER_TOP + GRAPHICAL_RADIUS) and (mouse_pos[1] < BORDER_BOTTOM - GRAPHICAL_RADIUS):
                pygame.draw.circle(screen, BLACK, mouse_pos, GRAPHICAL_RADIUS, 2)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        superposition: bool = False
                        for ball in BALLS:
                            if find_distance(ball.location, pygame.mouse.get_pos()) <= float(GRAPHICAL_RADIUS * 2):
                                superposition = True
                                break
                        if superposition:
                            continue
                        clack()
                        Ball(True, pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                finish_drawing()
                return
            finish_drawing()
            if event.type == pygame.QUIT:
                sys.exit()


def choosing_a_ball() -> Ball:
    """chooses a ball to be hit"""
    ball_to_choose: Ball = Ball()
    redraw_table()
    finish_drawing()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if ball_to_choose.chosen:
                        for ball2 in BALLS:
                            if ball2.chosen:
                                ball2.chosen = False
                                break
                    for ball in BALLS:
                        if abs(ball.location[0] - pygame.mouse.get_pos()[0]) <= GRAPHICAL_RADIUS and abs(ball.location[1] - pygame.mouse.get_pos()[1]) <= GRAPHICAL_RADIUS:
                            ball.chosen = True
                            ball_to_choose = ball
                redraw_table()
                finish_drawing()
                if pygame.mouse.get_pressed()[2]:
                    if ball_to_choose.chosen:
                        return ball_to_choose
            if event.type == pygame.QUIT:
                print('exit')
                sys.exit()


def choose_hit_destination(chosen_ball: Ball) -> (Vector, [int, int, int, int]):
    """returns a tuple of hit_vector and initial_cue_position"""
    redraw_table()
    finish_drawing()
    while True:
        for event in pygame.event.get():
            redraw_table()
            x0: int = 0
            x1: int = 0
            y0: int = 0
            y1: int = 0
            hit_vector: Vector
            initial_cue_position: [int, int, int, int]
            if event.type == pygame.MOUSEMOTION:
                # Drawing a cue
                hit_vector = Vector(chosen_ball.location[0] - pygame.mouse.get_pos()[0], chosen_ball.location[1] - pygame.mouse.get_pos()[1])
                if hit_vector.y == 0 and hit_vector.x == 0:
                    continue
                if hit_vector.x == 0:
                    k: float = 0
                    y_s = - hit_vector.y / abs(hit_vector.y)
                    sign_x: int = 0
                else:
                    k: float = hit_vector.y / hit_vector.x
                    y_s = 0
                    sign_x: int = int(-hit_vector.x / abs(hit_vector.x))
                temp: float = sqrt(k * k + 1)
                # cue_tip
                x0_f: float = chosen_ball.location[0] + sign_x * (GRAPHICAL_RADIUS + DISTANCE_BTW_BALL_AND_CUE) / temp
                x0: int = int(x0_f)
                y0 = int(k * (x0_f - chosen_ball.location[0]) + chosen_ball.location[1] + y_s * (GRAPHICAL_RADIUS + DISTANCE_BTW_BALL_AND_CUE))
                # cue_tail
                x1_f: float = chosen_ball.location[0] + sign_x * (GRAPHICAL_RADIUS + DISTANCE_BTW_BALL_AND_CUE + CUE_LENGTH) / temp
                x1: int = int(x1_f)
                y1 = int(k * (x1_f - chosen_ball.location[0]) + chosen_ball.location[1] + y_s * (GRAPHICAL_RADIUS + DISTANCE_BTW_BALL_AND_CUE + CUE_LENGTH))
                pygame.draw.line(screen, BLACK, (x0, y0), (x1, y1), 6)
                initial_cue_position = [x0, y0, x1, y1]
                finish_drawing()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    try:
                        hit_vector.normalize()
                        return hit_vector, initial_cue_position
                    except NameError:
                        print("hit vector wasn't assigned!!!")
            if event.type == pygame.QUIT:
                sys.exit()


def wait_for_click(running: [bool]):
    """checks pygame events for a left mouse button to be clicked"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    running[0] = False
                    return
            if event.type == pygame.QUIT:
                running[0] = False
                print('quit')
                sys.exit()


def cue_animation(cue_position: [int, int, int, int], hit_vector: Vector, running: [bool]):
    while running[0]:
        for counter in range(100):
            if not running[0]:
                break
            redraw_table()
            cue_position[0] -= hit_vector.x
            cue_position[1] -= hit_vector.y
            cue_position[2] -= hit_vector.x
            cue_position[3] -= hit_vector.y
            pygame.draw.line(screen, BLACK, (cue_position[0], cue_position[1]), (cue_position[2], cue_position[3]), 6)
            finish_drawing()
        for counter in range(DISTANCE_BTW_BALL_AND_CUE + 100):
            if not running[0]:
                break
            redraw_table()
            cue_position[0] += hit_vector.x
            cue_position[1] += hit_vector.y
            cue_position[2] += hit_vector.x
            cue_position[3] += hit_vector.y
            pygame.draw.line(screen, BLACK, (cue_position[0], cue_position[1]), (cue_position[2], cue_position[3]), 6)
            finish_drawing()
        for counter in range(DISTANCE_BTW_BALL_AND_CUE):
            if not running[0]:
                break
            redraw_table()
            cue_position[0] -= hit_vector.x
            cue_position[1] -= hit_vector.y
            cue_position[2] -= hit_vector.x
            cue_position[3] -= hit_vector.y
            pygame.draw.line(screen, BLACK, (cue_position[0], cue_position[1]), (cue_position[2], cue_position[3]), 6)
            finish_drawing()


def choose_hit_force(chosen_ball: Ball, hit_vector: Vector, cue_position: [int, int, int, int]) -> float:
    """The difference between the cue and the ball ~ the hit force; the function returns the distance btw cue and ball"""
    running: [bool] = [True]
    # cue animation
    th_1 = threading.Thread(target=cue_animation, args=[cue_position, hit_vector, running])
    th_1.start()
    # the function wait_for_click will wait for left mouse button click and then will change running[0] to false
    wait_for_click(running)

    th_1.join()
    # distance retrieving
    distance = sqrt((chosen_ball.location[0] - cue_position[0]) ** 2 + (chosen_ball.location[1] - cue_position[1]) ** 2)
    return distance


def hit(chosen_ball: Ball, hit_vector: Vector, cue_position: [int, int, int, int], distance: float):
    hit_force = distance * 100
    assert(hit_vector.x != 0 or hit_vector.y != 0)
    # hit animation
    to_go: float = distance - GRAPHICAL_RADIUS
    to_go_by_step: float = to_go / 5
    if hit_vector.x == 0:
        k: float = 0
        y_s = - hit_vector.y / abs(hit_vector.y)
        step_x: int = 0
        step_y: int = int(to_go_by_step)
        sign_x: int = 0
    else:
        k: float = hit_vector.y / hit_vector.x
        y_s = 0
        step_x: int = int(to_go_by_step / (k * k + 1))
        step_y: int = int(step_x * k)
        sign_x: int = int(-hit_vector.x / abs(hit_vector.x))
    temp: float = sqrt(k * k + 1)
    # cue_tip
    x0_f: float = chosen_ball.location[0] + sign_x * GRAPHICAL_RADIUS / temp
    x0: int = int(x0_f)
    y0 = int(k * (x0_f - chosen_ball.location[0]) + chosen_ball.location[1] + y_s * GRAPHICAL_RADIUS)
    # cue_tail
    x1_f: float = chosen_ball.location[0] + sign_x * (GRAPHICAL_RADIUS + CUE_LENGTH) / temp
    x1: int = int(x1_f)
    y1 = int(k * (x1_f - chosen_ball.location[0]) + chosen_ball.location[1] + y_s * (GRAPHICAL_RADIUS + CUE_LENGTH))
    for counter in range(4):
        redraw_table()
        cue_position[0] -= step_x
        cue_position[1] -= step_y
        cue_position[2] -= step_x
        cue_position[3] -= step_y
        pygame.draw.line(screen, BLACK, (cue_position[0], cue_position[1]), (cue_position[2], cue_position[3]), 6)
        finish_drawing()
    redraw_table()
    pygame.draw.line(screen, BLACK, (x0, y0), (x1, y1), 6)
    finish_drawing()
    chosen_ball.apply_force(Vector(hit_vector.x * hit_force, hit_vector.y * hit_force))
    chosen_ball.update_velocity()

def check_for_quit(running):
    while running[0]:
        time.sleep(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

def balls_bouncing(running: [bool]):
    in_move:  int = 1
    for a_ball in BALLS:
        if a_ball.chosen:
            a_ball.chosen = False
            break
    while in_move != 0:
        counter = 0
        for a in BALLS:
            counter += 1
            # Border collisions & energy loss (implemented as surface friction)
            if a.location[1] + GRAPHICAL_RADIUS >= BORDER_BOTTOM:
                a.bounce_off_the_board(border=BORDER_BOTTOM, bigger=1, horizontal=0)
            elif a.location[1] - GRAPHICAL_RADIUS <= BORDER_TOP:
                a.bounce_off_the_board(BORDER_TOP, 0, 0)
            if a.location[0] - GRAPHICAL_RADIUS <= BORDER_LEFT:
                a.bounce_off_the_board(BORDER_LEFT, 0, 1)
            elif a.location[0] + GRAPHICAL_RADIUS >= BORDER_RIGHT:
                a.bounce_off_the_board(BORDER_RIGHT, 1, 1)


            # Processing collisions
            for b in BALLS[counter:]:
                if find_distance(a.location, b.location) <= GRAPHICAL_RADIUS * 2:
                    in_move += a.collide(b)

            # Surface friction
            if a.velocity.magnitude() > SURFACE_FRICTION * MOTION_SPEED / (1000 * a.mass):
               a.friction(SURFACE_FRICTION)
            elif a.velocity.magnitude() != 0:
                a.velocity = Vector()
                in_move -= 1
            a.update()
        redraw_table(False)
        for a in BALLS:
            a.render(BLACK)
        finish_drawing()
        running[0] = False


if __name__=="__main__":
    run()
    #start_program()
    Ball(True, [20,20]).velocity = Vector(200, 200)
    Ball(True, [100,110]).velocity = Vector(-20, 20)
    Ball(True, [205,302]).velocity = Vector(201, -20)
    while True:
        #ball: Ball = choosing_a_ball()
        #vector, cue_pos = choose_hit_destination(ball)
        #force = choose_hit_force(ball, vector, cue_pos)
        #hit(ball, vector, cue_pos, force)
        runnin=[True]
        th1 = threading.Thread(target=balls_bouncing, args=runnin)
        th1.start()
        check_for_quit(runnin)
        th1.join()
