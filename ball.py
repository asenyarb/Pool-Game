from cfg import *
from vector import Vector
from utils import *


class Ball:
    location: [int, int]
    radius: float
    mass: float
    velocity: Vector
    force: Vector
    impulse: Vector
    graphical_radius: int
    chosen: bool

    def __init__(self, add_to_balls_array: bool = False, location: (int, int) = (0, 0)):
        # Ball properties
        self.location = list(location)
        self.mass = MASS
        self.radius = RADIUS
        # Dynamics
        self.velocity = Vector()
        self.force = Vector()
        self.impulse = Vector()
        self.graphical_radius = int(RADIUS * SCALE_COEFFICIENT)
        self.chosen = False
        # General
        if add_to_balls_array:
            BALLS.append(self)

    def __str__(self):
        return 'Ball:\n\tvelocity:' + str(self.velocity)

    @property
    def location_point(self):
        return (int(self.location[0]), int(self.location[1]))

    def apply_force(self, force: Vector):
        """Applies certain force to an object."""
        self.force += force

    def impulse_vector(self):
        """Calculates an impulse of an object."""
        return self.velocity * self.mass

    def kinetic_energy(self):
        return self.mass * (self.velocity.x ** 2 + self.velocity.y ** 2) / 2  # ==self.velocity.magnitude**2 / 2

    # def potential_energy(self):
    # return (self.location.y - border_bot) * self.mass * cfg.G

    def energy(self):
        return self.kinetic_energy()  # + self.potential_energy()

    def update_velocity(self):
        """Updates body's velocity and forces."""
        self.velocity += self.force * MOTION_SPEED / (1000 * self.mass)
        self.force = Vector()

    def update(self):
        """Fully updates object's state."""
        self.update_velocity()
        self.location[0] += int(self.velocity.x * MOTION_SPEED / 10)
        self.location[1] += int(self.velocity.y * MOTION_SPEED / 10)

    def friction(self, magnitude):
        """Applies a force with a given magnitude directing backwards relative to the current velocity."""
        friction = self.velocity.copy()     # The main goal is to get direction
        friction.set_magnitude(-magnitude)
        self.apply_force(friction)

    def two_moving_balls_collision(self, other_ball):
        self_mass_coeff = (2 * other_ball.mass) / (self.mass + other_ball.mass)
        other_mass_coeff = (2 * self.mass) / (self.mass + other_ball.mass)

        self_center = Vector(self.location[0], self.location[1])
        other_ball_center = Vector(other_ball.location[0], other_ball.location[1])

        self_delta_distance_vector = self_center - other_ball_center
        other_delta_distance_vector = other_ball_center - self_center

        distance_square = (self_center - other_ball_center).magnitude() ** 2

        self.velocity = self.velocity - self_delta_distance_vector * (
                self_mass_coeff * (self.velocity - other_ball.velocity).dot(
            self_delta_distance_vector) / distance_square)

        other_ball.velocity = other_ball.velocity - other_delta_distance_vector * (
                other_mass_coeff * (other_ball.velocity - self.velocity).dot(
            other_delta_distance_vector) / distance_square)

    def one_moving_ball_collision(moving_ball, staying_ball):
        delta_location_vector = Vector(staying_ball.location[0] - moving_ball.location[0], -(staying_ball.location[1] - moving_ball.location[1]))
        angle = acos(delta_location_vector.dot(Vector(1,0)) / delta_location_vector.magnitude())

        staying_mass_coeff = (2 * moving_ball.mass / (moving_ball.mass + staying_ball.mass) *
                              sin(angle/2))
        moving_mass_coeff = sqrt(moving_ball.mass ** 2 + staying_ball.mass ** 2 + 2 *
                                 moving_ball.mass * staying_ball.mass * cos(angle)) / (
                                    moving_ball.mass + staying_ball.mass)
        print("\nBefore collision:\nStaying ball:\nx: ", staying_ball.velocity.x, "\ny: ", staying_ball.velocity.y)
        print("Moving ball:\nx: ", moving_ball.velocity.x, "\ny: ", moving_ball.velocity.y)
        print("\nAngle: ", angle)
        staying_ball.velocity = moving_ball.velocity * staying_mass_coeff
        moving_ball.velocity = moving_ball.velocity * moving_mass_coeff
        print("\nAfter collision:\nStaying ball:\nx: ", staying_ball.velocity.x, "\ny: ", staying_ball.velocity.y)
        print("Moving ball:\nx: ", moving_ball.velocity.x, "\ny: ", moving_ball.velocity.y, "\n\n")

    def bounce_off_the_board(self, border, bigger, horizontal):
        """Applies bounce force. Literally flips object's speed around certain axis
        (specified by horizontal/vertical values). Used to bounce off the walls & floor."""
        if horizontal:
            self.location[0] = border
            self.location[0] -= GRAPHICAL_RADIUS if bigger else -GRAPHICAL_RADIUS
            self.velocity = Vector(-self.velocity.x, self.velocity.y)
        else:
            self.location[1] = border
            self.location[1] -= GRAPHICAL_RADIUS if bigger else -GRAPHICAL_RADIUS
            self.velocity = Vector(self.velocity.x, -self.velocity.y)
        clack()

    def collide(self, other_ball) -> int:
        in_move_beginning = 0
        if self.velocity.magnitude():
            in_move_beginning += 1
        if other_ball.velocity.magnitude():
            in_move_beginning += 1

        delta: Vector = Vector(self.location[0] - other_ball.location[0], self.location[1] - other_ball.location[1])
        d: float = delta.magnitude()

        # Repositioning balls
        if delta.x:
            k = -delta.y/delta.x
            new_delta = Vector()
            new_delta.x = (GRAPHICAL_RADIUS * 2) / sqrt(k*k + 1)
            new_delta.y = -k * new_delta.x
            other_ball.location[0] = self.location[0] + new_delta.x
            other_ball.location[1] = self.location[1] + new_delta.y
        else:
            other_ball.location[0] = self.location[0]
            other_ball.location[1] = self.location[1] + delta.y

        if in_move_beginning == 2:
            self.two_moving_balls_collision(other_ball)
        elif self.velocity.magnitude():
            self.one_moving_ball_collision(other_ball)
        else:
            other_ball.one_moving_ball_collision(self)
        clack()

        in_move_end = 0
        if self.velocity.magnitude() != 0:
            in_move_end += 1
        if other_ball.velocity.magnitude() != 0:
            in_move_end += 1
        in_move_change = in_move_end - in_move_beginning
        return in_move_change

    def render(self, color):
        """Renders a as a ball of a given color.
        Attaches a velocity vector (multiplied by 15 for better visuals)."""
        if self.chosen:
            pygame.draw.circle(screen, color, self.location_point, self.graphical_radius, 4)
        else:
            pygame.draw.circle(screen, color, self.location_point, self.graphical_radius, 1)
        # (self.velocity * 15).render(self.location, RED)
