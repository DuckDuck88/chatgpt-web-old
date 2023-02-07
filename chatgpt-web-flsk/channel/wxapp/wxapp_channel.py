# encoding:utf-8

"""
web channel
"""

from channel.channel import Channel
from common.log import logger


class WxAppChannel(Channel):
    def __init__(self):
        pass

    def startup(self):
        pass

    def handle(self, request):
        try:
            query = request.get_json().get("question")
        except Exception as e:
            logger.exception(f'请求异常！{e}')
            return self.failure_reply(e)
        try:
            reply_text = self.build_reply_content(query, "openAI", None)
        except Exception as e:
            return self.failure_reply(e)
        return self.success_reply(reply_text)

    def reply(self, msg, receiver):
        return self.success_reply('暂时无实现')

    def verify(self, request):
        openid = request.args.get("openid")
        jsonData = {
            
        }
        return self.success_reply(openid)

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
