import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class TelegramProxy(tornado.web.RedirectHandler):
    _url, _permanent = None, None

    def initialize(self, *args):
        self._url = 'https://api.telegram.org/bot'
        self._permanent = False
