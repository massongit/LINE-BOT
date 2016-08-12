import json
import logging
import os
import re

import bs4
import falcon
import requests

"""
BOTっぽい何か
"""

# プログラム情報
__author__ = 'Masaya SUZUKI'
__version__ = '1.0.2'


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

        # 受信データ読み取り用パターン
        pattern = [re.compile(r'.+っ+ほ'),
                   re.compile(r'[あア][ー〜]*っ*[ほホ]'),
                   re.compile(r'[ばバ][ー〜]*っ*[かカ]'),
                   re.compile(r'(ドジ|どじ)'),
                   re.compile(r'(マヌケ|まぬけ)')]

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
            res_data = {'to': [req_data['content']['from']], 'toChannel': 1383378250, 'eventType': '138311608800106203'}

            if req_data['content']['text']:  # 受信データが文字であるとき
                res_data['content'] = {'contentType': 1, 'toType': 1}

                # patternで定義されている各パターンに当てはまるかどうか
                pr = [p.search(req_data['content']['text']) is not None for p in pattern]

                if 0 < pr[1:].count(True):  # 受信データが暴言ならば、『なんだと(# ﾟДﾟ)』を返す
                    res_data['content']['text'] = 'なんだと(# ﾟДﾟ)'
                elif pr[0]:  # 受信データが暴言でなく、かつ、正規表現『.+っほー.*』に当てはまるパターンならば、『ほっほー(・∀・)』を返す
                    res_data['content']['text'] = 'ほっほー(・∀・)'
                else:  # patternで定義されているパターンに当てはまらないならば、係り受け解析を行い、結果を返す
                    # 係り受け解析結果
                    da = requests.post('http://jlp.yahooapis.jp/DAService/V1/parse',
                                       {'appid': os.environ['YAHOO_JAPAN_WEB_SERVICE_APPLICATION_ID'],
                                        'sentence': req_data['content']['text']})

                    # 結果
                    r = list()
                    r.append('\t'.join(['文節番号', '修飾先の文節番号', '表記', 'よみがな', '基本形表記', '品詞', '形態素情報']))

                    for c in bs4.BeautifulSoup(da.content, "html.parser").find_all('chunk'):
                        for m in c.find_all('morphem'):
                            r.append('\t'.join([t.text.replace('\n', '{改行}') for t in [c.find('id'),
                                                                                       c.find('dependency'),
                                                                                       m.find('surface'),
                                                                                       m.find('reading'),
                                                                                       m.find('baseform'),
                                                                                       m.find('pos'),
                                                                                       m.find('feature')]]))

                    res_data['content']['text'] = '\n'.join(r)
            else:  # 受信データが文字でないならば、オウム返しする
                res_data['content'] = req_data['content']

            # 送信データを文字列化
            res_data = json.dumps(res_data)

            logger.debug('res_data: {}'.format(res_data))

            # レスポンスを送信
            res = requests.post('https://trialbot-api.line.me/v1/events',
                                data=res_data,
                                headers={'Content-Type': 'application/json; charset=UTF-8',
                                         'X-Line-ChannelID': os.environ['LINE_CHANNEL_ID'],
                                         'X-Line-ChannelSecret': os.environ['LINE_CHANNEL_SECRET'],
                                         'X-Line-Trusted-User-With-ACL': os.environ['LINE_CHANNEL_MID']},
                                proxies={'https': os.environ['FIXIE_URL']})

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
