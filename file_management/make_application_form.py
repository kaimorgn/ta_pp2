#!/usr/bin/env python3
#
# make_application_form.py
#
# [概要]
#
#
#
#
#
#
#
#

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from datetimejp import JDatetime
import pyinputplus as pyip

from datetime import datetime, timedelta
from logging import getLogger
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


def make_date_dict(base_date):
    '''
    [概要]
    申請書に記入する日付情報を辞書に内包して返す関数．
    '''
    assert isinstance(base_date, JDatetime), "base_dateはJDatetime型想定"

    try:
        tomorrow = base_date + timedelta(days=1)
        one_week_later = base_date + timedelta(weeks=1)
        logger.info(f"{base_date}をベースにした日付関連の辞書を返します")
        
        return {
            "{start_year}": f"{tomorrow.year}",
            "{start_month}": f"{tomorrow.month}",
            "{start_day}": f"{tomorrow.day}",
            "{start_wareki}": f"{base_date.strftime('%-e')}",
            "{end_month}": f"{one_week_later.month}",
            "{end_day}": f"{one_week_later.day}",
            "{end_wareki}": f"{one_week_later.strftime('%-e')}"
        }

    except Exception as e:
        logger.error(
            f"日付関連の辞書を作成時にエラーが発生しました: {e}"
        )
        raise e


def make_student_dict():
    '''
    '''
    MAX_STUDENT = 7
    logger.info("使用する学生情報を取得します")
    total_student = pyip.inputStr(
        "使用する学生の合計人数を教えてください(上限 7 人): "
    )
    tell_number = pyip.inputStr(
        "代表者の電話番号を入力してください: \n",
    )
    use_room = pyip.inputMenu(
        (
            "G1-205",
            "D603"
        ),
        prompt="使用予定の教室を選択してください: \n",
        numbered=True
    )
    student_dict = {
        "{total_student}": total_student,
        "{use_room}": use_room,
        "{tell_number}": tell_number
    }
    
    try:
        for i in range(MAX_STUDENT):
            if i < int(total_student):
                student_id = pyip.inputStr(
                    f"{i+1}人目の学籍番号を入力してください:"
                )
                student_name = pyip.inputStr(
                    f"{i+1}人目の氏名を入力してください:"
                )
                student_age = pyip.inputStr(
                    f"{i+1}人目の年齢を入力してください:"
                )
                student_gender = pyip.inputMenu(
                    (
                        "男",
                        "女"
                    ),
                    prompt=f"{i+1}人目の性別を選択してください: \n",
                    numbered=True
                )

            else:
                student_id = ""
                student_name = ""
                student_age = ""
                student_gender = ""
                
                
            student_dict[f"{{student_id_{i+1}}}"] = student_id
            student_dict[f"{{student_name_{i+1}}}"] = student_name
            student_dict[f"{{age_{i+1}}}"] = student_age
            student_dict[f"{{gender_{i+1}}}"] = student_gender

        logger.info("使用する学生の情報を辞書型で定義できました")
            
        return student_dict

    except Exception as e:
        logger.error(
            f"学生情報入力中にエラーが発生しました: {e}"
        )
        raise e


def gender_dict(student_dict):
    '''
    [概要]
    男女別の合計人数を算出してstudent_dictに追加する関数
    '''
    assert isinstance(student_dict, dict), "student_dictは辞書型想定です"

    males = 0
    females = 0
    try:
        logger.info("男女別の合計人数を算出します")
        for key, value in student_dict.items():
            if "gender" in key:
                if "男" in value:
                    males += 1

                elif "女" in value:
                    females += 1

        student_dict["{total_males}"] = str(males)
        student_dict["{total_females}"] = str(females)

        logger.info("男女別の合計人数をstudent_dictに追加しました")

        return True

    except Exception as e:
        logger.error(
            f"男女それぞれの合計人数算出中にエラーが発生しました: {e}"
        )
        raise e


def _clear_paragraph(cell):
    '''
    [概要]
    '''
    try:
        for para in cell.paragraphs:
            p_element = para._element
            p_element.getparent().remove(p_element)

    except Exception as e:
        logger.error(
            f"指定セル内のパラグラフを削除する際にエラーが発生しました: {e}"
        )
        raise e


def _edit_paragraph(docx_obj, replace_dict):
    '''
    '''
    assert isinstance(replace_dict, dict), "replace_dictは辞書型想定です"

    try:
        for para in docx_obj.paragraphs:
            original_text = para.text
            new_text = original_text
            replaced = False
            
            for key, value in replace_dict.items():
                if key in new_text:
                    new_text = new_text.replace(key, value)
                    replaced = True

            if replaced:
                para.clear()
                para.add_run(new_text)

        return True

    except Exception as e:
        logger.error(
            f"パラグラフ編集中にエラーが発生しました: {e}"
        )
        raise e


def edit_table_cell(docx_obj, replace_dict):
    '''
    '''
    assert isinstance(replace_dict, dict), "replace_dictは辞書型想定です"
    try:
        for table in docx_obj.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        for run in para.runs:
                            for key, value in replace_dict.items():
                                if key in run.text:
                                    run.text = run.text.replace(
                                        key, str(value)
                                    )

        return True

    except Exception as e:
        logger.error(
            f"テーブル(表)の編集中にエラーが発生しました: {e}"
        )
        raise e


def edit_docx(docx_path_obj, base_date):
    '''
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
    

if __name__ == "__main__":
    from features.setup_logging import setup_logging
    from pathlib import Path

    # loggingの設定を反映
    setup_logging()

    output_dir = Path("output")
    if output_dir.exists() == False:
        output_dir.mkdir(exist_ok=True)
        logger.debug(f"{output_dir.name}を新規作成しました")

    else:
        logger.debug(f"{output_dir.name}は作成済みです")
        
    today = JDatetime.now()
    input_docx = Path("./input/mse_facility_use_application_form.docx")
    output_docx = output_dir / f"{today.strftime('%Y%m%d')}_application_form.docx"
    copy_template(input_docx, output_docx)

    edit_docx(output_docx, today)
