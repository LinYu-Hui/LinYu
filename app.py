from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('xsK7hIqxvam2Z24TzWkxgkMUFJkb5JeTSSsm/wR4OYivRC+S+xoEVpYGJUgdhndaBsryY+jvMS2M/RRfsaKCkOnmo0XNWQ6hzs/al0Kiwhke5kC2vCWWXfCylhadUftw06knxyH7wnrhzsXwIJwxQgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('daf7afc1a819727be8b68dfb3f413a80')


@app.route("/")
def home():
    return 'home OK'

# 監聽所有來自 /callback 的 Post Request
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
    