import unittest
import time
from think.particle_filter import *


class TestArrow(unittest.TestCase):
    """Unit tests for ParticleFilter."""

    def setUp(self):
        self.arrow = Arrow(50, 50, pi / 2)
        self.wall_x = Arrow(0, 0, 0)  # == X-Achse
        self.wall_y = Arrow(0, 0, pi / 2)  # == Y-Achse

    def test_base_robot_move(self):
        """Test BaseRobot class"""
        robot = BaseRobot(x=None, y=None, orientation=None, world_size=(110, 110))
        robot.set_noise(0, 0, 0)
        self.assertIsNotNone(robot.x)
        self.assertIsNotNone(robot.y)

        robot.set(50, 100, 0)
        self.assertEqual(50, robot.x)
        self.assertEqual(100, robot.y)

        # 10 nach rechts
        robot.move(0, 10)
        self.assertEqual(60, robot.x)
        self.assertEqual(100, robot.y)

        # 9 nach oben
        robot.move(pi/2, 9)
        self.assertEqual(60, robot.x)
        self.assertEqual(109, robot.y)

        # Torus-Topologie
        robot.move(0, 1)
        self.assertEqual(60, robot.x)
        self.assertEqual(0, robot.y)

        # 10 nach links
        robot.move(-1.5*pi, 10)
        self.assertEqual(50, robot.x)
        self.assertEqual(0, robot.y)

        # diagonal move
        robot.move(-0.75*pi, sqrt(5**2+5**2))
        self.assertEqual(55, robot.x)
        self.assertEqual(5, robot.y)


    def test_base_robot(self):
        """Test BaseRobot class"""
        robot = BaseRobot()
        robot.set_noise(0.1, 0.2, 5)

        for j in range(5):
            turn = random.random() * 2 * pi
            forward = 25 + random.random() * 50
            print "Turning robot {} by {} and moving forward by {}.".format(robot, turn, forward)
            print "New orientation =", (turn + robot.orientation) % (2*pi)
            x1, y1 = robot.x, robot.y
            robot.move(turn, forward)
            x2, y2 = robot.x, robot.y
            print robot
            self.assertTrue(x1 != x2, 'No x movement')
            self.assertTrue(y1 != y2, 'No y movement')

    def test_arrow_constuctor(self):
        print self.arrow
        assert self.arrow.x == 50
        assert self.arrow.y == 50
        assert self.arrow.orientation == pi / 2

    def test_arrow_collision(self):
        cv_x = (cv1, cv2) = self.arrow.collision_vector(self.wall_x)
        assert cv1 == -50
        assert cv2 == 50
        print "wall_x collision_vector:    {}".format(cv_x)

        cv_y = (cv1, cv2) = self.arrow.collision_vector(self.wall_x)
        assert cv1 == -50
        assert cv2 == 50
        print "wall_y collision_vector:     {}".format(cv_y)

    def test_arrow_intersection(self):
        arrow = Arrow(50, 50, pi / 2)
        (x, y) = schnittp_x = self.arrow.intersect(self.wall_x)
        assert x == 50
        assert y == 0
        print "wall1 intersection:    {}".format(schnittp_x)

        (x, y) = schnittp_y = self.arrow.intersect(self.wall_y)
        assert x is None
        assert y is None
        print "wall1 intersection:    {}".format(schnittp_y)


class TestDiscreteDistribution(unittest.TestCase):

    def test_sampling(self):
        w = [25, 10, 5, 60] # Gewichte sind gleichzeitig prozentzahlen (siehe asserts)
        dd = DiscreteDistribution(w)  # 0=>25%, 1=>10%, 2=>5%, 3=>60%

        sample_size = 1000
        sample = dd.sample1(sample_size)

        for i in range(len(w)):
            x = len([x for x in sample if x == i])
            print x
            prozent = float(x)*100 / sample_size
            self.assertAlmostEqual(prozent, w[i], None, None, 5)
            print "Sample contains {} % of element {}.".format(prozent, i)
        print sample
        #assert

    def test_sampling_perf(self):
        size = 20000
        w = [random.random()/10000000000000. for i in range(size)]
        dd = DiscreteDistribution(w)

        sample = dd.sample3(size)
        self.assertEqual(size, len(sample))


class TestGaussian(unittest.TestCase):

    def test_gaussian(self):
        pos = 150
        for noise in range(10, 30, 5):
            for measurement in range(100, 200, 10):
                prob = gaussian(pos, noise, measurement)
                print "pos=", pos, "measurement=", measurement, "noise=", noise, " prob=", prob








