from creds import SLACK_TOKEN
from settings import SLACK_CHANNEL
from slackclient import SlackClient
from datetime import datetime

class Bot:
    def __init__(self):
        self.sc = SlackClient(SLACK_TOKEN)

    def post_message(self, msg):
        curr_month = datetime.now().strftime('%B')
        if curr_month in msg:
            msg = "<@U1YUJ2FBR> <@U1XU0UF7B>\n" + msg
        self.sc.api_call(
            "chat.postMessage",
            channel = SLACK_CHANNEL,
            text = msg,
            username = 'DMV-bot',
            icon_emoji = ':robot_face:')
