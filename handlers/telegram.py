import telegram
import tornado.web
import tornado.gen
import logging
from tornado.options import options

logger = logging.getLogger(__name__)


class TgBotActionsHandler:
    update_id = None

    def __init__(self, update_id):
        self.update_id = update_id

    @property
    def _proxy_url(self):
        return 'https://ifrag-notifier.herokuapp.com/_proxy/telegram/'

    async def execute(self):
        bot = telegram.Bot(options.tg_token, base_url=self._proxy_url)
        self.try_update_id(bot)
        self.echo(bot)
        return self.update_id

    def try_update_id(self, bot):
        try:
            self.update_id = bot.get_updates()[0].update_id
        except IndexError:
            self.update_id = None

    def echo(self, bot):
        for update in bot.get_updates(offset=self.update_id, timeout=10):
            self.update_id = update.update_id + 1

            if update.message:
                update.message.reply_text(update.message.text)
