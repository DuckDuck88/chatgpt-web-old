"""
Message sending channel abstract class
"""
import threading

from bridge.bridge import Bridge


class Channel(object):
    _lock = threading.Lock()
    _instance = None

    @classmethod
    def get_instance(cls, ins_name):
        """
        实现单例模式
        """
        if cls._instance is not None:
            return cls._instance

        with cls._lock:
            if cls._instance is not None:
                return cls._instance

            cls._instance = ins_name()
            return cls._instance

    def startup(self):
        """
        init channel
        """
        raise NotImplementedError

    def handle(self, msg):
        """
        process received msg
        :param msg: message object
        """
        raise NotImplementedError

    def reply(self, msg, receiver):
        """
        send message to user
        :param msg: message content
        :param receiver: receiver channel account
        :return:
        """
        raise NotImplementedError

    def build_reply_content(self, query, bot="openAI", context=None):
        return Bridge().fetch_reply_content(query, context, bot)
