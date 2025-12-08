#!/usr/bin/env python3
#
# txt_reader.py
#
# [概要]
# .txtファイルから文字列を
# 取得して，カテゴリ別のリストに
# まとめて返すプログラム．
#

from logging import getLogger
from pathlib import Path

# 専用のロガーを作成
logger = getLogger(__name__)


def read_txt(txt_path, total_day):
    assert isinstance(txt_path, Path), "txt_pathはPathオブジェクト想定"
    assert isinstance(total_day, int), "total_dayは整数型想定"

    try:
        logger.info(f"{txt_path}からテキストデータを取得します")
        with open(txt_path, "r", encoding="utf-8") as tf:
            full_text = tf.read()

        sections = [
            section.strip() for section in full_text.split(
                "======"
            ) if section.strip()
        ]
        logger.info(f"{txt_path}からテキストデータを取得しました")

        expected_count = total_day * 2
        if len(sections) != expected_count:
            raise ValueError(
                "データが足りません"
            )

        logger.info("sectionsリストの中身を分配します")
        content_list = sections[::2]
        comment_list = sections[1::2]
        logger.info("sectionsリストの中身を分配しました")

        return content_list, comment_list

    except Exception as e:
        logger.error(
            f"テキスト取得時 or リストの分配時にエラーが発生しました: {e}"
        )
        raise e


if __name__ == "__main__":
    from setup_logging import setup_logging
    from pathlib import Path

    setup_logging()

    txt_path = Path("../input/report_data_3day.txt")
    total_day = 3
    content_list, comment_list = read_txt(txt_path, total_day)
    logger.debug(
        f"実習内容: {content_list}"
    )
    logger.debug(
        f"コメント: {comment_list}"
    )
    
