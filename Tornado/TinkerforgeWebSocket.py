import tornado.ioloop
import tornado.web
import tornado.websocket
from MyTinkerforge import TinkerforgeStack

TIMEOUT = 1000
PORT = 8889
globalcount =0 

class TinkerforgeWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        global globalcount
        self.id = globalcount
        self.application.tinkerforge_listeners.add(self)
        globalcount += 1
        print "WebSocket opened"

    def on_message(self, message):
        print "on_message"
        self.write_message(u"You said: " + message)

    def on_close(self):
        self.application.tinkerforge_listeners.remove(self)
        print "WebSocket closed"

    def send(self, value):
        print "notify " + str(value)
        self.write_message(u"Value=" + str(value) + " global=" + str(globalcount))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Halo 1", "World 2", "Item 3"]
        self.render("home.html", title="RobotControlCenter", port=PORT, items=items)

class MyApp(tornado.web.Application):

    def __init__(self, bindings):
        super(MyApp, self).__init__(bindings)
        self.tinkerforge_listeners = set([])

        #loop = tornado.ioloop.IOLoop.instance()
        #period_cbk = tornado.ioloop.PeriodicCallback(self.notify, TIMEOUT, loop)
        #period_cbk.start()

        dist_20 = 2942
        dist_60 = 2970
        dist_100 = 3080

        threshold = dist_20

        self.tinkerforge_stack = TinkerforgeStack.PiTinkerforgeStack()
        self.tinkerforge_stack.connect()

        us = self.tinkerforge_stack.distance_us_1
        us.set_debounce_period(1000)
        us.set_distance_callback_period(500)

        us.set_moving_average(20)
        print "Moving averag is {}".format(us.get_moving_average())

        us.register_callback(us.CALLBACK_DISTANCE_REACHED, self.notify_distance_us)
        us.set_distance_callback_threshold('<', threshold, 0)
        print "Callback for distance < {}".format(threshold)

    def notify_distance_us(self, distance):
        for listener in self.tinkerforge_listeners:
            print "Notifying TinkerforgeListener " + repr(listener)
            listener.send(distance)
    
    def notify(self):
        value = 1
        for listener in self.tinkerforge_listeners:
            print "Notifying TinkerforgeListener " + repr(listener)
            listener.send(value)
    

application = MyApp([
    (r"/", MainHandler),
    (r"/websocket", TinkerforgeWebSocket),
])

if __name__ == "__main__":
    application.listen(PORT)
    loop = tornado.ioloop.IOLoop.instance()
    print "Starting loop..."
    loop.start()
