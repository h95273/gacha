from flask import Flask, request, redirect, render_template
import random
import os

app = Flask(__name__)

# 使った金額、出たカードの種類等を保存するデータファイル
DATAFILE = './data.txt'

# 買った枚数、使ったお金を扱う変数。グローバル変数。
# この値は、ファイルから読み込む。
# 買った枚数は、まだ対応していません。対応する必要あり。
# 11連ガチャでも対応する必要あり。
number_of_cards = 0
if os.path.exists(DATAFILE):
    with open(DATAFILE, 'rt') as f:
        # moneyはint型。intに変換しておく。
        money = int(f.read())
else:
    money = 0

# ルートにアクセスしたとき
@app.route('/')
def index():
    return render_template('index.html')

# 1回まわすガチャのページにアクセスしたとき
@app.route('/gacha1')
def gacha1():
    #買った枚数、使ったお金を扱う変数。グローバル変数。
    global number_of_cards
    global money

    # number_of_cardsに1追加する。
    number_of_cards +=  1
    # moneyに100追加する。
    money += 100  # ←は、money = money + 100 と同じ。
    # moneyをサーバにあるファイルに書き込む。
    with open(DATAFILE, 'wt') as f:
        # 文字列じゃないとwriteは使えない。
        f.write( str(money) )

    # この下に乱数の処理を書く。
    # どのカードの種類が当たるか抽選する。
    lottery = random.randint(1, 100)  # 抽選の数字

    # 抽選結果が1～33(33個)のときN
    if lottery <= 33:
        card_class = "N"
    # 抽選結果が34～58(25個)のときN+
    elif lottery <= 33 + 25:
        card_class = "N+"
    # 抽選結果が59～78(20個)のときR
    elif lottery <= 33 + 25 + 20:
        card_class = "R"
    # 途中略（修正が必要）
    # 抽選結果が99～100(2個)のときSR+
    else:
        card_class = "SR+"

    return render_template('gacha1.html',
                           card_class=card_class,
                           number_of_cards=number_of_cards,
                           money=money)

# 11回まわすガチャのページにアクセスしたとき
@app.route('/gacha11')
def gacha11():
    #買った枚数、使ったお金を扱う変数。グローバル変数。
    global number_of_cards
    global money

    # number_of_cardsに11追加する。
    number_of_cards +=  11
    # moneyに1000追加する。
    money += 1000  # ←は、money = money + 1000 と同じ。

    # この下に乱数の処理を書く。
    # どのカードの種類が当たるか抽選する。
    lottery_list = []  # 抽選した複数の数字を格納するリスト
    card_class_list = []  # カードの種類を格納するリスト
    # 処理を10回繰り返す。iは「0」から「9」の整数が入る。
    for i in range(10):
        num = random.randint(1, 100)  # 抽選の数字
        # lottery_listリストの最後に、抽選した数字numを追加する。
        lottery_list.append(num)

        # 抽選結果が1～57(57個)のときR
        if lottery_list[i] <= 57:
            card_class_list.append("R")
        # 抽選結果が58～88(30個)のときR+
        elif lottery_list[i] <= 57 + 30:
            card_class_list.append("R+")
        # 途中略（修正が必要）
        # 抽選結果が98～100(3個)のときSR+
        else:
            card_class_list.append("SR+")

    # 10個の抽選後にSRを追加する。
    card_class_list.append("SR")

    return render_template('gacha11.html', card_class_list=card_class_list)

# リセットをクリックしたとき
# リセットしたらルートのページを表示する（indexのページが表示されたまま）
@app.route('/reset')
def reset():
    #買った枚数、使ったお金を扱う変数。グローバル変数。
    global number_of_cards
    global money

    # 金額を記録しているファイルを消すことで金額をゼロにする。
    # （あるいは、money=0をファイルに上書きすることでもOK）
    money = 0
    os.remove(DATAFILE)
    # ルートにリダイレクト（アクセス）する。
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
