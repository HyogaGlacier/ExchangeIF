# ExchangeIF
one of Esolang using EXIF Data. It works on hakatashi/esolang-box.

### How to Use
prepare pictures, and zip these pictures. and
```bash
ExchangeIF [zipfile]
```
to execute.

### Documentation
取り敢えず日本語で書いておく。

* ルールその1	プログラムは作成日時の早い順に実行されていきます。同時刻のファイルがある際の動作はランダムです。
* ルールその2	変数はGPS座標で識別します。latitude, longitudeで識別します。各変数には数値が1つだけ入ります。
* ルールその3	1コマンドは1つの画像からなり、コマンド及びその文法については以下のようになっています。

コマンド	条件			影響先	影響元
代入		ISOが0~99	GPS(lat)		画像サイズ（縦×横がそのまま入る）
入力		ISOが100~199	GPS(lat)		無し（標準入力から1文字文字コードとして受け取ります）
出力		ISOが200~299	無し（標準出力へ文字コード1文字）		GPS(lng)
加算		ISOが300~399	GPS(lat)		GPS(lng)
減算		ISOが400~499	GPS(lat)		GPS(lng)
乗算		ISOが500~599	GPS(lat)		GPS(lng)
除算		ISOが600~699	GPS(lat)		GPS(lng)
剰余		ISOが700~799	GPS(lat)		GPS(lng)

* ルールその4	タイムトラベルが可能です。
タイムトラベル		
ただし、タイムトラベルの代償として「現在時刻との差の絶対値の時間」を無為に消費します。時間切れに気を付けましょう。
ISOコマンドとタイムトラベルの優先順位はタイムトラベルが上です。

ルールその5	GPS座標はlat、lng共通です。Metering Modeを2進数として見たとき、下2桁について、
下1桁が1→lngはlngが示す値の変数を参照します
下2桁目が1→latはlatが示す値の変数を参照します

実質bfなので面白みはありません。変則ショートコーティングに挑んでください。

### Samples
* HelloWorld
面倒だったのでHだけ出力。許してくだせぇ…
* cat