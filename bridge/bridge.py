from bot import bot_factory


class Bridge(object):
    def __init__(self):
        pass

    def fetch_reply_content(self, query, context, bot):
        return bot_factory.create_bot(bot).reply(query, context)
