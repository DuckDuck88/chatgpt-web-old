"""
channel factory
"""

from channel.web.web_channel import WebChannel


def create_channel(channel_type):
    """
    create a channel instance
    :param channel_type: channel type code
    :return: channel instance
    """
    if channel_type == 'web':
        return WebChannel()
    raise RuntimeError
