import tornado.web
from tornado.options import options
import vk_api
import os


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class SenderHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        url = self.get_argument('url')
        user_id = url[url.index('=')+1:]

        vk_session = vk_api.VkApi(
            options.EMAIL,
            options.PASSWORD,
            scope='messages',
        )
        vk_session.auth()
        api = vk_session.get_api()
        print(user_id, text)
        api.messages.send(
            message=text,
            user_id=user_id,
            peer_id=user_id,
            random_id=user_id,
        )

    def check_xsrf_cookie(self):
        return True
