#!/usr/bin/env python3
#
# schedule_manager.py
#
# [概要]
# features/ディレクトリ下に配置した
# DateTimeMangerとSyncWithGoogleCalendarを呼び出し
# カレンダーの情報を取得したり書き込んだりするプログラム
#

from features.datetime_manager import DateTimeManager
from features.setup_logging import setup_logging
from features.sync_with_google_calendar import SyncWithGoogleCalendar

from logging import getLogger
from pathlib import Path

# 専用のロガーを作成
logger = getLogger(__name__)

logging_config = Path("./config/logging_config.yml")
setup_logging(logging_config)


class ScheduleManager:
    def __init__(self, token_path, json_path):
        self.datetime = DateTimeManager()
        self.calendar = SyncWithGoogleCalendar(
            token_path, json_path
        )

    def search_event_id(
            self, event_name, search_start_date, search_start_moment,
            search_end_date, search_end_moment):
        '''
        [概要]
        日付データと時間データを受け取り，ISO形式データに変換した後
        Google カレンダーに指定のイベントがあるか検索するメソッド
        一致するイベントがあった場合，イベントIDを返す
        '''
        try:
            search_start_iso = self.datetime.convert_isoformat(
                search_start_date, search_start_moment
            )
            search_end_iso = self.datetime.convert_isoformat(
                search_end_date, search_end_moment
            )
            self.calendar.load_event_id(
                event_name, search_start_iso, search_end_iso
            )
            return True

        except Exception as e:
            logger.error(
                f"イベントID検索時にエラー発生: {e}"
            )
            raise e

    def add_event_to_calendar(
            self, event_date, event_start_moment, event_end_moment,
            summary, location):
        '''
        [概要]
        日付データと時間データを受け取り，ISO形式データに変換した後
        Google カレンダーにイベントを書き込む(追加)するメソッド
        '''
        try:
            event_start_iso = self.datetime.convert_isoformat(
                event_date, event_start_moment
            )
            event_end_iso = self.datetime.convert_isoformat(
                event_date, event_end_moment
            )
            self.calendar.add_event(
                summary, location, event_start_iso, event_end_iso
            )

            return True

        except Exception as e:
            logger.error(
                f"イベント追加時にエラー発生: {e}"
            )
            raise e


if __name__ == "__main__":
    token_path = Path("./config/token.pickle")
    json_path = Path("./config/client_secret.json")
    manager = ScheduleManager(token_path, json_path)

    search_title = "test"
    search_date = "2026年1月20日"
    search_start_moment = "00:00"
    search_end_moment = "23:59"
    manager.search_event_id(
        search_title, search_date, search_start_moment,
        search_date, search_end_moment
    )

    ###
    summary = "[最終発表会]Python プログラミング2"
    location = "G1-205"
    event_date = "2026年1月27日"
    event_start_moment = "14:30"
    event_end_moment = "16:00"
    manager.add_event_to_calendar(
        event_date, event_start_moment, event_end_moment,
        summary, location
    )
