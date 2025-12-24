#!/usr/bin/env python3
#
# json_io.py
#
# [概要]
# json モジュールを使った基本操作
# ・既存ファイルからのデータ読み取り
# ・JSON ファイルを新規作成して書き込み
# ・既存の JSON ファイルに書き込み
# を定義したプログラム
# 

from logging import getLogger
from pathlib import Path
import json

# 専用のロガーを作成
logger = getLogger(__name__)


class JSONIO:
    def __init__(self):
        pass

    def read_json_data(self, json_path):
        '''
        [概要]
        既存のJSONファイルからデータを取得するメソッド
        '''
        assert json_path, "JSONファイルパスを渡して"
        assert isinstance(json_path, Path), "JSONのPathオブジェクトを渡して"

        if json_path.exists() == False:
            logger.warning(
                f">>> {json_path} が存在していない"
            )
            raise FileNotFoundError
            
        try:
            logger.debug(f"> データを取得する")
            with open(json_path, "r", encoding="utf-8") as json_file:
                self.json_data = json.load(json_file)
                logger.debug(
                    f"> 取得したデータ: {self.json_data}"
                )
                logger.info(f">> {len(self.json_data)} 個のデータを取得した")
                return self.json_data

        except Exception as e:
            logger.error(
                f"データ取得時にエラーが発生: {e}"
            )
            raise e
        
    def write_json_data(self, data, save_json_path=Path("./output.json")):
        '''
        [概要]
        JSONファイルにデータを書き込むメソッド
        書き込み対象のJSONが存在しない場合でも新規作成した上で書き込む
        '''
        assert data, "書き込むデータを辞書型・JSON型で渡して"
        
        assert save_json_path, "JSONファイルパスを渡して"
        assert isinstance(save_json_path, Path), "Pathオブジェクトを渡して"

        if save_json_path.exists() == False:
            save_json_path.touch()
            logger.info(
                f">> {save_json_path} がないので新規作成した"
            )

        try:
            logger.debug(f"> {save_json_path} にデータを書き込む")
            with open(save_json_path, "w", encoding="utf-8") as json_file:
                json.dump(
                    data, json_file, ensure_ascii=False, indent=4
                )
            logger.info(
                f">> {len(data)} 個のデータを書き込んだ"
            )

        except Exception as e:
            logger.error(
                f"データ書き込み時にエラーが発生: {e}"
            )
            raise e


if __name__ == "__main__":
    from setup_logging import setup_logging

    logging_path = Path("../config/logging_config.yml")
    setup_logging(logging_path)

    data = {
        "id": 1,
        "name": "Python 3.10",
        "features": ["Type Hinting", "Pattern Matching"],
        "is_active": True,
        "note": "日本語のテスト書き込み"
    }
    #JSONIO().write_json_data(data)
    JSONIO().read_json_data(
        Path("output.json")
    )
