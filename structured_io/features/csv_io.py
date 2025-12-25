#!/usr/bin/env python3
#
# csv_io.py
#
# [概要]
# csv モジュールを使った基本操作
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
    def __init__(self):
        pass

    def read_csv_data(self, csv_path):
        '''
        [概要]
        _make_reader() で生成した変数を使って
        CSV からデータを取得するメソッド
        '''
        assert csv_path, "CSVを指定していない"
        assert isinstance(csv_path, Path), "CSVはPathオブジェクトで指定"

        if csv_path.exists() == False:
            logger.warning(f">>> {csv_path} が存在していません")
            raise FileNotFoundError

        data = []
        try:
            logger.info(f">> {csv_path} 読み取り用変数を生成")
            with open(csv_path, mode="r", encoding="utf-8") as csv_file:
                reader = csv.reader(csv_file)
        
                logger.debug(f"> データを取得する")
                for row in reader:
                    data.append(row)

            #logger.debug(f"取得したデータ: {data}")
            logger.info(f">> データを取得した: {len(data)}")
            return data

        except Exception as e:
            logger.error(
                f"データ取得時にエラーが発生: {e}"
            )
            raise e

    def write_data(self, data_lists, save_csv_path="output.csv"):
        '''
        [概要]
        _make_writer() で生成した変数を使って
        CSVにデータを書き込むメソッド
        '''
        assert save_csv_path, "CSVを指定していない"
        assert isinstance(save_csv_path, Path), "CSVはPathオブジェクトで指定"

        if save_csv_path.exists() == False:
            save_csv_path.touch()
            logger.info(
                f">> {save_csv_path} が存在していないので新規作成する"
            )
        
        try:
            logger.info(f">> {csv_path} 書き込み用変数を生成")
            with open(save_csv_path, mode="w", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
        
                logger.debug(f"> {len(data_lists)} 個書き込む")
                for data in data_lists:
                    writer.writerow(data)

            logger.debug(f"> {len(data_lists)} 個書き込んだ")
            return True

        except Exception as e:
            logger.error(
                f"データ書き込み時にエラーが発生: {e}"
            )
            raise e
    
    def add_data_csv(self, data_lists, csv_path):
        '''
        '''
        assert csv_path, "CSVを指定していない"        
        assert isinstance(csv_path, Path), "CSVはPathオブジェクトで指定"

        if csv_path.exists() == False:
            logger.warning(f">>> {csv_path} が存在していません")
            raise FileNotFoundError
        
        try:
            logger.info(f">> {csv_path} 追記するための変数を生成")
            with open(csv_path, mode="a", encoding="utf-8") as csv_file:
                additioner = csv.writer(csv_file)
                
                logger.debug(f"> データを追記する: {len(data_lists)}")
                for data in data_lists:
                    additioner.writerow(data)

            logger.info(f">> データを追記した: {len(data_lists)}")
            return True

        except Exception as e:
            logger.error(
                f"データの追記時にエラーが発生: {e}"
            )
            raise e


if __name__ == "__main__":
    from setup_logging import setup_logging

    logging_config = Path("../config/logging_config.yml")
    setup_logging(logging_config)

    csv_path = Path("output.csv")
    csv_handler = CSVIO()
    input_data = [
        ["id", "name", "mail"],
        ["1", "kai", "kai@gmail"],
        ["2", "yama", "yama@ylab"],
        ["3", "ogacho", "ogacho@mafu"]
    ]

    last_input_data = [
        ["4", "jun", "jun@ibe"],
    ]
    
    #csv_handler.write_data(input_data, csv_path)
    #csv_handler.read_csv_data(csv_path)
    #csv_handler.add_data_csv(last_input_data, csv_path)
    netflix_csv = Path("../input/netflix_titles.csv")
    csv_handler.read_csv_data(netflix_csv)
