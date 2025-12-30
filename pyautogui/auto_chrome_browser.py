#!/usr/bin/env python3
#
# auto_chrome_browser.py
#
# [概要]
# pyautoguiモジュールを使って
# Chromeブラウザを操作し，
# 担当教員とTAそれぞれのGitHubリポジトリを
# ブックマークするプログラム．
#
# 実行にあたり，ブラウザやOSの背景色は「黒」
# あらかじめChromeブラウザを展開しておくなどの
# 条件がある．
#

import pyautogui

from features.setup_logging import setup_logging

from logging import getLogger
from pathlib import Path
import time

# 専用のロガーを作成
logger = getLogger(__name__)

# logging の設定を適用
logging_config = Path("./config/logging_config.yml")
setup_logging(logging_config)


class AutoBot:
    def __init__(self, image_dir=Path("input"), confidence=0.9):
        self.image_dir = image_dir
        self.confidence = confidence

    def find_image(self, image_name, retries=30, interval=1.0):
        '''
        [概要]
        指定された画像と一致する部分を探して，見つけたら座標を取得するメソッド
        '''
        image_path = self.image_dir / image_name

        if image_path.exists() == False:
            logger.error(
                "指定の画像ファイルが存在していません"
            )
            raise FileNotFoundError

        logger.debug("> 画像と一致する箇所を探す")
        for _ in range(retries):
            try:
                location = pyautogui.locateCenterOnScreen(
                    str(image_path),
                    confidence=self.confidence,
                    grayscale=True
                )
                if location:
                    logger.debug("> 画像と一致する箇所を発見")
                    return location

            except pyautogui.ImageNotFoundException:
                pass

            except Exception:
                pass

        logger.warning(">>> 画像と一致する箇所が見つからない")
        raise Exception(
            ">>>> 画像と一致する箇所が見つからなかった"
        )

    def click_image(self, image_name, wait_after=0.5):
        '''
        [概要]
        画像と一致する部分の座標を受け取り，該当箇所をクリックするメソッド
        '''
        x, y = self.find_image(image_name)
        pyautogui.click(x, y)
        time.sleep(wait_after)

    def type_text(self, text):
        '''
        [概要]
        テキストを書き込み"Enter"キーを押すメソッド
        '''
        try:
            pyautogui.write(text, interval=0.3)
            time.sleep(1)
            pyautogui.press("enter")

        except Exception as e:
            logger.error(
                f"テキスト書き込み時にエラー発生: {e}"
            )
            raise e


class AutoChrome(AutoBot):
    def __init__(self, target_urls, image_dir=Path("input")):
        super().__init__(image_dir=image_dir, confidence=0.9)
        self.target_urls = target_urls

    def execute(self):
        '''
        [概要]
        継承したAutoBotクラスのメソッドを駆使して
        Chromeブラウザを操作し，該当サイトをブックマークするメソッド
        '''
        try:
            logger.debug("> Chromeブラウザ自動操作開始")
            for url in self.target_urls:
                logger.debug("> 新しいタブを開く")
                self.click_image("new_tab_icon.png")
                time.sleep(1.5)

                logger.debug(f"> URLを入力する: {url}")
                self.type_text(url)
                time.sleep(1)

                logger.debug("> ブックマークに追加する")
                self.click_image("bookmark_icon.png")

            logger.debug("> 操作終了")

        except Exception as e:
            logger.error(
                f"Chromeブラウザ操作中にエラー発生: {e}"
            )
            raise e
        
        
if __name__ == "__main__":
    pyautogui.FAILSAFE = True

    input_dir = Path("./input")
    target_urls = [
        "https://github.com/yamasound/pp2",
        "https://github.com/kaimorgn/ta_pp2"
    ]
        
    chromebot = AutoChrome(
        target_urls=target_urls,
        image_dir=input_dir
    )

    logger.info(
        ">> 2秒後に自動操作が開始します．操作端末から手を離してください"
    )
    time.sleep(2)

    try:
        chromebot.execute()

    except Exception as e:
        logger.error(
            f"実行中にエラー発生: {e}"
        )
