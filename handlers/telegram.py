import telegram
import tornado.web
import tornado.gen
import logging
from tornado.options import options

logger = logging.getLogger(__name__)


class TgBotActionsHandler:
    update_id, item = None, None

    def __init__(self, item_update_id):
        self.item = item_update_id
        self.update_id = self.item.get()

    def execute(self):
        bot = telegram.Bot(options.tg_token)
        self.echo(bot)
        self.item.set(self.update_id)

    def echo(self, bot):
        for update in bot.get_updates(offset=self.update_id, timeout=10):
            self.update_id = update.update_id + 1

            if update.message:
                update.message.reply_text(update.message.text)
