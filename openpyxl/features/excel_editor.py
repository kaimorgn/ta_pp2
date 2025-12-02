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

from logging import getLogger

# 専用のロガーを作成
logger = getLogger(__name__)


def load_worksheet(xlsx_path, sheet_name):
    '''
    '''
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
    '''
    '''
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


def save_workbook(wb_obj, save_path):
    '''
    '''
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
    from pathlib import Path

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
