#!/usr/bin/env python3
#
# sync_with_google_calendar.py
#
# [概要]
# Google Calendar API と連携して
# 特定の日時の予定(イベント)を取得したり
# 追加したりするプログラム．
# 
# まずは手作業でイベントを追加して
# そのイベント情報を取得する．
# その後，Python を使って
# 講義最終回の日時に最終発表の予定を
# 追加する．
#

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from logging import getLogger
from pathlib import Path
import os
import pickle

# 専用のロガーを作成
logger = getLogger(__name__)


class SyncWithGoogleCalendar:
    def __init__(self, token_path, json_path, calendar_id="primary"):
        self.SCOPES = [
            "https://www.googleapis.com/auth/calendar"
        ]

        creds = self._creds_refresh(
            token_path, json_path
        )
        self.service = build(
            "calendar",
            "v3",
            credentials=creds,
        )

        self.calendar_id = calendar_id

    def _creds_refresh(self, token_path, json_path):
        '''
        [概要]
        コンストラクタと同時に実行してトークンをリフレッシュするメソッド
        '''
        assert token_path, "token_pathを渡して"
        assert json_path, "json_pathを渡して"
        assert isinstance(token_path, Path), "tokenはPathオブジェクト想定"
        assert isinstance(json_path, Path), "jsonはPathオブジェクト想定"

        creds = None
        
        try:
            logger.debug("> 認証情報オブジェクト(creds)を取得")
            if token_path.exists() == True:
                with open(token_path, "rb") as token:
                    creds = pickle.load(token)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Requests())

                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        json_path,
                        self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)

                with open(token_path, "wb") as token:
                    pickle.dump(creds, token)

            logger.info(">> 認証情報オブジェクト(creds)を取得完了")

            return creds

        except Exception as e:
            logger.error(
                f"認証情報オブジェクト取得時にエラーが発生: {e}"
            )
            raise e
        
    def load_event_id(self, event_name, start_iso, end_iso):
        '''
        [概要]
        自分のカレンダーから特定のイベント情報を取得するメソッド
        ＊ 処理を切り分ければリストでまとめて取得するメソッドに発展できる
        '''
        if not self.service:
            logger.error(">>>> サービスが初期化されていないため処理を中止")

        try:
            event_list = self.service.events().list(
                calendarId=self.calendar_id,
                q=event_name,
                timeMin=start_iso,
                timeMax=end_iso,
                maxResults=5,
                singleEvents=True,
                orderBy="startTime",
            ).execute()
            events = event_list.get("items", [])

            if not events:
                logger.info(
                    f">>>> 検索条件と一致する予定は見つからない: {len(events)}"
                )

            for event in events:
                if event.get("summary") == event_name:
                    event_id = event["id"]
                    logger.debug(
                        f"> 検索条件と一致する予定が見つかった: {event_id}"
                    )
                    return event_id

            logger.debug(
                "名前が完全に一致するイベントは見つからない"
            )
            return None

        except TypeError as e:
            logger.error(
                f"APIリクエスト中にエラーが発生: {e}"
            )
            raise e

        except Exception as e:
            logger.error(
                f"予定検索時にエラーが発生: {e}"
            )
            raise e

    def add_event(self, summary, location, start_iso, end_iso, ):
        '''
        [概要]
        自分のカレンダーに予定を追加するメソッド
        '''
        event = {
            "summary": summary,
            "location": location,
            "description": "",
            "start": {
                "dateTime": start_iso,
                "timeZone": "Asia/Tokyo",
            },
            "end": {
                "dateTime": end_iso,
                "timeZone": "Asia/Tokyo",
            },
        }

        try:
            self.service.events().insert(
                calendarId=self.calendar_id,
                body=event,
            ).execute()

            logger.debug(
                f"> カレンダーにイベントを追加しました: {event}"
            )
            return True

        except Exception as e:
            logger.error(
                f">>>> イベント追加時にエラーが発生: {e}"
            )
            raise e


if __name__ == "__main__":
    from datetime_manager import DateTimeManager
    from setup_logging import setup_logging

    logging_config = Path("../config/logging_config.yml")
    setup_logging(logging_config)

    token_path = Path("../config/token.pickle")
    json_path = Path("../config/client_secret.json")
    calendar = SyncWithGoogleCalendar(token_path, json_path)
    datetime_manager = DateTimeManager()
    start_date = "2025年12月29日"
    end_date = "2025年12月31日"

    event = "test"
    start_moment = "00:00"
    end_moment = "23:50"
    start_iso = datetime_manager.convert_isoformat(
        start_date, start_moment
    )
    end_iso = datetime_manager.convert_isoformat(
        end_date, end_moment
    ) 
    calendar.load_event_id(event, start_iso, end_iso)

    ###
    summary = "[最終発表会]Python プログラミング2"
    location = "G1-205"
    insert_date = "2026年1月27日"
    insert_start_moment = "14:30"
    insert_end_moment = "16:00"
    insert_start_iso = datetime_manager.convert_isoformat(
        insert_date, insert_start_moment
    )
    insert_end_iso = datetime_manager.convert_isoformat(
        insert_date, insert_end_moment
    )
    calendar.add_event(
        summary, location, insert_start_iso, insert_end_iso
    )
