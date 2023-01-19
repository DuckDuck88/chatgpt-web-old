# encoding:utf-8

"""
web channel
"""

from flask import render_template

from channel.channel import Channel
from common.log import logger


def failure_reply(reply_text, code=400):
    return {
        "code": code,
        "message": "failed",
        "reply": reply_text
    }


def success_reply(reply_text):
    return {
        "code": 200,
        "message": "success",
        "reply": reply_text
    }


class WebChannel(Channel):
    def __init__(self):
        pass

    def startup(self):
        pass

    #     server.run(debug=True, host='0.0.0.0', port=80)

    def handle(self, request):
        try:
            query = request.get_json().get("question")
        except Exception as e:
            logger.exception(f'请求异常！{e}')
            return failure_reply(e)
        try:
            reply_text = self.build_reply_content(query, "openAI", None)
        except Exception as e:
            return failure_reply(e)
        return success_reply(reply_text)

    def reply(self, msg, receiver):
        """
        用于主动发送回复消息，适用场景 wx
        """
        pass

    def verify(self, request):
        return {
            "status": 200,
            "message": None,
            "reply": 'web 不需要校验请求用户身份'
        }

    def handle_html(self, request):
        try:
            # query = request.get_json().get("question")
            if len(request.form['question']) < 1:
                return render_template('chat.html',
                                       question="null", res="问题不能为空")
            query = request.form['question']
        except Exception as e:
            logger.exception(f'请求异常！{e}')
            return failure_reply(e)
        try:
            reply_text = self.build_reply_content(query, "openAI", None)
        except Exception as e:
            return failure_reply(e)
        return render_template('chat.html', question=query,
                               res=str(reply_text))

    def reply_template(self, request):
        return render_template('chat.html', question=0)
