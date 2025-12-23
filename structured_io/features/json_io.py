#!/usr/bin/env python3
#
# json_io.py
#
# [概要]
#
#
#
#
#
#
# 

from logging import getLogger
from pathlib import Path
import json

# 専用のロガーを作成
logger = getLogger(__name__)


class JSONIO:
    def __init__(self, json_path, mode):
        pass

    def read_json_data(self):
        '''
        '''
        data = {}
        try:
            logger.debug(f"> データを取得する")
            for row in self.reader:
                data.append(row)

            logger.info(f">> データを取得した: {len(data)}")
            return True

        except Exception as e:
            logger.error(
                f"データ取得時にエラーが発生: {e}"
            )
            raise e
        
    def _make_reader(self, json_path):
        '''
        '''
        assert json_path, "JSONを指定していない"
        assert isinstance(json_path, Path), "JSONはPathオブジェクトで指定"

        if json_path.exists() == False:
            logger.warning(f">>> {json_path} が存在していません")
            raise FileNotFoundError

        try:
            logger.info(f">> {json_path} 読み取り用のインスタンス変数を生成")
            with open(json_path, mode="r", encoding="utf-8") as json_file:
                self.reader = json.reader(json_path)

            return True

        except Exception as e:
            logger.error(
                f"読み取り用のインスタンス変数生成中にエラーが発生: {e}"
            )
            raise e


if __name__ == "__main__":
    from setup_logging import setup_logging

    logging_path = Path("../config/logging_config.yml")
    setup_logging(logging_path)

    json_io = JSONIO()
