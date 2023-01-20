from werobot import WeRoBot

from channel.wxpublic.wxpublic_channel import WxPublicChannel
from common.log import logger
from config import conf

token = conf().get('wx_public_token', '')
app_id = conf().get('wx_public_appid', '')
encoding_aes_key = conf().get('wx_public_encoding_aes_key', '')
myrobot = WeRoBot(token=token, app_id=app_id, encoding_aes_key=encoding_aes_key)


@myrobot.text
def handle_wx_public_msg(message):
    logger.info(f'received wx public msg: {message.content}')
    return WxPublicChannel().handle(message)
