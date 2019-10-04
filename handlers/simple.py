import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class TelegramProxy(tornado.web.RedirectHandler):
    _url, _permanent = None, None

    def initialize(self, end, *args):
        self._url = f'https://api.telegram.org/bot/{end}'
        self._permanent = False

    def check_xsrf_cookie(self):
        return
