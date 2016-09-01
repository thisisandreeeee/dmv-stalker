from creds import SLACK_TOKEN
from settings import SLACK_CHANNEL
from slackclient import SlackClient
from datetime import datetime
from logger import Logger

class Bot:
    def __init__(self):
        self.sc = SlackClient(SLACK_TOKEN)
        self.logger = Logger()
        self.logger.log("Bot initialized")

    def post_message(self, msg):
        curr_month = datetime.now().strftime('%B')
        if curr_month in msg:
            self.logger.log("Appointment found for current month")
            msg = "*********************\n" + "<@U1YUJ2FBR> <@U1XU0UF7B>\n" + msg + "\n====================="
        self.sc.api_call(
            "chat.postMessage",
            channel = SLACK_CHANNEL,
            text = msg,
            username = 'DMV-bot',
            icon_emoji = ':robot_face:')
        self.logger.log("Message sent to %s: %s" % (SLACK_CHANNEL, msg.replace('\n',' ').replace('=','').replace('*','')))
