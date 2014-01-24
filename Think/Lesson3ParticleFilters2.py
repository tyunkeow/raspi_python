# In this exercise, try to write a program that
# will resample particles according to their weights.
# Particles with higher weights should be sampled
# more frequently (in proportion to their weight).

# Don't modify anything below. Please scroll to the
# bottom to enter your code.

from math import *
import random
import numpy as np
from visual import BeliefsMapStr
from RobotWindow import Window

landmarks = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0


def Gaussian(mu, sigma, x):

    # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
    return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))


class Arrow:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi

    # copy constructor
    def copy(self):
        result = Arrow()
        result.x = self.x
        result.y = self.y
        result.orientation = self.orientation
        return result

    def move(self, turn, forward):

        self.orientation += float(turn)
        self.orientation %= 2 * pi

        dist = float(forward)
        self.x += (cos(self.orientation) * dist)
        self.y += (sin(self.orientation) * dist)
        self.x %= world_size    # cyclic truncate
        self.y %= world_size

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
        v = np.linalg.solve(a, b)
        print v
        return "v=" + str(v)

    def intersect(self, arrow):
        (v1, v2) = self.collision_vector(arrow)
        arr = self.copy()
        arr.move(0, v1)
        return arr.x, arr.y

    def __repr__(self):
        return 'Arrow[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))


class BaseRobot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0

    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError, 'X coordinate out of bound'
        if new_y < 0 or new_y >= world_size:
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

        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi

        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size    # cyclic truncate
        y %= world_size

        # set particle
        res = Robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))


class Robot(BaseRobot):
    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z

    def measurement_prob(self, measurement):

        # calculates how likely a measurement should be

        prob = 1.0
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= Gaussian(dist, self.sense_noise, measurement[i])
        return prob


def eval(r, p):
    sum = 0.0
    for i in range(len(p)):  # calculate mean error
        dx = (p[i].x - r.x + (world_size / 2.0)) % world_size - (world_size / 2.0)
        dy = (p[i].y - r.y + (world_size / 2.0)) % world_size - (world_size / 2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))

def show_generation(myrobot):
    win.dots([(robot.x, robot.y) for robot in p])
    win.dot_red(myrobot.x, myrobot.y)
    win.show()


arrow1 = Arrow()
arrow2 = Arrow()
(r1, r2) = arrow1.collision_vector(arrow2)
arrow1.move(0, r1)
arrow2.move(0, r2)
print arrow1
print arrow2
print arrow1.intersect(arrow2)
print ".................."

myrobot = Robot()

N = 1000
p = []
for i in range(N):
    x = Robot()
    x.set_noise(0.05, 0.05, 5.0)
    p.append(x)

win = Window()
show_generation(myrobot)

T = 40

for j in range(T):
    turn = random.random() * 2*pi
    forward = random.random() * 25
    myrobot = myrobot.move(turn, forward)

    p = [robot.move(turn, forward) for robot in p]
    show_generation(myrobot)

    Z = myrobot.sense()
    w = []
    for i in range(N):
        w.append(p[i].measurement_prob(Z))

    w_max = max(w)
    p3 = []
    index = int(floor(random.random() * N))
    b = 0
    for i in range(N):
        b += random.random() * w_max
        while w[index] < b:
            b -= w[index]
            index = (index + 1) % N
        p3.append(p[index])

    p = p3
    show_generation(myrobot)

print p #please leave this print statement here for grading!