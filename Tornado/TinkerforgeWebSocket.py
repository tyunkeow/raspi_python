import tornado.ioloop
import tornado.web
import tornado.websocket

TIMEOUT = 1000
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
        self.render("home.html", title="RobotControlCenter", items=items)

class MyApp(tornado.web.Application):

    def __init__(self, bindings):
        super(MyApp, self).__init__(bindings)
        self.tinkerforge_listeners = set([])

        loop = tornado.ioloop.IOLoop.instance()
        period_cbk = tornado.ioloop.PeriodicCallback(self.notify, TIMEOUT, loop)
        period_cbk.start()

    
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
    application.listen(8888)
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()
