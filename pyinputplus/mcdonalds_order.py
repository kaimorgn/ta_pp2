#!/usr/bin/env python3
#
# mcdonalds_order.py
# 
# [概要]
#
#
#
#
#

import pyinputplus as pyip
import re

BURGER_PRICES = {
    "ビッグマック": 480,
    "炙り醤油風 ダブル肉厚ビーフ": 580,
    "炙り醤油風 たまごベーコン肉厚ビーフ": 570,
    "ダブルチーズバーガー": 450,
    "チキチー": 250
}

SIDEMENU_PRICES = {
    "マックフライポテト(M)": 330,
    "チキンマックナゲット(5P)": 290,
    "サイドサラダ": 350,
    "えだまめコーン": 300,
    "シャカチキ": 220
}

DRINK_PRICES = {
    "コカ・コーラ(M)": 270,
    "スプライト(M)": 270,
    "ファンタ メロン(M)": 270,
    "爽健美茶": 270,
    "プレミアムローストコーヒー(M)": 180
}


def burger_order():
    burger = pyip.inputMenu(
        (
            "ビッグマック",
            "炙り醤油風 ダブル肉厚ビーフ",
            "炙り醤油風 たまごベーコン肉厚ビーフ",
            "ダブルチーズバーガー",
            "チキチー"
        ),
        prompt="お好みのバーガーを選択してください．\n",
        numbered=True
    )

    return burger


def sidemenu_order():
    sidemenu = pyip.inputMenu(
        (
            "マックフライポテト(M)",
            "チキンマックナゲット(5P)",
            "サイドサラダ",
            "えだまめコーン",
            "シャカチキ"
        ),
        prompt="サイドメニューを選択してください．\n",
        numbered=True
    )

    return sidemenu


def drink_order():
    drink = pyip.inputMenu(
        (
            "コカ・コーラ(M)",
            "スプライト(M)",
            "ファンタ メロン(M)",
            "爽健美茶",
            "プレミアムローストコーヒー(M)"
        ),
        prompt="お飲み物を選んでください．\n",
        numbered=True
    )

    return drink


def order_check():
    decision = pyip.inputYesNo(
        "ご注文は以上でよろしいでしょうか?\n",
        yesVal="はい",
        noVal="いいえ"
    )

    return decision


def accountiong(total_price):
    try:
        cash = pyip.inputInt(
            "5秒以内にお支払いください．\n",
            limit=3,
            timeout=5,
            blockRegexes=[(r"^0$", "0円では支払えません．")]
        )

        if cash < total_price:
            print("現金が足りません．取引をキャンセルします．")

        else:
            change = cash - total_price
            print(f"お支払いありがとうございます．お釣りは {change} 円です．")
            return change

    except pyip.RetryLimitException:
        print("3回の入力を超えました．取引をキャンセルします．")
        return 
        
    except pyip.TimeoutException:
        print("時間切れです．取引をキャンセルします．")
        return
    

def price_check():
    total_price = 0

    while True:
        burger = burger_order()
        total_price += BURGER_PRICES[burger]
    
        sidemenu = sidemenu_order()
        total_price += SIDEMENU_PRICES[sidemenu]
    
        drink = drink_order()
        total_price += DRINK_PRICES[drink]

        decision = order_check()
        if decision == "はい":
            break
        
    print("-" * 15)
    print(f"お会計は {total_price} 円となります．")

    accountiong(total_price)
    

if __name__ == "__main__":
    price_check()
