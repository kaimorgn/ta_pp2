#!/usr/bin/env python3
# 
# datetime_manager.py
#
# [概要]
# 標準モジュールの datetime モジュールをはじめ
# dateutil モジュールや datetimeJP を組み合わせて
# 日時情報を操作するプログラム．
# データ型の変換や簡単な日付算出も定義している．
#

from datetimejp import JDatetime
from dateutil.relativedelta import relativedelta

from datetime import datetime, timedelta, timezone
from logging import getLogger
from zoneinfo import ZoneInfo

# 専用のロガーを作成
logger = getLogger(__name__)


class DateTimeManager:
    def __init__(self, tz="Asia/Tokyo"):
        self.today = JDatetime.today()
        self.tz = ZoneInfo(tz)

    def convert_dtformat(self, input_date):
        '''
        [概要]
        文字列型の日付を datetime 型に変換するメソッド
        '''
        assert input_date, "変換する日付データを渡して"
        assert isinstance(input_date, str), "変換前の日付データは文字列型"
        
        date_format = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%Y年%m月%d日"
        ]
        
        for fmt in date_format:
            try:
                converted_date = JDatetime.strptime(
                    input_date, fmt
                )
                return converted_date
                break

            except ValueError:
                logger.debug("datetime 型へ変換する前の文字列型チェック中...")
                continue

    def add_time(self, input_date, moment):
        '''
        [概要]
        JDatetime 型の日付データに時間データを追加するメソッド
        '''
        assert input_date, "日付データを渡して"
        assert isinstance(input_date, JDatetime), "日付データは JDatetime 型"
        assert moment, "追加する時間データを渡して"
        assert isinstance(moment, str), "追加する時間は文字列型にして"

        try:
            parts = list(
                map(
                    int, moment.strip().split(":")
                )
            )
            
            if len(parts) == 2:
                hour, minute = parts
                second = 0

            elif len(parts) == 3:
                hour, minute, second = parts

            else:
                raise ValueError(
                    f"追加する時間データの形式を確認して: {moment}"
                )

            return input_date.replace(
                hour=hour, minute=minute, second=second
            )

        except Exception as e:
            logger.error(
                f"時間データを追加する際にエラー発生: {e}"
            )
            raise e

    def convert_wareki(self, input_date, option="%g%-e"):
        '''
        [概要]
        JDatetime 型の日付データから"和暦"を取得するメソッド
        取得した和暦は文字列型で返す
        '''
        assert input_date, "日付データを渡して"
        assert isinstance(input_date, JDatetime), "日付データは JDatetime 型"

        try:
            logger.debug("> 取得した和暦を返す")
            return input_date.strftime(option)

        except Exception as e:
            logger.error(
                f"和暦取得時にエラーが発生: {e}"
            )
            raise e

    def convert_week_jp(self, input_date):
        '''
        [概要]
        入力された日付データを参照して日本表記の曜日を取得するメソッド
        '''
        assert input_date, "日付データを渡して"
        assert isinstance(input_date, JDatetime), "日付データは JDatetime 型"

        try:
            logger.debug("> 取得した日本表記の曜日を返す")
            return input_date.strftime("%#a")

        except Exception as e:
            logger.error(
                f"日本表記の曜日取得時にエラーが発生: {e}"
            )
            raise e

    def calculation_month_range(self, input_date):
        '''
        [概要]
        入力された日付データを起点に月初日と月末日を算出するメソッド
        '''
        assert input_date, "日付データを渡して"
        assert isinstance(input_date, JDatetime), "日付データは JDatetime 型"

        try:
            first_date = input_date.replace(day=1)
            last_date = (
                first_date + relativedelta(months=1)
            ).replace(day=1) - timedelta(days=1)

            logger.debug(
                f"> {input_date.strftime('%m')} 月の月初日と月末日を算出"
            )

            return first_date, last_date

        except Exception as e:
            logger.error(
                f"月初日と月末日の算出時にエラー発生: {e}"
            )
            raise e

    def calculation_week_range(self, input_date):
        '''
        [概要]
        入力された日付データを起点に週初め日と週末日を算出するメソッド
        '''
        assert input_date, "日付データを渡して"
        assert isinstance(input_date, JDatetime), "日付データは JDatetime 型"

        try:
            days_to_sunday = (input_date.weekday() + 1) % 7
            sunday = input_date - timedelta(days=days_to_sunday)
            saturday = sunday + timedelta(days=6)

            logger.debug(
                f"> 入力された日付データの週初めと週末日を算出した"
            )
            return sunday, saturday

        except Exception as e:
            logger.error(
                f"週初めと週末日算出時にエラー発生: {e}"
            )
            raise e

    def convert_isoformat(self, input_date, moment):
        '''
        [概要]
        外部サービスと連携する際は ISO 形式の時間表記に修正する必要があるため
        変換する役割を担うメソッド
        外部サービスの代表的な例は "Google Calendar"
        '''
        try:
            date = self.add_time(input_date, moment)
            if date.tzinfo is None:
                date = date.replace(tzinfo=self.tz)

            logger.debug(f"ISO 形式への変換に成功した")
            return date.isoformat()

        except Exception as e:
            logger.error(
                f"ISO 形式への変換時にエラーが発生: {e}"
            )
            raise e


if __name__ == "__main__":
    from setup_logging import setup_logging
    from pathlib import Path

    logging_config = Path("../config/logging_config.yml")
    setup_logging(logging_config)

    datetime_manager = DateTimeManager()

    input_date = "2025年12月25日"
    converted_date = datetime_manager.convert_dtformat(input_date)
    logger.debug(f"> datetime型への変換結果: {converted_date}")

    moment = "21:00"
    converted_datetime = datetime_manager.add_time(converted_date, moment)
    logger.debug(
        f"> 時間データの追加結果{converted_datetime}"
    )

    converted_iso_datetime = datetime_manager.convert_isoformat(
        converted_datetime, moment
    )
    logger.debug(
        f"> ISO 形式に変換した結果: {converted_iso_datetime}"
    )
