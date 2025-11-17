#!/usr/bin/env python3
#
# pokemon_gotcha.py
#
# [概要]
# 公式の「ポケモンずかん」
# （https://zukan.pokemon.co.jp/）
# を参照して，好きなポケモンの画像を
# 取得して保存するプログラム．
#


from bs4 import BeautifulSoup
import requests

from features.setup_logging import setup_logging
from features.setup_selenium import setup_driver, driver_wait

from logging import getLogger
from pathlib import Path
import time
import sys
import os


# loggingの設定を反映して，専用のロガーを作成
setup_logging()
logger = getLogger(__name__)

driver = setup_driver()


def scroll_page(url):
    assert isinstance(url, str), "url は文字列型である必要があります"
    
    try:
        logger.info("指定のサイトへアクセスします")
        driver.get(url)
        driver_wait(driver)
        logger.info(
            f"指定のサイトへアクセスできました: {driver.title}"
        )

        logger.info("ブラウザで全ポケモンを表示するためにスクロールを開始")

        last_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            time.sleep(2)

            new_height = driver.execute_script(
                "return document.body.scrollHeight"
            )

            if new_height == last_height:
                logger.info("ページの最下部に到達しました")
                break
            last_height = new_height

        return driver.page_source

    except Exception as e:
        logger.error(
            f"画面のスクロール中にエラーが発生しました: {e}"
        )
        raise


def make_soup(page_source):
    '''
    [概要]
    指定された url (今回は公式のポケモンずかん) を参照して，
    BeautifulSoup オブジェクト (soup) を作成し，返す関数．

    Arg:
        url (str): 情報を取得したい Webサイトの URL を指定．
    '''
    #assert isinstance(url, str), "url引数を文字列型で指定してください．"

    try:
        logger.info(
            "driverで取得した HTML を読み込んでオブジェクトを作成します"
        )
        soup = BeautifulSoup(
            page_source, "html.parser"
        )
        logger.info(
            "BeautifulSoup オブジェクトを作成しました"
        )

        return soup

    except Exception as e:
        logger.error(
            f"BeautifulSoup オブジェクトの作成時にエラーが発生しました: {e}"
        )
        raise


def new_make_soup(url):
    '''
    [概要]
    指定された url (今回は公式のポケモンずかん) を参照して，
    BeautifulSoup オブジェクト (soup) を作成し，返す関数．

    Arg:
        url (str): 情報を取得したい Webサイトの URL を指定．
    '''
    #assert isinstance(url, str), "url引数を文字列型で指定してください．"

    try:
        logger.info(
            "driverで取得した HTML を読み込んでオブジェクトを作成します"
        )
        response = requests.get(url)
        soup = BeautifulSoup(
            response.text, "html.parser"
        )
        logger.info(
            "BeautifulSoup オブジェクトを作成しました"
        )

        return soup

    except Exception as e:
        logger.error(
            f"BeautifulSoup オブジェクトの作成時にエラーが発生しました: {e}"
        )
        raise


def found_img_source(soup, name, tag="img"):
    '''
    ''' 
    try:
        logger.info("指定の画像を見つけます")
        img_tags = soup.select(tag)
        logger.debug(
            f"img_tagsの中身: {len(img_tags)}"
        )
        for img in img_tags:
            alt_text = img.get("alt")

            if alt_text == name:
                logger.info(
                    f"{name}の気配がする・・・"
                )

                img_src = img.get("src")

                if not img_src:
                    logger.warning(
                        f"{name}はここにはいないようだ・・・"
                    )

        return img_src

    except Exception as e:
        logger.error(
            f"画像検索中にエラーが発生しました: {e}"
        )
        raise


def gotcha(url, img_src, save_img_path):
    try:
        img_url = f"{img_src}"
        logger.info(
            f"指定の URL へリクエストを送ります: {img_url}"
        )
        img_response = requests.get(img_url)
        img_response.raise_for_status()

        logger.info(
            "ポケモンを見つけました!"
        )

        logger.info(
            "捕獲します!"
        )

        with open(save_img_path, "wb") as f:
            f.write(img_response.content)

        logger.info(
            f"ポケモンを捕獲しました!: {save_img_path}"
        )

        return True

    except Exception as e:
        logger.error(
            f"捕獲に失敗しました: {e}"
        )
        raise


def main():
    url = "https://zukan.pokemon.co.jp/"
    name = "テラパゴス"

    save_dir = Path("output")
    save_dir.mkdir(exist_ok=True)
    
    img_name = f"gotcha_{name}.png"

    save_img_path = save_dir / img_name

    page_source = scroll_page(url)
    
    soup = make_soup(page_source)
    img_src = found_img_source(soup, name)

    gotcha(url, img_src, save_img_path)

    driver.quit()
    

if __name__ == "__main__":
    main()
    
