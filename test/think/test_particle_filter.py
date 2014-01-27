import unittest
from think.particle_filter import *


class TestArrow(unittest.TestCase):
    """Unit tests for ParticleFilter."""

    def setUp(self):
        self.arrow = Arrow(50, 50, pi / 2)
        self.wall_x = Arrow(0, 0, 0)  # == X-Achse
        self.wall_y = Arrow(0, 0, pi / 2)  # == Y-Achse

    def test_base_robot(self):
        """Test BaseRobot class"""
        robot = BaseRobot()
        robot.set_noise(0.1, 0.2, 5)

        for j in range(5):
            turn = random.random() * 2 * pi
            forward = random.random() * 25
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
        w = [25, 10, 5, 60]
        dd = DiscreteDistribution(w)  # 0=>25%, 1=>10%, 2=>5%, 3=>60%

        sample_size = 1000
        sample = dd.sample(sample_size)
        sample.sort()
        two = [x for x in sample if x == 2]
        assert len(two) < 150

        for i in range(len(w)):
            x = len([x for x in sample if x == i])
            print x
            print "Sample contains {} % of element {}.".format(float(x)*100 / sample_size, i)
        print sample
        #assert


if __name__ == "__main__":
    TestArrow.main()






