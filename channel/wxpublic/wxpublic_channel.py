import hashlib

from werobot import WeRoBot

from channel.channel import Channel
from common.log import logger
from config import conf

token = conf().get('wx_public_token', '')
myrobot = WeRoBot(token=token)


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

    @myrobot.handler
    def handle(self, message):
        logger.info(f'收到公众号请求 {message}')
        try:
            query = message.content
        except Exception as e:
            logger.exception(f'请求异常！{e}')
            return self.failure_reply(e)
        try:
            reply_text = self.build_reply_content(query, "openAI", None)
        except Exception as e:
            return self.failure_reply(e)
        return self.success_reply(reply_text)

    def reply(self, msg, receiver):
        pass

    def failure_reply(self, reply_text, code=400):
        return {
            "code": code,
            "message": "failed",
            "reply": reply_text
        }

    def success_reply(self, reply_text):
        return {
            "code": 200,
            "message": "success",
            "reply": reply_text
        }
