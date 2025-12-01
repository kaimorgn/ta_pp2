#!/usr/bin/env python3
#
# make_application_form.py
#
# [概要]
# shutilモジュールを使って複製した
# テンプレート(mse_facility_use_application_form.docx)を
# 第1週目で学習した docx モジュールを駆使して編集し，保存する．
# その後，保存先(output)を参照してZIPファイルを
# 作成するプログラム．
#

from docx import Document
from datetimejp import JDatetime
import pyinputplus as pyip

from features.docx_editor import _clear_paragraph, _edit_paragraph, edit_table_cell
from features.dict_maker import make_date_dict, make_student_dict, gender_dict

from logging import getLogger
from pathlib import Path
import shutil
import zipfile

# 専用のロガーを作成
logger = getLogger(__name__)


def copy_template(input_docx, output_docx):
    '''
    [概要]
    shutilモジュールを使って既存ファイルを複製する関数．
    '''
    assert isinstance(input_docx, Path), "input_docxはPathオブジェクト想定"
    assert isinstance(output_docx, Path), "output_docxはPathオブジェクト想定"

    try:
        logger.info(f"{input_docx}を複製します")
        shutil.copy(
            input_docx, output_docx
        )
        logger.info(f"複製が完了しました: {output_docx}")

        return True

    except FileNotFoundError as e:
        logger.error(
            f"{input_docx}が見つかりません: {e}"
        )
        raise e

    except Exception as e:
        logger.error(
            f"ファイルの複製中に予期せぬエラーが発生しました: {e}"
        )
        raise e


def edit_docx(docx_path_obj, base_date):
    '''
    [概要]
    ドキュメントファイル編集関連の関数を呼び出して実行する役割．
    '''
    docx_obj = Document(docx_path_obj)
    date_dict = make_date_dict(base_date)
    student_dict = make_student_dict()
    gender_dict(student_dict)
    
    replace_dict = date_dict | student_dict
    logger.debug(replace_dict)
    try:
        logger.info("ドキュメントを編集します")
        _edit_paragraph(docx_obj, replace_dict)
        edit_table_cell(docx_obj, replace_dict)
        docx_obj.save(docx_path_obj)

        logger.info("ドキュメントを編集して保存が完了しました")

        return True

    except Exception as e:
        logger.error(
            f"ドキュメント編集中にエラーが発生しました: {e}"
        )
        raise e


def save_snapshot(snapshot_name, data_dir):
    '''
    [概要]
    outputディレクトリを参照してZIPファイルを作成する関数．
    '''
    assert isinstance(snapshot_name, Path), "snapshot_nameはPathオブジェクト"
    assert isinstance(data_dir, Path), "data_dirはPathオブジェクト"

    try:
        logger.info("スナップショットを作成します")
        items = list(data_dir.iterdir())
        logger.info(f"{len(items)}個のデータをスナップショットに保存します")
        with zipfile.ZipFile(snapshot_name, "w") as zf:
            for i, item in enumerate(items):
                zf.write(item)
                logger.info(f"{i+1}個目のデータを追加しました")

        logger.info("スナップショットを作成しました")
        return True

    except Exception as e:
        logger.error(
            f"スナップショット作成中にエラーが発生しました: {e}"
        )
        raise e


def main():    
    output_dir = Path("output")
    if output_dir.exists() == False:
        output_dir.mkdir(exist_ok=True)
        logger.debug(f"{output_dir.name}を新規作成しました")

    else:
        logger.debug(f"{output_dir.name}は作成済みです")

    snapshot_dir = Path("snapshot")
    if snapshot_dir.exists() == False:
        snapshot_dir.mkdir(exist_ok=True)
        logger.debug(f"{snapshot_dir.name}を新規作成しました")

    else:
        logger.debug(f"{snapshot_dir.name}は作成済みです")
        
    today = JDatetime.now()
    input_docx = Path("./input/mse_facility_use_application_form.docx")
    output_docx = output_dir / f"{today.strftime('%Y%m%d')}_application_form.docx"
    
    snapshot_name = snapshot_dir / f"{today.strftime('%Y%m%d')}_snapshot.zip"
    copy_template(input_docx, output_docx)
    edit_docx(output_docx, today)
    save_snapshot(snapshot_name, output_dir)
    

if __name__ == "__main__":
    from features.setup_logging import setup_logging

    # loggingの設定を反映
    setup_logging()
    # 一括実行
    main()
    
