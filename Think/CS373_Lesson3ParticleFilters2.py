# In this exercise, try to write a program that
# will resample particles according to their weights.
# Particles with higher weights should be sampled
# more frequently (in proportion to their weight).

# Don't modify anything below. Please scroll to the
# bottom to enter your code.

from math import *
import random
from ParticleFilter import Arrow, BaseRobot, gaussian, DEFAULT_WORLD_SIZE
from RobotWindow import Window

landmarks = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]


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
            prob *= gaussian(dist, self.sense_noise, measurement[i])
        return prob


class Robot2(BaseRobot):
    def __init__(self, x=None, y=None, o=None, world_size=DEFAULT_WORLD_SIZE):
        super(Robot2, self).__init__(x, y, o, world_size)
        self.wall_x = Arrow(0, 0, 0)  # == X-Achse
        self.wall_y = Arrow(0, 0, pi/2)  # == Y-Achse

    def distance_from_wall(self):
        (dx1, dx2) = self.collision_vector(self.wall_x)
        (dy1, dy2) = self.collision_vector(self.wall_y)
        return min(dx1, dy1)

    def sense(self):
        return self.distance_from_wall() + random.gauss(0.0, self.sense_noise)

    def measurement_prob(self, measurement):

        # calculates how likely a measurement should be

        prob = 1.0
        dist = self.distance_from_wall()
        prob *= gaussian(dist, self.sense_noise, measurement)
        return prob


class Simulator(object):
    def __init__(self, robot, N=10000):
        self.win = Window()
        self.robot = robot
        self.N = N
        self.p = []
        for i in range(self.N):
            r = Robot2()
            r.set_noise(0.1, 0.2, 1)
            self.p.append(r)

    def show_generation(self):
        self.win.dots([(robot.x, robot.y) for robot in self.p])
        self.win.dot_red(self.robot.x, self.robot.y)
        self.win.show()

    def simulate(self):
        self.show_generation()

        T = 40

        for j in range(T):
            turn = random.random() * 2 * pi
            forward = random.random() * 25
            myrobot.move(turn, forward)

            #p = [robot.move(turn, forward) for robot in p]
            for robot in self.p:
                robot.move(turn, forward)

            self.show_generation()

            Z = myrobot.sense()
            w = []
            for i in range(self.N):
                w.append(self.p[i].measurement_prob(Z))

            # wheel
            # biased? see http://forums.udacity.com/questions/3001328/an-on-unbiased-resampler#cs373
            w_max = max(w)
            p3 = []
            index = int(floor(random.random() * self.N))
            b = 0
            for i in range(self.N):
                b += random.random() * w_max
                while w[index] < b:
                    b -= w[index]
                    index = (index + 1) % self.N
                p3.append(self.p[index].copy_to(Robot2()))

            self.p = p3
            self.show_generation()


myrobot = Robot2()

sim = Simulator(myrobot, 1000)

sim.simulate()

