import tornado.ioloop
import tornado.web
import tornado.websocket

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print "WebSocket opened"

    def on_message(self, message):
        print "on_message"
        self.write_message(u"You said: " + message)

    def on_close(self):
        print "WebSocket closed"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Halo 1", "World 2", "Item 3"]
        self.render("template.html", title="My title", items=items)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", EchoWebSocket),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
