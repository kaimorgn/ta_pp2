#!/usr/bin/env python3
#
# excel_editor.py
#
# [概要]
# openpyxlを使って
# Workbookオブジェクトの作成，
# ワークシートの読み込み，
# セルの編集，
# ファイルの保存を定義した
# プログラム．
#

from openpyxl import load_workbook
from openpyxl.styles import Border, Side

from logging import getLogger
from pathlib import Path

# 専用のロガーを作成
logger = getLogger(__name__)


def load_worksheet(xlsx_path, sheet_name):
    assert isinstance(xlsx_path, Path), "ExcelファイルはPathオブジェクトで渡す"
    assert isinstance(sheet_name, str), "シート名は文字列型で渡して"

    try:
        logger.info(f"{xlsx_path}を使ってWorkbookオブジェクトを生成します")
        wb = load_workbook(xlsx_path)
        logger.debug(
            f"{xlsx_path}には{len(wb.sheetnames)}個のシートが存在します．"
        )
        
        logger.info(
            f"ワークシート: {sheet_name}を読み込みます..."
        )
        if not sheet_name in wb.sheetnames:
            logger.error(
                f"{xlsx_path}に{sheet_name}は存在しません．"
            )
            raise

        logger.info(
            f"ワークシート: {sheet_name}の読み込みに成功しました"
        )

        return wb, wb[sheet_name]

    except Exception as e:
        logger.error(
            f"ワークシート読み込み時に予期せぬエラーが発生しました: {e}"
        )
        raise e


def edit_cell(ws, cell_number, insert_data):
    assert isinstance(cell_number, str), "セル番号は文字列で指定して"

    try:
        logger.debug(
            f"{cell_number} に {insert_data} を書き込みます"
        )
        ws[cell_number] = insert_data
        logger.debug(
            f"{cell_number} に {insert_data} を書き込めました"
        )

        return True

    except Exception as e:
        logger.error(
            f"{cell_number} への書き込み中にエラーが発生しました: {e}"
        )
        raise e


def insert_internship_info(
        ws, base_date, days_delta, e_column_list, w_column_list
):
    assert isinstance(e_column_list, list), "e_column_listはリスト型にして"
    assert isinstance(w_column_list, list), "w_column_listはリスト型にして"

    try:
        logger.info("提出者情報を編集します")
        cell_number = "G1"
        edit_cell(ws, cell_number, "1")
        
        target_rows = range(3, 7)
        
        for row_num, text in zip(target_rows, e_column_list):
            cell_number = f"E{row_num}"
            edit_cell(ws, cell_number, text)

        target_rows = range(3, 5)
        for row_num, text in zip(target_rows, w_column_list):
            cell_number = f"W{row_num}"
            edit_cell(ws, cell_number, text)
        logger.info("提出者情報を編集しました")

    except Exception as e:
        logger.error(
            f"提出者情報の編集中にエラーが発生しました: {e}"
        )
        raise e


def insert_internship_schedule(ws, date_list, content_list, comment_list):
    assert isinstance(date_list, list), "date_listはリスト型"
    assert date_list, "date_listの中身が空です．直前の処理を確認してください"
    
    assert isinstance(content_list, list), "content_listはリスト型"
    assert content_list, "content_listの中身が空です"
    
    assert isinstance(comment_list, list), "comment_listはリスト型"
    assert comment_list, "comment_listの中身が空です"

    assert len(date_list) == len(content_list) == len(comment_list), \
        "リストの要素数が一致していません"
    
    target_rows = range(9, 9 + len(date_list))
    try:
        logger.info("実習スケジュールを記述します")
        logger.debug(">>> 最初に実習月日を記述します")
        for row_num, date in zip(target_rows, date_list):
            cell_number = f"A{row_num}"
            edit_cell(ws, cell_number, date)
            
        logger.debug(">>> 次に実習内容を記述します")
        for row_num, content in zip(target_rows, content_list):
            cell_number = f"E{row_num}"
            edit_cell(ws, cell_number, content)

        logger.debug(">>> 最後にコメントを記述します")
        for row_num, comment in zip(target_rows, comment_list):
            cell_number = f"Q{row_num}"
            edit_cell(ws, cell_number, comment)

        logger.info("実習スケジュールを記述しました")
        return True

    except Exception as e:
        logger.error(
            f"実習スケジュール編集中にエラーが発生しました: {e}"
        )
        raise e


def insert_internship_summary(ws, summary, num):
    assert summary, "summaryデータが空です"
    assert isinstance(summary, str), "summaryは文字列型想定です"

    try:
        logger.info("実習のまとめを記述します")
        cell_number = f"A{num}"
        edit_cell(ws, cell_number, summary)
        logger.info("実習のまとめを記述しました")

    except Exception as e:
        logger.error(
            f"実習のまとめを記述する際にエラーが発生しました: {e}"
        )
        raise e


def insert_message_for_junior(ws, message, num):
    assert message, "messageデータが空です"
    assert isinstance(message, str), "messageは文字列型想定です"

    try:
        logger.info("後輩に向けてのメッセージを記述します")
        cell_number = f"A{num}"
        edit_cell(ws, cell_number, message)
        logger.info("後輩に向けてのメッセージを記述しました")

    except Exception as e:
        logger.error(
            f"後輩に向けてのメッセージを記述する際にエラーが発生しました: {e}"
        )
        raise e


def save_workbook(wb_obj, save_path):
    assert isinstance(save_path, Path), "save_pathはPathオブジェクトにして"

    try:
        logger.debug(f"{save_path}を保存します")
        wb_obj.save(save_path)
        logger.info(f"{save_path}を保存しました")

        return True

    except Exception as e:
        logger.error(
            f"{save_path}の保存中にエラーが発生しました: {e}"
        )
        raise e


if __name__ == "__main__":
    from setup_logging import setup_logging

    setup_logging()

    xlsx_path = Path("../input/internship_training_report_3_day_format.xlsx")
    sheet_name = "3day"
    wb_obj, ws = load_worksheet(xlsx_path, sheet_name)

    cell_number = "E3"
    insert_data = "総合システム工学専攻"
    edit_cell(ws, cell_number, insert_data)

    save_dir = Path("../output")
    if save_dir.exists() == False:
        save_dir.mkdir(exist_ok=True)
        logger.debug(f"{save_dir}を新規作成しました")

    else:
        logger.debug(f"{save_dir}は作成済みです")

    save_path = save_dir / "sample_output.xlsx"
    save_workbook(wb_obj, save_path)
