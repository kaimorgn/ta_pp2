#!/usr/bin/env python3
#
# csv_io.py
#
# [概要]
# CSV モジュールを使った基本操作
# ・データの読み取り
# ・CSVファイルを新規作成して書き込み
# ・既存のCSVファイルに書き込み
# を定義したプログラム
#

from logging import getLogger
from pathlib import Path
import csv

# 専用のロガーを作成
logger = getLogger(__name__)


class CSVIO:
    def __init__(self, csv_path, mode):
        if mode == "read":
            self._make_reader(csv_path)

        elif mode == "write":
            self._make_writer(csv_path)

        elif mode == "add":
            self._make_additioner(csv_path)

    def read_csv_data(self, csv_path):
        '''
        [概要]
        _make_reader() で生成したインスタンス変数を使って
        CSV からデータを取得するメソッド
        '''
        data = []
        try:
            logger.debug(f"> {csv_path} からデータを取得する")
            for row in self.reader:
                data.append(row)

            logger.info(f">> {csv_path} からデータを取得した: {len(data)}")
            return data

        except Exception as e:
            logger error(
                f"{csv_path} からデータ取得時にエラーが発生: {e}"
            )
            raise e

    def _make_reader(self, csv_path):
        '''
        [概要]
        CSVからデータを読み取る self.reader を生成するためのメソッド
        '''
        assert csv_path, "CSVを指定していない"
        assert isinstance(csv_path, Path), "CSVはPathオブジェクトで指定"

        if csv_path.exists() == False:
            logger.warning(f">>> {csv_path} が存在していません")
            raise FileNotFoundError
        
        try:
            logger.info(f">> {csv_path} 読み取り用インスタンス変数を生成")
            with open(csv_path, mode="r", encoding="utf-8") as csv_file:
                self.reader = csv.reader(csv_path)

            return True

        except Exception as e:
            logger.error(
                f"読み取り用インスタンス変数生成中にエラーが発生: {e}"
            )
            raise e

    def write_data(self, csv_path, data_lists):
        '''
        [概要]
        _make_writer() で生成したインスタンス変数を使って
        CSVにデータを書き込むメソッド
        '''
        try:
            logger.debug(f"> {csv_path} に {len(data_list)} 個書き込む")
            for data in data_lists:
                self.writer.writerow(row)

            logger.debug(f"> {csv_path} に {len(data_list)} 個書き込んだ")
            return True

        except Exception as e:
            logger.error(
                f"データ書き込み時にエラーが発生: {e}"
            )
            raise e
        
    def _make_writer(self, csv_path):
        '''
        [概要]
        CSVを新規作成して書き込む self.writer を生成するためのメソッド
        '''
        assert csv_path, "CSVを指定していない"
        assert isinstance(csv_path, Path), "CSVはPathオブジェクトで指定"

        if csv_path.exists() == False:
            logger.info(f">> {csv_path} が存在していないので新規作成する")
        
        try:
            logger.info(f">> {csv_path} 書き込み用インスタンス変数を生成")
            with open(csv_path, mode="w", encoding="utf-8") as csv_file:
                self.writer = csv.writer(csv_path)

            return True

        except Exception as e:
            logger.error(
                f"書き込み用インスタンス変数生成中にエラーが発生: {e}"
            )
            raise e

    def add_data_csv(self, csv_path, data_lists):
        '''
        '''
        try:
            logger.debug(f"> {csv_path} にデータを追記する: {len(data_lists)}")
            for data in data_lists:
                self.additioner.writerow(data)

            logger.info(f">> {csv_path} にデータを追記した: {len(data_lists)}")
            return True

        except Exception as e:
            logger.error(
                f"データの追記時にエラーが発生: {e}"
            )
            raise e

    def _make_additioner(self, csv_path):
        '''
        [概要]
        既存のCSVにデータを追記する self.additioner を生成するためのメソッド
        '''
        assert csv_path, "CSVを指定していない"        
        assert isinstance(csv_path, Path), "CSVはPathオブジェクトで指定"

        if csv_path.exists() == False:
            logger.warning(f">>> {csv_path} が存在していません")
            raise FileNotFoundError
        
        try:
            logger.info(f">> {csv_path} 追記するためのインスタンス変数を生成")
            with open(csv_path, mode="a", encoding="utf-8") as csv_file:
                self.additioner = csv.writer(csv_path)

            return True

        except Exception as e:
            logger.error(
                f"追記するためのインスタンス変数生成中にエラーが発生: {e}"
            )
            raise e


if __name__ == "__main__":
    from setup_logging import setup_logging

    logging_config = Path("../config/logging_config.yml")
    setup_logging(logging_config)

    csv_path = Path("./input/XXX.csv")
    csv_io = CSVIO()
    csv_io.XXX(csv_path)
