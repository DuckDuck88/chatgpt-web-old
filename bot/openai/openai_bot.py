import openai
from flask import jsonify

from bot.bot import Bot
from common.log import logger
from config import conf


class OpenAIBot(Bot):

    def __init__(self, **args):
        openai.api_key = conf().get('open_ai_api_key')
        self.modele = args.get("model", "text-davinci-003")
        self.temperature = args.get('temperature', 0.9)
        self.max_tokens = args.get('max_tokens', 2048)

    def _get_chat_reply(self, question):
        try:
            response = openai.Completion.create(
                model=self.modele,
                prompt=f"{question}\n",
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.9,
                stop=None
            )
        except Exception as e:
            logger.error(f'OpenAi 请求失败！ {e}')
            return e
        return response["choices"][0].text

    def reply(self, query, context=None):
        if len(query) < 1:
            return jsonify({
                "status": 400,
                "message": None,
                "reply": '问题内容不能为空!'
            })
        logger.info("--------------------------------------")
        reply_text = self._get_chat_reply(query)
        logger.info(f"Q：{query}\nA: {reply_text}\n")
        return reply_text
