# In this exercise, try to write a program that
# will resample particles according to their weights.
# Particles with higher weights should be sampled
# more frequently (in proportion to their weight).

# Don't modify anything below. Please scroll to the
# bottom to enter your code.

from math import *
import random
import time
from SimpleCV import Color
from think.particle_filter import Arrow, BaseRobot, gaussian, DEFAULT_WORLD_SIZE
from think.robot_window import Window2
import hello
import numpy as np

class Robot2(BaseRobot):
    def __init__(self, window, x=None, y=None, o=None):
        super(Robot2, self).__init__(x, y, o, (window.max_x, window.max_y))
        self.window = window
        #self.wall_x = Arrow(0, 0, 0)  # == X-Achse
        #self.wall_y = Arrow(0, 0, pi/2)  # == Y-Achse

    def distance_from_wall(self, draw=False):
        if draw:
            color = Color.FORESTGREEN
        else:
            color = None

        x = self.x
        y = self.y

        result = []
        count = 4
        for i in range(count):
            # compute collision point
            #(x2, y2) = self.window.vector((self.x, self.y), (self.orientation + 2*pi*i/count) % (2*pi), 2000,
            #                              detect_collision=True, color=color)

            bx = int(round(x + cos(self.orientation + 2*pi*i/count) * 2000))
            by = int(round(y + sin(self.orientation + 2*pi*i/count) * 2000))
            if draw or random.random() < 0.01:
                c2 = self.window.line((x, y), (bx, by), detect_collision=True, color=color)
            else:
                c2 = hello.compute_distance(x, y, bx, by, self.window.array_map)
            if c2 is None:
                raise RuntimeError
            (x2, y2) = c2

            # pythagoras
            dist = sqrt((x2-self.x)**2 + (y2-self.y)**2)
            result.append(dist)
        return result

    def sense(self):
        distances = self.distance_from_wall(draw=True)
        result = []
        for d in distances:
            result.append(d + random.gauss(0.0, self.sense_noise))
        print "Measurement=", result
        return result

    def measurement_prob(self, measurement):

        # calculates how likely a measurement should be
        result = 1.0
        distances = self.distance_from_wall()
        for i in range(len(measurement)):
            prob = gaussian(distances[i], self.sense_noise, measurement[i])
            #print "Particle at {}, {} has distance {} at sensor {}".format(self.x, self.y, distances[i], i)
            #print "Measurement was {} resulting in probability {}".format(measurement[i], prob)
            result *= prob

        return result


def measurement_prob2(particles, measurement):
    t1 = time.clock()

    w = []
    for p in particles:
        #w.append(particles[i].measurement_prob(measurement))

        # calculates how likely a measurement should be
        result = 1.0

        distances = p.distance_from_wall()
        for i in range(len(measurement)):
            prob = gaussian(distances[i], p.sense_noise, measurement[i])
            #print "Particle at {}, {} has distance {} at sensor {}".format(self.x, self.y, distances[i], i)
            #print "Measurement was {} resulting in probability {}".format(measurement[i], prob)
            result *= prob
        w.append(result)
        t2 = time.clock()
    print "Time for computing particle prob: ", round(t2-t1, 10)

    return w

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
            #turn = 0
            forward = random.random() * 25
            self.robot.move(turn, forward)

            #p = [robot.move(turn, forward) for robot in p]
            print "Robot.move()............."
            for robot in self.p:
                robot.move(turn, forward)

            self.show_generation()

            print "Robot.sense()............"
            Z = self.robot.sense()
            print "Robot.sense() end"
            print "Computing weights..."
            #w = []
            #for i in range(self.N):
            #    w.append(self.p[i].measurement_prob(Z))
            w = measurement_prob2(self.p, Z)

            # wheel
            # biased? see http://forums.udacity.com/questions/3001328/an-on-unbiased-resampler#cs373
            print "Resampling..."
            w_max = max(w)
            p3 = []
            index = int(floor(random.random() * self.N))
            b = 0
            indexes = [1 for x in range(len(self.p))]
            for i in range(self.N):
                b += random.random() * w_max
                while w[index] < b:
                    b -= w[index]
                    index = (index + 1) % self.N
                    indexes[index] += 1
                p3.append(self.p[index].copy_to(Robot2(self.win)))

            self.p = p3
            #w.sort()
            #print w
            #print indexes
            self.show_generation()

def show_probs(pos, measurement, noise):
    prob = gaussian(pos, i, measurement)
    print "pos=", pos, "measurement=", measurement, "noise=", noise, " prob=", prob

if __name__ == "__main__":
    sim = Simulator(20000)
    sim.simulate()
    for pos in range(120, 160, 10):
        for i in range(15, 25, 5):
            show_probs(pos, 150, i)

