from werobot import WeRoBot

from channel.wxpublic.wxpublic_channel import WxPublicChannel
from common.log import logger
from config import conf

token = conf().get('wx_public_token', '')
app_id = conf().get('wx_public_appid', '')
encoding_aes_key = conf().get('wx_public_encoding_aes_key', '')
wxrobot = WeRoBot(token=token, app_id=app_id, encoding_aes_key=encoding_aes_key)

wx_public_channel: WxPublicChannel = WxPublicChannel.get_instance(WxPublicChannel)


@wxrobot.handler
def bottom_up_strategy(message):
    """
    兜底策略，其他 handle 没有给出回复时使用此策略
    """
    logger.info(f'received wx public msg: {message.__dict__}')
    return "当前操作未定义~"


@wxrobot.text
def handle_wx_public_msg(message):
    logger.info(f'received wx public msg: {message.content}')
    return wx_public_channel.handle(message)


@wxrobot.subscribe
def subscribe(message):
    return '你好呀，我是智能助理冰冰，感谢你的关注，有什么问题可以问我呀~'
