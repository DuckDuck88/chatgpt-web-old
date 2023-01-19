# server = Flask(__name__)
# load_config()
# server.config.from_mapping(conf())
# bot = create_bot('openAI')

from flask import Flask, request
from werobot.contrib.flask import make_view

from channel.web.web_channel import WebChannel
from channel.wxapp.wxapp_channel import WxAppChannel
from channel.wxpublic.wxpublic_channel import myrobot
from common.log import logger
from config import load_config, conf

server = Flask(__name__)

load_config()
server.config.from_mapping(conf())


# 前后端不分离
@server.route('/chat', methods=['GET', 'POST'])
def chat_replay_html():
    logger.info(f'请求类型是否为 json:{request.is_json}')
    # logger.info(f'Received request {request.method}, {request.get_json()}')
    if request.method == 'GET':
        # 校验
        return WebChannel().reply_template(request)
    elif request.method == 'POST':
        # 发送消息
        return WebChannel().handle_html(request)


# 前后端分离
@server.route('/chat2', methods=['GET', 'POST'])
def chat_replay_web():
    logger.info(f'请求类型是否为 json:{request.is_json}')
    # logger.info(f'Received request {request.method}, {request.get_json()}')
    if request.method == 'GET':
        # 校验
        return WebChannel().verify(request)
    elif request.method == 'POST':
        # 发送消息
        return WebChannel().handle(request)


# 微信小程序
@server.route('/wxappchat', methods=['GET', 'POST'])
def chat_replay_wxapp():
    logger.info(f'Received request {request.method}, {request.get_json()}')
    wxapp_channel = WxAppChannel()
    verify = wxapp_channel.verify(request)
    if not verify:
        return wxapp_channel.failure_reply('请求校验失败，非来自微信小程序', 400)
    if request.method == 'GET':
        # 校验
        return wxapp_channel.reply(request, None)
    elif request.method == 'POST':
        # 发送消息
        return wxapp_channel.handle(request)


# 微信公众号
server.add_url_rule(rule='/wxpublic/',  # WeRoBot 挂载地址
                    endpoint='werobot',  # Flask 的 endpoint
                    view_func=make_view(myrobot),
                    methods=['GET', 'POST'])

# flask 入口模式
if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=80)
