import random
from flask import Flask, request, abort
    

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
    VideoMessageContent
)
from linebot.v3.messaging.models.reply_message_response import ReplyMessageResponse

import tempfile
import os
import time
from datetime import datetime

from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth


gauth = GoogleAuth()

drive = GoogleDrive(gauth)

app = Flask(__name__)

configuration = Configuration(access_token='YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')


# get verified groups' id
verified_groups_id = ""
with open("verified_groups.txt") as f:
    verified_groups_id = f.read().splitlines()


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
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_TextMessage(event):
    with ApiClient(configuration) as api_client:
        if event.message.text == "!getgid":
            line_bot_api = MessagingApi(api_client)
            msg = TextMessage(text=event.source.group_id)
            reply_message_request = ReplyMessageRequest(reply_token=event.reply_token, messages=[msg)
            line_bot_api.reply_message(reply_message_request)

def handle_blob(event,ext):
    with ApiClient(configuration) as api_client:
        try:
            line_bot_api = MessagingApiBlob(api_client)
            time.sleep(10)
            dir_id = verified_groups_id[verified_groups_id.index(event.source.group_id) + 1]
            message_content = line_bot_api.get_message_content(event.message.id)
            with tempfile.NamedTemporaryFile(delete=False) as tf:
                tf.write(message_content)    
                tempfile_path = tf.name
            dist_path = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "." + ext
            os.rename(tempfile_path, dist_path)
            file1 = drive.CreateFile({"parents": [{"id": dir_id}]})
            file1.SetContentFile(dist_path)
            file1.Upload()
            return 0
        except ValueError:
            print("id: " + event.source.group_id + "not matching.")
        except Exception as e:
            print(e)

@handler.add(MessageEvent, message=ImageMessageContent)
def handle_ImageMessage(event):
    handle_blob(event,"jpg")


@handler.add(MessageEvent, message=VideoMessageContent)
def handle_ImageMessage(event):
    handle_blob(event,"mp4")


if __name__ == "__main__":
    app.run()
