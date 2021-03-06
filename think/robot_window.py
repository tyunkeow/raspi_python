from SimpleCV import Image, Display, Color, pg
import time
import os
import numpy as np
from math import *
from profilehooks import profile


class Window:
    world_size = 100
    img_size = (world_size, world_size)
    generation = 0

    def __init__(self):
        self.display = Display(self.img_size)
        self.img = Image(self.img_size)
        self.img.save(self.display)

    def dot(self, x, y, size=0, color=Color.WHITE):
        x = int(round(x))
        y = int(round(y))
        #print "Drawing robot particle at {}, {}".format(x, y)
        self.img.dl().circle((x, y), size, color, filled=True)

    def dot_red(self, x, y):
        self.dot(x, y, 2, Color.RED)

    def dots(self, coords, size=0, color=Color.WHITE):
        for (x, y) in coords:
            self.dot(x, y, size, color)

    def clear(self):
        self.img = Image(self.img_size)
        #self.display.clear()
        self.img.save(self.display)

    def show(self):
        self.img.save(self.display)
        self.generation += 1
        print "Generation = {}".format(self.generation)
        self.wait_for_mouse()

    def wait_for_mouse(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    print event
                    self.clear()
                    return


class Window2:
    generation = 0

    def __init__(self, filename, scale=1):
        filename = os.path.expanduser(filename)
        self.img = Image(filename)
        self.max_x, self.max_y = self.img.width, self.img.height
        self.scale = scale

        self.array_map = np.array([[0 for y in range(self.max_y)] for x in range(self.max_x)])
        for x in range(self.max_x):
            for y in range(self.max_y):
                pixel = self.img.getPixel(x, y)
                self.array_map[x][y] = (pixel == (255, 255, 255))

        # scale image
        self.img = self.img.resize(self.img.width*scale, self.img.height*scale)
        self.img_size = self.img.width, self.img.height

        self.display = Display(self.img_size)
        self.img.save(self.display)

    def dot(self, p, color=Color.WHITE, size=0):
        x, y = p[0], p[1]
        #print "Drawing robot particle at {}, {}".format(x, y)
        if x < 0 or x >= self.max_x:
            print "Oh my god! x=", x
            raise RuntimeError
        if y < 0 or y >= self.max_y:
            print "Oh shit! y=", y
            raise RuntimeError
        else:
            self.img.dl().circle(center=(x*self.scale, y*self.scale), radius=size, color=color, width=1, filled=True)

    def dot_red(self, p, color=Color.RED):
        self.dot(p, color, 2)

    def dots(self, coords, color=Color.WHITE, size=0):
        for (x, y) in coords:
            self.dot((x, y), color, size)

    def clear(self):
        self.img = Image(self.img_size)
        #self.display.clear()
        self.img.save(self.display)

    def clear_dl(self):
        self.img.clearLayers()
        self.img.save(self.display)

    def show(self):
        self.img.save(self.display)
        self.generation += 1
        print "Generation = {}".format(self.generation)
        self.wait_for_mouse()
        print "Mouse pressed!"

    def draw_robot(self, position, orientation):
        color = Color.RED
        #self.img.drawRectangle(p[0], p[1], 20, 40, color, 1)
        self.dot(position, color, 2)

        length = 20
        bx = int(round(position[0] + cos(orientation) * length))
        by = int(round(position[1] + sin(orientation) * length))

        self.vector(position, orientation, length, detect_collision=False, color=color)
        self.vector((bx, by), orientation - 3*pi/4, length=8, detect_collision=False, color=color)
        self.vector((bx, by), orientation + 3*pi/4, length=8, detect_collision=False, color=color)

    def vector(self, x, orientation, length, detect_collision=True, color=Color.FORESTGREEN):
        bx = int(round(x[0] + cos(orientation) * length))
        by = int(round(x[1] + sin(orientation) * length))
        #self.dot_red((bx, by))
        return self.line(x, (bx, by), detect_collision=detect_collision, color=color)
        #return bx, by

    # a = startpunkt, b = endpunkt
    #@profile
    def line(self, a, b, detect_collision=True, color=Color.BLUE):
        """http://en.wikipedia.org/wiki/Bresenham's_line_algorithm"""

        # performance => use local vars
        max_x = self.max_x
        max_y = self.max_y
        array_map = self.array_map

        x0, y0 = a
        x1, y1 = b
        dx = abs(x1-x0)
        dy = -abs(y1-y0)
        if x0 < x1:
            sx = 1
        else:
            sx = -1

        if y0 < y1:
            sy = 1
        else:
            sy = -1
        err = dx+dy

        while True:
            if x0 <= 0 or x0 >= max_x or y0 <= 0 or y0 >= max_y:
                break
            if color:
                self.dot((x0, y0), color, 0)
            #if detect_collision and self.img.getPixel(x0, y0) == (255, 255, 255):
            if detect_collision and array_map[x0][y0]:
                break
            if x0 == x1 and y0 == y1:
                break
            e2 = 2*err

            if e2 > dy:
                err += dy
                x0 += sx

            if x0 == x1 and y0 == y1:
                #if color:
                #    self.dot((x0, y0), color, 0)
                break

            if e2 < dx:
                err = err + dx
                y0 += sy
        return x0, y0

    def wait_for_mouse(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    print event
                    #self.clear()
                    return

#
# if __name__ == "__main__":
#     w = Window2("../data/images/map1.bmp")
#     #w.dot_red(90, 90)
#     for i in range(0, 700, 50):
#         print "step", i
#         a = (100+i, 100)
#         b = (500, 700)
#         print pi*i/700
#         w.draw_robot(a, 2*pi*i/700)
#         w.dot_red(b)
#         p = w.line(a, b)
#         if p is not None:
#             print "Wall sensed at ", p
#         w.show()
#         #time.sleep(500)
#         w.clear_dl()

