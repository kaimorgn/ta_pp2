#!/usr/bin/env python3
#
# dict_maker.py
#
# [概要]
#
#
#
#

from datetimejp import JDatetime
import pyinputplus as pyip

from datetime import datetime, timedelta
from logging import getLogger

# 専用のロガーを作成
logger = getLogger(__name__)


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
    [概要]
    申請書に記入する学生の氏名や年齢を取得して辞書型でまとめる関数．
    '''
    MAX_STUDENT = 7
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

