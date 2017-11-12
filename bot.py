# coding=utf-8
import os
import re

import bs4
import flask
import linebot
import requests
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

"""
BOTっぽい何か
"""

# プログラム情報
__author__ = 'Masaya SUZUKI'
__version__ = '1.0.2'

app = flask.Flask(__name__)
app.debug = bool(os.environ['DEBUG'])

api = linebot.LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = linebot.WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])

# 日本語形態素解析 (Yahoo! JAPAN Webサービス) のURL
yahoo_url = 'http://jlp.yahooapis.jp/DAService/V1/parse'

# 受信データ読み取り用パターン
patterns = [re.compile(r'.+っ+ほ'),
            re.compile(r'[あア][ー〜]*っ*[ほホ]'),
            re.compile(r'[ばバ][ー〜]*っ*[かカ]'),
            re.compile(r'(ドジ|どじ)'),
            re.compile(r'(マヌケ|まぬけ)')]


@app.route('/callback', methods=['POST'])
def callback():
    """
    コールバック
    """
    # get request body as text
    body = flask.request.get_data(as_text=True)
    app.logger.info('Request body:' + body)

    # handle webhook body
    try:
        handler.handle(body, flask.request.headers['X-Line-Signature'])
    except InvalidSignatureError:
        flask.abort(400)

    return 'OK'


@handler.default()
def handle(event):
    """
    デフォルトハンドラ
    :param event: イベント
    """
    api.reply_message(event.reply_token, event.message)


@handler.add(MessageEvent, TextMessage)
def handle_message(event):
    """
    メッセージハンドラ
    :param event: イベント
    """
    for pattern in patterns[1:]:
        if pattern.search(event.message.text) is not None:  # 受信データが暴言ならば、『なんだと(# ﾟДﾟ)』を返す
            text = 'なんだと(# ﾟДﾟ)'
            break
    else:
        if patterns[0].search(event.message.text) is not None:
            text = 'ほっほー(・∀・)'
        else:  # patternで定義されているパターンに当てはまらないならば、ひらがなに変換し、単語ごとに区切る
            text = get_hiragana(event.message.text)

    api.reply_message(event.reply_token, TextSendMessage(text))


def get_hiragana(text):
    """
    文字列をひらがなに変換し、単語ごとに区切った上で返す
    :param text: 文字列
    :return: ひらがなに変換し、単語ごとに区切った文字列
    """
    # 日本語形態素解析 (Yahoo! JAPAN Webサービス) 用のデータ
    data = {'appid': os.environ['YAHOO_JAPAN_WEB_SERVICE_APPLICATION_ID'],
            'sentence': text, 'response': 'reading'}

    # ひらがなのリスト
    hiragana = list()

    for word in bs4.BeautifulSoup(requests.post(yahoo_url, data).content, 'html.parser').find_all('reading'):
        hiragana.append(word.text)

    return ' '.join(hiragana)


if __name__ == '__main__':
    app.run()
