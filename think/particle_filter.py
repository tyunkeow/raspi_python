# coding=utf-8
from math import *
import random
import numpy as np
import time
from profilehooks import profile

DEFAULT_WORLD_SIZE = (100., 100.)


# Wahrscheinlichkeit für x bei Gausscher Verteilung mit Mittelwert mu und
# Standardabweichung sigma (Varianz = sigma**2
def gaussian(mu, sigma, x):
    # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
    return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))


# Wahrscheinlichkeitsverteilung für diskrete n (integer) aus einem Intervall 0..N
class DiscreteDistribution:
    # prob n = weights[n]/sum(weights)
    def __init__(self, weights, values=None):
        self.weights = weights  # array
        if values is None:
            self.values = xrange(len(weights))
        else:
            assert len(values) == len(weights)
            self.values = values
        self.max_weight = max(weights)
        self.normalizer = sum(weights)
        print "Sum of weigths=", self.normalizer

    def probability(self, n):
        return self.weights[n] / self.normalizer

    @profile
    def sample1(self, j):
        n = len(self.weights)
        print "Resampling {} elements ...".format(n)
        t1 = time.clock()

        # wheel
        # biased? see http://forums.udacity.com/questions/3001328/an-on-unbiased-resampler#cs373
        result = []
        index = int(floor(random.random() * n))
        b = 0
        for i in range(j):
            b += random.random() * self.max_weight
            while self.weights[index] < b:
                b -= self.weights[index]
                index = (index + 1) % n
            result.append(self.values[index])
        t2 = time.clock()
        print "Time for computing sample: ", round(t2-t1, 10)

        return result

    @profile
    def sample2(self, j):
        nw = [x / float(self.normalizer) for x in self.weights] #An array of the weights, cumulatively summed.
        #print nw
        cs = np.cumsum(nw)
        #print "cs", cs

        result = []
        for i in range(j):
            index = sum(cs < random.random()) #Find the index of the first weight over a random value.
            result.append(self.values[index])
        return result

# compute estimated robot position from a particle set
def get_robot_position(p):
    x = 0.0
    y = 0.0
    orientation = 0.0
    for i in range(len(p)):
        x += p[i].x
        y += p[i].y
        # orientation is tricky because it is cyclic. By normalizing
        # around the first particle we are somewhat more robust to
        # the 0=2pi problem
        orientation += (((p[i].orientation - p[0].orientation + pi) % (2.0 * pi))
                        + p[0].orientation - pi)
    return [x / len(p), y / len(p), orientation / len(p)]


class Point(object):
    def __init__(self, x=None, y=None, world_size=DEFAULT_WORLD_SIZE):
        if x is None:
            x = random.random() * world_size[0]
        self.x = int(x)
        if y is None:
            y = random.random() * world_size[1]
        self.y = int(y)
        self.world_size = world_size

    # Abstand der Startpunkte
    def distance(self, arrow):
        return sqrt((self.x - arrow.x) ** 2 + (self.y - arrow.y) ** 2)


class Arrow(Point):
    def __init__(self, x=None, y=None, orientation=None, world_size=DEFAULT_WORLD_SIZE):
        super(Arrow, self).__init__(x, y, world_size)
        if orientation is None:
            orientation = random.random() * 2.0 * pi
        self.orientation = orientation

    # copy constructor
    def copy_to(self, arrow):
        arrow.x = self.x
        arrow.y = self.y
        arrow.orientation = self.orientation
        arrow.world_size = self.world_size
        return arrow

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

    def move(self, turn, forward):

        self.orientation += float(turn)
        self.orientation %= 2 * pi

        dist = float(forward)
        self.x += int(cos(self.orientation) * dist)
        self.y += int(sin(self.orientation) * dist)
        self.x %= self.world_size[0]    # cyclic truncate
        self.y %= self.world_size[1]
        return self

    #
    # Liefert Vector v = [v1, v2] fuer den gilt
    # self.move(0, v1).x = arrow.move(0, v2).x
    # und
    # self.move(0, v1).x = arrow.move(0, v2).x
    #
    def collision_vector(self, arrow):
        a = np.array(
            [[cos(self.orientation), - cos(arrow.orientation)], [sin(self.orientation), -sin(arrow.orientation)]])
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
    def __init__(self, x=None, y=None, orientation=None, world_size=DEFAULT_WORLD_SIZE):
        super(BaseRobot, self).__init__(x, y, orientation, world_size)
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise)
        self.turn_noise = float(new_t_noise)
        self.sense_noise = float(new_s_noise)

    def move(self, turn, forward):
        if forward < 0:
            raise ValueError, 'Robot cant move backwards'

        # add noise, then delegate to superclass
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

