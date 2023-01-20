# server = Flask(__name__)
# load_config()
# server.config.from_mapping(conf())
# bot = create_bot('openAI')

from flask import Flask, request, render_template
from werobot.contrib.flask import make_view

from channel.web.web_channel import WebChannel
from channel.wxapp.wxapp_channel import WxAppChannel
from channel.wxpublic.wxpublic_channel import WxPublicChannel
from common.log import logger
from config import conf
from thirdapp.wx_public_admin.wx_public_admin import wxrobot

server = Flask(__name__)
server.config.from_mapping(conf())

# 实例化各个 channel
web_channel = WebChannel.get_instance(WebChannel)
wxapp_channel = WxAppChannel.get_instance(WxAppChannel)
wx_public_channel = WxPublicChannel.get_instance(WxPublicChannel)


@server.route('/', methods=['GET'])
def hello_world():
    return render_template('hello.html')


# 前后端不分离
@server.route('/chat', methods=['GET', 'POST'])
def chat_replay_html():
    # logger.info(f'Received request {request.method}, {request.get_json()}')
    if request.method == 'GET':
        # 校验
        return web_channel.reply_template(request)
    elif request.method == 'POST':
        # 发送消息
        return web_channel.handle_html(request)


# 前后端分离
@server.route('/chat2', methods=['GET', 'POST'])
def chat_replay_web():
    # logger.info(f'Received request {request.method}, {request.get_json()}')
    if request.method == 'GET':
        # 校验
        return web_channel.verify(request)
    elif request.method == 'POST':
        # 发送消息
        return web_channel.handle(request)


# 微信小程序
@server.route('/wxappchat', methods=['GET', 'POST'])
def chat_replay_wxapp():
    logger.info(f'Received request {request.method}, {request.get_json()}')
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
server.add_url_rule(rule='/chatrest/wxpublic/',  # WeRoBot 挂载地址
                    endpoint='werobot',  # Flask 的 endpoint
                    view_func=make_view(wxrobot),
                    methods=['GET', 'POST'])

# flask 入口模式
if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=8888)
