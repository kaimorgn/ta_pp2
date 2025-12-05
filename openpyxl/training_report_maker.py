#!/usr/bin/env python3
#
# training_report_maker.py
#
# [概要]
# 秋県大のキャリア情報センターが配布している
# インターンシップ実習報告書（1~3日間，5日間，10日間）を
# 自動編集して保存するプログラム．
# 
# なお，openpyxlを使った操作は
# features/excel_editor.py を参照すること．
#

from datetimejp import JDatetime

from features.copy_template import copy_template
from features.datetime_manager import make_internship_period
from features.excel_editor import load_worksheet, edit_cell, save_workbook, insert_internship_info
from features.make_snapshot import make_snapshot

from logging import getLogger
from pathlib import Path

# 専用のロガーを作成
logger = getLogger(__name__)


def make_three_day_report(save_dir):
    '''
    '''
    assert isinstance(save_dir, Path), "save_dirはPathオブジェクトにして"

    three_day_report_path = Path(
        "input/internship_training_report_3_day_format.xlsx"
    )
    three_day_data = Path(
        "input/report_data_3day.txt"
    )
    save_path = save_dir / "internship_training_report_3day.xlsx"

    try:
        wb_obj, ws = load_worksheet(three_day_report_path, "3day")
        
        
        base_date = JDatetime.today()
        days_delta = 3
        e_column_list = [
            "経営システム工学科",
            "XXX株式会社",
            "由利本荘市部",
            make_internship_period(base_date, days_delta),
        ]

        w_column_list = [
            "吉田 快",
            "土谷字海老ノ口84-4"
        ]
        insert_internship_info(
            ws, base_date, days_delta, e_column_list, w_column_list
        )
        
        save_workbook(wb_obj, save_path)
        
        return True

    except Exception as e:
        logger.error(
            f"実習報告書(3日間)の編集中にエラーが発生しました: {e}"
        )
        raise e


if __name__ == "__main__":
    from features.setup_logging import setup_logging

    setup_logging()

    save_dir = Path("output")
    if save_dir.exists() == False:
        save_dir.mkdir(exist_ok=True)
        logger.debug(f"{save_dir}を新規作成しました")

    else:
        logger.debug(f"{save_dir}は作成済みです")

    make_three_day_report(save_dir)
