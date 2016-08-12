import json
import logging
import os
import re

import falcon
import requests

"""
BOTっぽい何か
"""

# プログラム情報
__author__ = 'Masaya SUZUKI'
__version__ = '1.0'


class CallbackResource:
    """
    コールバック用クラス
    """

    @staticmethod
    def on_post(req, resp):
        """
        POSTメソッドによってコールバックされた際の処理
        :param resp: レスポンス
        :param req: リクエスト
        """

        # リクエストのBody
        body = req.stream.read()

        # リクエストのBodyが空ならば、HTTPBadRequestを返す
        if not body:
            raise falcon.HTTPBadRequest('Empty request body', "A valid JSON document is required.")

        # リクエストのBodyをディクショナリ化
        body = json.loads(body.decode('utf-8'))

        logger.debug('body: {}'.format(body))

        # 受信データを処理
        for req_data in body['result']:
            logger.debug('req_data: {}'.format(req_data))

            # 送信データ
            res_data = {
                'to': [req_data['content']['from']],
                'toChannel': 1383378250,
                'eventType': '138311608800106203'
            }

            # 受信データが文字以外(スタンプ等)である、または、正規表現『.+っほー.*』に当てはまらないパターンならばオウム返し
            if req_data['content']['text'] is None or not re.match(r'.+っほー.*', req_data['content']['text']):
                res_data['content'] = req_data['content']
            # 受信データが正規表現『.+っほー.*』に当てはまるパターンのとき
            else:
                res_data['content'] = {
                    'contentType': 1,
                    'toType': 1
                }

                if req_data['content']['text'] == 'あっほー':  # 受信データが『あっほー』ならば、『なんだと(# ﾟДﾟ)』を返す
                    res_data['content']['text'] = 'なんだと(# ﾟДﾟ)'
                else:  # 受信データが『あっほー』以外で正規表現『.+っほー.*』に当てはまるパターンならば、『ほっほー(・∀・)』を返す
                    res_data['content']['text'] = 'ほっほー(・∀・)'

            # 送信データを文字列化
            res_data = json.dumps(res_data)

            logger.debug('res_data: {}'.format(res_data))

            # レスポンスを送信
            res = requests.post('https://trialbot-api.line.me/v1/events',
                                data=res_data,
                                headers={
                                    'Content-Type': 'application/json; charset=UTF-8',
                                    'X-Line-ChannelID': os.environ['LINE_CHANNEL_ID'],
                                    'X-Line-ChannelSecret': os.environ['LINE_CHANNEL_SECRET'],
                                    'X-Line-Trusted-User-With-ACL': os.environ['LINE_CHANNEL_MID']
                                },
                                proxies={'https': os.environ.get('FIXIE_URL', '')})

            logger.debug('res: {} {}'.format(res.status_code, res.reason))

            # 正常に送信された旨を送信
            resp.body = json.dumps('OK')


# logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

# 『/callback』がコールバックされた際に、CallbackResourceを呼び出すように設定
api = falcon.API()
api.add_route('/callback', CallbackResource())
