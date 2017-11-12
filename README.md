# BOTっぽい何か ver.1.0.2
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE) [![Maintainability](https://api.codeclimate.com/v1/badges/6b6ac25e1d6752fe67ae/maintainability)](https://codeclimate.com/github/massongit/LINE-BOT/maintainability)  
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## 概要
[Heroku](https://www.heroku.com/)で動かすことを想定したLINE BOTです。

## 開発環境
Python 3.6.2

## 使用サービス
* [Heroku](https://www.heroku.com/)
* [LINE Messaging API](https://developers.line.me/ja/services/messaging-api/)
* [日本語形態素解析 (Yahoo! JAPAN Webサービス)](https://developer.yahoo.co.jp/webapi/jlp/ma/v1/parse.html)

## 機能
* 暴言が来たら、『なんだと(# ﾟДﾟ)』と返す
* 『{1文字以上の文字列}っぽー』と来たら、『ほっほー(・∀・)』と返す
* 上記2つに当てはまらない文字列が来たら、文字列をひらがなに変換し、単語ごとに区切った上で返す

## Webhook URL ([LINE Messaging API](https://developers.line.me/ja/services/messaging-api/))
https://{アプリ名}.herokuapp.com/callback

## Config Variables ([Heroku](https://www.heroku.com/))
|||
|:--:|:--:|
|`LINE_CHANNEL_SECRET`|Channel Secret ([LINE Messaging API](https://developers.line.me/ja/services/messaging-api/))|
|`LINE_CHANNEL_ACCESS_TOKEN`|アクセストークン ([LINE Messaging API](https://developers.line.me/ja/services/messaging-api/))|
|`YAHOO_JAPAN_WEB_SERVICE_APPLICATION_ID`|アプリケーションID ([Yahoo! JAPAN Webサービス](https://developer.yahoo.co.jp/start/))|
|`DEBUG`|デバッグするかどうか (`True`, `False` / デフォルト値: `False`)|
