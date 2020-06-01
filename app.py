import random
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import tempfile
import os
import time
from datetime import datetime

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

gauth = GoogleAuth()

drive = GoogleDrive(gauth)

app = Flask(__name__)

line_bot_api = LineBotApi("YOUR_TOKEN_HERE")
handler = WebhookHandler("YOUR_CHANNEL_SECRET")


# get verified groups' id
verified_groups_id = ""
with open("verified_groups.txt") as f:
    verified_groups_id = f.read().splitlines()


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_TextMessage(event):
    if event.message.text == "!getgid":
        msg = TextMessage(text=event.source.group_id)
        line_bot_api.reply_message(event.reply_token, msg)


@handler.add(MessageEvent, message=ImageMessage)
def handle_ImageMessage(event):
    try:
        time.sleep(10)
        dir_id = verified_groups_id[verified_groups_id.index(event.source.group_id) + 1]
        ext = "jpg"
        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(
            dir=os.path.dirname(__file__), delete=False
        ) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name
        dist_path = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "." + ext
        os.rename(tempfile_path, dist_path)
        file1 = drive.CreateFile({"parents": [{"id": dir_id}]})
        file1.SetContentFile(dist_path)
        file1.Upload()
        return 0
    except ValueError:
        print("no id found.")
    except Exception as e:
        print(e)


@handler.add(MessageEvent, message=VideoMessage)
def handle_ImageMessage(event):
    try:
        time.sleep(10)
        dir_id = verified_groups_id[verified_groups_id.index(event.source.group_id) + 1]
        ext = "mp4"
        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(
            dir=os.path.dirname(__file__), delete=False
        ) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name
        dist_path = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "." + ext
        os.rename(tempfile_path, dist_path)
        file1 = drive.CreateFile({"parents": [{"id": dir_id}]})
        file1.SetContentFile(dist_path)
        file1.Upload()
        return 0
    except ValueError:
        print("no id found.")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app.run()
