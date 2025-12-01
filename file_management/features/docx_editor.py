#!/usr/bin/env python3
#
# docx_editor.py
#
#
#
#
#
#
#
#

from logging import getLogger

# 専用のロガーを作成
logger = getLogger(__name__)


def _clear_paragraph(cell):
    '''
    [概要]
    セル内のパラグラフを削除する関数．
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
    [概要]
    テキストを置換するための関数．
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
    [概要]
    テーブル（表）内のセルを参照して，
    編集対象のテキストを見つけて置換する関数．
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

