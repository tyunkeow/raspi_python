# In this exercise, try to write a program that
# will resample particles according to their weights.
# Particles with higher weights should be sampled
# more frequently (in proportion to their weight).

# Don't modify anything below. Please scroll to the
# bottom to enter your code.

from math import *
import random
from think.particle_filter import Arrow, BaseRobot, gaussian, DEFAULT_WORLD_SIZE
from think.robot_window import Window2


class Robot2(BaseRobot):
    def __init__(self, window, x=None, y=None, o=None):
        super(Robot2, self).__init__(x, y, o, (window.max_x, window.max_y))
        self.window = window
        #self.wall_x = Arrow(0, 0, 0)  # == X-Achse
        #self.wall_y = Arrow(0, 0, pi/2)  # == Y-Achse

    def distance_from_wall(self):
        result = []
        count = 10
        for i in range(10):
            # compute collision point
            (x2, y2) = self.window.vector((self.x, self.y), (self.orientation + 2*pi*i/count) % (2*pi), 2000)
            # pythagoras
            dist = sqrt((x2-self.x)**2 + (y2-self.y)**2)
            result.append(dist)
        return result

    def sense(self):
        distances = self.distance_from_wall()
        result = []
        for d in distances:
            result.append(d + random.gauss(0.0, self.sense_noise))
        print "Measuremen=", result
        return result

    def measurement_prob(self, measurement):

        # calculates how likely a measurement should be

        prob = 1.0
        distances = self.distance_from_wall()
        for i in range(len(measurement)):
            prob *= gaussian(distances[i], self.sense_noise, measurement[i])

        return prob


class Simulator(object):
    def __init__(self, N=10000):
        self.win = Window2("../data/images/map1.bmp")
        self.robot = Robot2(self.win)
        self.N = N
        self.p = []
        for i in range(self.N):
            r = Robot2(self.win)
            r.set_noise(0.2, 0.2, 50)
            self.p.append(r)

    def show_generation(self):
        self.win.dots([(robot.x, robot.y) for robot in self.p])
        self.win.draw_robot((self.robot.x, self.robot.y), self.robot.orientation)
        self.win.show()
        self.win.clear_dl()

    def simulate(self):
        self.show_generation()

        T = 40

        for j in range(T):
            turn = random.random() * 2 * pi
            turn = 0
            forward = random.random() * 25
            self.robot.move(turn, forward)

            #p = [robot.move(turn, forward) for robot in p]
            for robot in self.p:
                robot.move(turn, forward)

            self.show_generation()

            Z = self.robot.sense()
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
                p3.append(self.p[index].copy_to(Robot2(self.win)))

            self.p = p3
            self.show_generation()


sim = Simulator(1000)
sim.simulate()

