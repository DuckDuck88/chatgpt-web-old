# server = Flask(__name__)
# load_config()
# server.config.from_mapping(conf())
# bot = create_bot('openAI')

from channel import channel_factory
from common.log import logger

# @server.route('/chat', methods=['GET', 'POST'])
# def chat_replay():
#     logger.info(f'Received request {request.method}, {request.get_json()}')
#     if request.method == 'GET':
#         # 校验
#         return bot.get_completion(request)
#     elif request.method == 'POST':
#         # 发送消息
#         data = request.get_json().get("question")
#         return bot.reply(data)
# encoding:utf-8

# server

if __name__ == '__main__':
    try:
        # load config

        # create channel
        channel_type = 'web'
        channel = channel_factory.create_channel(channel_type)
        if channel_type == 'web':
            logger.info("Channel WEB")
        logger.info(f'Starting')
        channel.startup()
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)

# if __name__ == '__main__':
# server.run(debug=True, host='0.0.0.0', port=80)
#
