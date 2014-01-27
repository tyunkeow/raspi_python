from SimpleCV import Image, Display, Color, pg
import time

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





