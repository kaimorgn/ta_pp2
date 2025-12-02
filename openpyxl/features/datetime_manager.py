#!/usr/bin/env python3
#
# datetime_manager.py
#
# [概要]
# 実習報告書の「実習期間」に
# 書き込む和暦込みの日付データを
# 作成するためのプログラム．
#

from datetimejp import JDatetime

from datetime import datetime, timedelta
from logging import getLogger

# 専用のロガーを作成
logger = getLogger(__name__)


def make_internship_period(base_date, days_delta):
    '''
    [概要]
    base_dateからdays_delta分遡った日付を算出して，
    「令和W年MM月DD日(w)〜MM月DD日(w)」の文字列を返す関数．
    '''
    assert isinstance(base_date, JDatetime), "base_dateはJDatetime型想定"
    assert isinstance(days_delta, int), "days_deltaは整数型にして"

    try:
        logger.info("実習期間文字列を作成します")
        delta_days_ago = base_date - timedelta(days=days_delta)

        base_period = base_date.strftime("%m月%d日(%#a)")
        delta_days_period = delta_days_ago.strftime("%g%-e年%m月%d日(%#a)")
        
        internship_period = f"{delta_days_period}〜{base_period}"

        logger.info(f"実習期間文字列を作成しました: {internship_period}")
        logger.debug(
            f"作成した日付データ: {internship_period}"
        )
        return internship_period

    except Exception as e:
        logger.error(
            f"実習期間の日付データ作成中にエラー発生: {e}"
        )
        raise e


if __name__ == "__main__":
    from setup_logging import setup_logging

    setup_logging()

    base_date = JDatetime.today()
    days_delta = 10
    period = make_internship_period(base_date, days_delta)
    logger.debug(
        f"出力チェック: {period}"
    )
