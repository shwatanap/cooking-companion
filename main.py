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

import config
from gpt.reply import create_recipe

app = Flask(__name__)

# config.pyで設定したチャネルアクセストークン
LINE_CHANNEL_ACCESS_TOKEN = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
# config.pyで設定したチャネルシークレット
LINE_CHANNEL_SECRET = WebhookHandler(config.LINE_CHANNEL_SECRET)
# LINEBotの応答メッセージで使う単語
REPLY_KEYWORDS = ["レシピ", "食材", "ジャンル"]


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        LINE_CHANNEL_SECRET.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@LINE_CHANNEL_SECRET.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # APIのヘルスチェック用
    if event.reply_token == "00000000000000000000000000000000":
        return

    user_input = event.message.text

    # 応答メッセージで設定されている単語が含まれていたら、何もしない
    if user_input in REPLY_KEYWORDS:
        return

    output = create_recipe(user_input)

    LINE_CHANNEL_ACCESS_TOKEN.reply_message(
        event.reply_token,
        TextSendMessage(text=output)
    )

if __name__ == "__main__":
    app.run(host="localhost", port=8000)   # ポート番号を8000に指定
