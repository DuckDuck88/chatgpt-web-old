"""
channel factory
"""


def create_bot(bot_type):
    """
    create a channel instance
    :param channel_type: channel type code
    :return: channel instance
    """
    if bot_type == 'openAI':
        # OpenAI 官方对话模型API
        from bot.openai.openai_bot import OpenAIBot
        return OpenAIBot()
    raise RuntimeError
