#!/usr/bin/env python3
#
# extract_japanese_video.py
#
# [概要]
# Kaggle で公開されていたオープンデータ
# ・Netflix Movies and TV Shows
# (https://www.kaggle.com/datasets/shivamb/netflix-shows)
# を拝借して分析するプログラム．
# 
# 具体的には，日本の映像作品だけを抽出して
# JSON ファイルに保存するアルゴリズムとなっている．
# CSV と JSON の操作はそれぞれ別ファイルで定義しており，
# 本ファイルではそれらの機能を継承して使っている．
#

from features.csv_io import CSVIO
from features.json_io import JSONIO
from features.setup_logging import setup_logging

from logging import getLogger
from pathlib import Path
import re

# 専用のロガーを作成
logger = getLogger(__name__)

# logging の設定を適用
logging_config = Path("./config/logging_config.yml")
setup_logging(logging_config)


class ExtractJapaneseVideo(CSVIO, JSONIO):
    def __init__(self):
        super().__init__()
        self.target_country_pattern = re.compile(r"Japan")

    def run_analysis(self, input_csv_path, output_json_path):
        '''
        [概要]
        CSV ファイルからデータを取得して分析するメソッド
        データの細かな処理は
        ・_get_column_indices()
        ・_extract_target_data()
        が担っている
        '''
        csv_data = self.read_csv_data(input_csv_path)

        if not csv_data:
            logger.warning(
                f"{input_csv_path} の中身が空でした: {len(csv_data)}"
            )
            raise ValueError

        header = csv_data[0]
        body = csv_data[1:]

        try:
            logger.debug(f"> データの分析を開始")
            indices = self._get_column_indices(header)
            target_data = self._extract_target_data(body, indices)
            self.write_json_data(target_data, output_json_path)
            logger.info(f">> 分析結果: {len(target_data)} 件")

            return True

        except Exception as e:
            logger.error(
                f"データ分析中にエラーが発生: {e}"
            )
            raise e

    def _get_column_indices(self, header):
        '''
        [概要]
        ヘッダーリストから必要なカラムのインデックス(位置)を
        特定して辞書で返すメソッド
        '''
        assert header, "ヘッダーリストを渡して"
        
        try:
            indices = {
                "country": header.index("country"),
                "title": header.index("title"),
                "type": header.index("type"),
                "duration": header.index("duration")
            }

            return indices

        except Exception as e:
            logger.error(
                f"カラムインデックス特定時にエラーが発生: {e}"
            )
            raise e

    def _extract_target_data(self, body, indices):
        '''
        [概要]
        データ本体を参照して，条件(Japaneseを含む)に合うデータを
        整形してリストで返す
        '''
        assert body, "body(データ本体)を渡して"
        assert indices, "カラムのインデックスを渡して"

        results = []

        idx_country = indices["country"]
        idx_title = indices["title"]
        idx_type = indices["type"]
        idx_duration = indices["duration"]

        try:
            for row in body:
                if len(row) <= idx_country:
                    continue

                country_value = row[idx_country]
                if self.target_country_pattern.search(country_value):
                    item = {
                        "title": row[idx_title],
                        "type": row[idx_type],
                        "duration": row[idx_duration]
                    }
                    results.append(item)

            return results

        except Exception as e:
            logger.error(
                f"データ整形中にエラーが発生: {e}"
            )
            raise e
    

if __name__ == "__main__":
    input_csv_path = Path("./input/netflix_titles.csv")
    output_dir_path = Path("./output")

    if output_dir_path.exists() == False:
        output_dir_path.mkdir(exist_ok=True)
        logger.debug(
            f"{output_dir_path} を新規作成"
        )

    output_json_path = output_dir_path / "output.json"
    extractor = ExtractJapaneseVideo()
    extractor.run_analysis(input_csv_path, output_json_path)
