import hashlib
import time

from werobot import WeRoBot

from channel.channel import Channel
from common.log import logger
from config import conf

token = conf().get('wx_public_token', '')
app_id = conf().get('wx_public_appid','')
encoding_aes_key = conf().get('wx_public_encoding_aes_key','')
myrobot = WeRoBot(token=token, app_id=app_id, encoding_aes_key=encoding_aes_key)

@myrobot.text
def handle_wx_public_msg(message):
    logger.info(f'received wx public msg: {message.content}')
    return WxPublicChannel().handle(message)

class WxPublicChannel(Channel):
    def startup(self):
        pass

    # weRoBot 自动处理了鉴权，这里的代码不生效
    def verify(self, request):
        try:
            data = request.get('data')
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "xxxx"  # 请按照公众平台官网\基本配置中信息填写

            sign_list = [token, timestamp, nonce]
            sign_list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, sign_list)
            hashcode = sha1.hexdigest()
            logger.info("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except  Exception as e:
            logger.exception(f'鉴权异常! {e}')
            return str(e)

    def handle(self, message):
        start_time = time.time()
        try:
            # print(message.content)
            query = message.content
        except Exception as e:
            logger.exception(f'请求异常！{e}')
            return str(e)
        try:
            reply_text = self.build_reply_content(query.strip(), "openAI", None)
            end_time = time.time()-start_time
            logger.info(f'请求耗时：{str(end_time)}')
        except Exception as e:
            return str(e)
        return reply_text.strip()

    def reply(self, msg, receiver):
        pass

    # def failure_reply(self, reply_text, code=400):
    #     return {
    #         "code": code,
    #         "message": "failed",
    #         "reply": reply_text
    #     }

    # def success_reply(self, reply_text):
    #     return {
    #         "code": 200,
    #         "message": "success",
    #         "reply": reply_text
    #     }
