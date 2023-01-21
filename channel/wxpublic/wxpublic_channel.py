import datetime
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor

from channel.channel import Channel
from common.log import logger

# token = conf().get('wx_public_token', '')
# app_id = conf().get('wx_public_appid','')
# encoding_aes_key = conf().get('wx_public_encoding_aes_key','')
# myrobot = WeRoBot(token=token, app_id=app_id, encoding_aes_key=encoding_aes_key)

# @myrobot.text
# def handle_wx_public_msg(message):
#     logger.info(f'received wx public msg: {message.content}')
#     return WxPublicChannel().handle(message)

msg_id_cache = {}
msg_content_cache = {}


class WxPublicChannel(Channel):
    pool = ThreadPoolExecutor(max_workers=8)

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

    def pre_handle(self, message):
        """
        预处理，用于处理超时问题。
        """
        if msg_content_cache.get(message.content, '') != '':
            logger.info(f'问题已存在，返回混存值')
            return msg_content_cache[message.content]  # 如果已存在同样请求直接返回。
        msg_id_cache[message.message_id] = msg_id_cache.get(message.message_id, 4) - 1
        if msg_id_cache[message.message_id] >= 3:  # 判断 message 是否已经存在
            msg_content_cache[message.content] = ''

            # 启动一个新线程，用于构建返回值
            thread_future = self.pool.submit(self.handle, message.content)
            now = datetime.datetime.now()
            timeout = now + datetime.timedelta(seconds=msg_id_cache[message.message_id] * 5 - 0.5)
            logger.info(f'进入超时判断逻辑，当前超时时间 {msg_id_cache[message.message_id] * 5} {timeout}')
            while thread_future.running() and now < timeout:
                now = datetime.datetime.now()
                time.sleep(0.1)
            # 超时
            if now < timeout and thread_future.done():
                logger.info(f'未超时且完成返回')
                result = thread_future.result()
                msg_content_cache[message.content] = result
                return result
        # 已存在，如果存在返回结果，则直接返回对应结果
        else:
            logger.info(f'session 中存在对应请求，判断是否存在返回值，res={msg_content_cache[message.content]}')
            time.sleep(0.1)
            now = datetime.datetime.now()
            timeout = now + datetime.timedelta(seconds=msg_id_cache[message.message_id] * 5 - 0.5)
            logger.info(f'进入超时判断逻辑，当前超时时间 {msg_id_cache[message.message_id] * 5} {timeout}')
            while msg_content_cache[message.content] == '' and now < timeout:
                now = datetime.datetime.now()
                time.sleep(0.1)
            return msg_content_cache[message.content]

    def handle(self, query):
        start_time = time.time()
        try:
            reply_text = self.build_reply_content(query, "openAI", None)
            msg_content_cache[query] = reply_text
            end_time = time.time() - start_time
            logger.info(f'构建回复耗时：{str(end_time)}')
        except Exception as e:
            logger.exception(f"{e}")
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
