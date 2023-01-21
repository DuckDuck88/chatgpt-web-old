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
    if message.type == 'text':
        logger.info(f'received wx public msg: {message.content}')
        return "这个问题有些复杂，公众号大大要 15s 内给出回复，小的办不到 ಥ_ಥ "


@wxrobot.text
def handle_wx_public_msg(message, session):
    logger.info(f'===================================\nreceived wx public msg: {message.content}')
    # return wx_public_channel.handle(message)
    return wx_public_channel.pre_handle(message)


@wxrobot.subscribe
def subscribe(message):
    return '你好呀，我是智能助理冰冰，感谢你的关注，有什么问题可以问我呀~'
