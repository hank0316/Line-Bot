import os
import sys
import json

from flask import Flask, request, abort, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)

from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FollowEvent, JoinEvent,
)

app = Flask(__name__)
channel_access_token = os.getenv("CHANNEL_ACCESS_TOKEN", None)
channel_secret = os.getenv("CHANNEL_SECRET", None)

if channel_access_token is None or channel_secret is None:
    print("Please make sure that CHANNEL_ACCESS_TOKEN & CHANNEL_SECRET are both in your environment variable.")
    exit(1)

linebot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# Get information from LINE when someone access https://hank_interview.herokuapp.com/callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# The default language is Chinese
LANG="chinese"
# Load the json file for the reply message
f = open('./reply.json', 'r')
reply_messages = json.load(f)[LANG]
f.close()


# Handle follow event
@handler.add(FollowEvent)
def handle_follow_event(event):
    try:
        user_profile = linebot_api.get_profile(event.source.user_id)
        linebot_api.reply_message(
            event.reply_token, [
                    TextSendMessage(text=f'{reply_messages["greeting"]} {user_profile.display_name}！{reply_messages["follow"]}'),
                ]
            )
    except:
        # User unblock this account
        linebot_api.reply_message(
            event.reply_token, [
                    TextSendMessage(text=reply_messages["unblock"])
                ]
            )

# join group
@handler.add(JoinEvent)
def handle_join_group(event):
    linebot_api.reply_message(
        event.reply_token, [
                TextSendMessage(text=f'{reply_messages["greeting"]}！{reply_messages["follow"]}'),
            ]
        )

# Handle text messages
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text.lower()

    if text == 'github':
         linebot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=reply_messages["github"])
                ]
            )
    elif text == 'lab':
        linebot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=reply_messages["lab"])
                ]
            )
    elif text in ['project', 'speech lab', 'miulab']:
        linebot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=t)
                    for _, t in reply_messages[text].items()
                ]
            )
    elif text == 'introduction':
        linebot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=reply_messages["myself"])
                ]
            )
    else:
       linebot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=reply_messages['unknown'])
                ]
            )
        

if __name__ == '__main__':
    app.run()
