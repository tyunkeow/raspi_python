
from math import *
import random
import numpy as np

DEFAULT_WORLD_SIZE = 100.


def gaussian(mu, sigma, x):

    # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
    return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))


class Point(object):
    def __init__(self, x=None, y=None, world_size=DEFAULT_WORLD_SIZE):
        if x is None:
            x = random.random() * world_size
        self.x = x
        if y is None:
            y = random.random() * world_size
        self.y = y
        self.world_size = world_size

    # Abstand der Startpunkte
    def distance(self, arrow):
        return sqrt((self.x - arrow.x) ** 2 + (self.y - arrow.y) ** 2)


class Arrow(Point):
    def __init__(self, x=None, y=None, o=None, world_size=DEFAULT_WORLD_SIZE):
        super(Arrow, self).__init__(x, y, world_size)
        if o is None:
            o = random.random() * 2.0 * pi
        self.orientation = o

    # copy constructor
    def copy_to(self, arrow):
        arrow.x = self.x
        arrow.y = self.y
        arrow.orientation = self.orientation
        arrow.world_size = self.world_size
        return arrow

    def move(self, turn, forward):

        self.orientation += float(turn)
        self.orientation %= 2 * pi

        dist = float(forward)
        self.x += (cos(self.orientation) * dist)
        self.y += (sin(self.orientation) * dist)
        self.x %= self.world_size    # cyclic truncate
        self.y %= self.world_size
        return self

    #
    # Liefert Vector v = [v1, v2] fuer den gilt
    # self.move(0, v1).x = arrow.move(0, v2).x
    # und
    # self.move(0, v1).x = arrow.move(0, v2).x
    #
    def collision_vector(self, arrow):
        a = np.array([[cos(self.orientation), - cos(arrow.orientation)], [sin(self.orientation), -sin(arrow.orientation)]])
        b = np.array([[arrow.x - self.x], [arrow.y - self.y]])
        #print a
        #print b
        try:
            v = np.linalg.solve(a, b)
            #print "v=" + str(v)
            return v
        except np.linalg.LinAlgError as e:
            #print e
            return None, None

    # liefert Koordinaten des Schnittpunkts
    def intersect(self, arrow):
        #print self.collision_vector(arrow)
        (v1, v2) = self.collision_vector(arrow)
        if v1 is None:
            return None, None
        else:
            arr = Arrow()
            self.copy_to(arr)
            arr.move(0, v1)
            return arr.x, arr.y

    def __repr__(self):
        return 'Arrow[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))


class BaseRobot(Arrow):
    def __init__(self, x=None, y=None, o=None, world_size=DEFAULT_WORLD_SIZE):
        super(BaseRobot, self).__init__(x, y, o, world_size)
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0

    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= self.world_size:
            raise ValueError, 'X coordinate out of bound'
        if new_y < 0 or new_y >= self.world_size:
            raise ValueError, 'Y coordinate out of bound'
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise)
        self.turn_noise = float(new_t_noise)
        self.sense_noise = float(new_s_noise)

    def move(self, turn, forward):
        if forward < 0:
            raise ValueError, 'Robot cant move backwards'

        turn = float(turn) + random.gauss(0.0, self.turn_noise)
        forward = float(forward) + random.gauss(0.0, self.forward_noise)
        return super(BaseRobot, self).move(turn, forward)

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))

    # copy constructor
    def copy_to(self, base_robot):
        super(BaseRobot, self).copy_to(base_robot)
        base_robot.forward_noise = self.forward_noise
        base_robot.turn_noise = self.turn_noise
        base_robot.sense_noise = self.sense_noise
        return base_robot

    def eval_mean_error(self, p):
        sum = 0.0
        for i in range(len(p)):  # calculate mean error
            dx = (p[i].x - self.x + (self.world_size / 2.0)) % self.world_size - (self.world_size / 2.0)
            dy = (p[i].y - self.y + (self.world_size / 2.0)) % self.world_size - (self.world_size / 2.0)
            err = sqrt(dx * dx + dy * dy)
            sum += err
        return sum / float(len(p))


if __name__ == "__main__":
    robot = BaseRobot()
    robot.set_noise(0.1, 0.2, 5)

    T = 5

    for j in range(T):
        turn = random.random() * 2*pi
        forward = random.random() * 25
        robot.move(turn, forward)
        print robot

    arrow = Arrow(50, 50, pi/2)
    print arrow
    assert arrow.x == 50
    assert arrow.y == 50
    assert arrow.orientation == pi/2

    wall_x = Arrow(0, 0, 0)  # == X-Achse
    wall_y = Arrow(0, 0, pi/2)  # == Y-Achse

    cv = (cv1, cv2) = arrow.collision_vector(wall_x)
    assert cv1 == -50
    assert cv2 == 50

    print "wall1 collision_vector:    {}".format(cv)
    #print "wall2 collision_vector:     {}".format(arrow.collision_vector(wall2))

    (x, y) = schnittp_x = arrow.intersect(wall_x)
    assert x == 50
    assert y == 0
    print "wall1 intersection:    {}".format(schnittp_x)

    (x, y) = schnittp_y = arrow.intersect(wall_y)
    assert x is None
    assert y is None
    print "wall1 intersection:    {}".format(schnittp_y)
