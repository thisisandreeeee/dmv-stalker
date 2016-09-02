from creds import SLACK_TOKEN
from settings import SLACK_CHANNEL, URL
from slackclient import SlackClient
from datetime import datetime
from logger import Logger
import time

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

    def listen(self):
        if self.sc.rtm_connect():
            self.logger.log("Bot is listening to %s" % SLACK_CHANNEL)
            while True:
                command = self._parse_slack_output(self.sc.rtm_read())
                if command:
                    self._handle_command(command)
                    self.logger.log("Bot has responded to command")
                time.sleep(1)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")

    def _handle_command(self, cmd):
        self.sc.api_call(
            "chat.postMessage",
            channel = SLACK_CHANNEL,
            text = cmd,
            username = 'DMV-bot',
            icon_emoji = ':robot_face:')

    def _parse_slack_output(self, rtm_output):
        self.logger.log("Command received. Processing now.")
        output_list = rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and 'url' in output['text']:
                    self.logger.log("Command identified to be 'url'")
                    return URL
        return None
