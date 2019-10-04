import os
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options


define("environment", default="development", type=str)
define("site_title", default="Simple Notifier", type=str)
define("cookie_secret", default=os.getenv('cookie_secret', 'seсret'), type=str)
define("port", default="8000", help="Listening port", type=str)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
           (r"/", MainHandler),
        ]
        settings = dict(
            site_title=options.site_title,
            cookie_secret=options.cookie_secret,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    print("Server listening on port " + str(options.port))
    logging.getLogger().setLevel(logging.DEBUG)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
