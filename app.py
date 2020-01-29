import os
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from tornado_sqlalchemy import make_session_factory
from utils import Collector, Item
from handlers import *


item_update_id = None


class Application(tornado.web.Application):
    def __init__(self, **settings):
        handlers = [
            (r'/', MainHandler),
            (r'/send/vk/', SenderHandler),
        ]
        settings.update(
            site_title=options.site_title,
            cookie_secret=options.cookie_secret,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

    def update_tg_bot_message(self):
        global item_update_id
        TgBotActionsHandler(item_update_id).execute()
        return None


def main():
    Collector(define, 'def_base', 'def_secrets')  # pick options
    fake_tlc = Collector(None, 'def_kwargs', update_id=None)

    global item_update_id
    item_update_id = Item(fake_tlc, 'update_id')

    tornado.options.parse_command_line()
    print("Server listening on port " + str(options.port))
    logging.getLogger().setLevel(logging.DEBUG)

    factory = make_session_factory(options.dburl)
    app = Application(session_factory=factory)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    # im-send-btn im-chat-input--send _im_send im-send-btn_send
    # im_chat-input--buttons
    loop = tornado.ioloop.IOLoop.instance()
    # period_cbk = tornado.ioloop.PeriodicCallback(
    #     app.update_tg_bot_message,
    #     10 * 1000,  # раз в 10 секунд
    # )
    # period_cbk.start()

    loop.start()


if __name__ == "__main__":
    main()
