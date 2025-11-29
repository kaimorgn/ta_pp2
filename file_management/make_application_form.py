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

from datetime import datetime, timedelta
from ligging import getLogger
from pathlib import Path
import shutil
import zipfile

# 専用のロガーを作成
logger = getLogger(__name__)


def copy_template(input_docx, output_docx):
    '''
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


def make_date_dict(base_date):
    '''
    '''
    
