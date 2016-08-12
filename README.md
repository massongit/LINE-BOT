#名称
BOTっぽい何か ver.1.0.2

#作者
鈴木雅也

#開発言語
Python 3.5.2

#使用サービス
* [Heroku](https://www.heroku.com/)
* [日本語係り受け解析(Yahoo! JAPAN Webサービス)](http://developer.yahoo.co.jp/webapi/jlp/da/v1/parse.html)

#概要
[Heroku](https://www.heroku.com/)で動かすことを想定したLINE BOTです。

#機能
* 暴言が来たら、『なんだと(# ﾟДﾟ)』と返す
* 『{1文字以上の文字列}っぽー』と来たら、『ほっほー(・∀・)』と返す
* 上記2つに当てはまらない文字列が来たら、係り受け解析を行う

#LINE BOT API用CallBack URL
https://{アプリ名}.herokuapp.com:443/callback

#注意事項
Yahoo! JAPAN Webサービスへの登録が必要です(http://developer.yahoo.co.jp/start/)。

#デプロイ
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)