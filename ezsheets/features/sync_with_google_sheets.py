#!/usr/bin/env python3
#
# sync_with_google_sheets.py
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
#

import ezsheets

from logging import getLogger
from pathlib import Path

# 専用のロガーを作成
logger = getLogger(__name__)


class SyncWithGoogleSheets:
    def __init__(self, secret_file):
        self._refresh_token(secret_file)

    def _refresh_token(self, secret_file):
        '''
        [概要]
        client_secret_*.jsonを使ってトークンを発行するためのメソッド．
        インスタンス生成と同時に実行される．
        '''
        assert secret_file, "client_secret.jsonのパスを確認してください"
        assert isinstance(secret_file, Path), "Pathオブジェクトにしてください"

        try:
            logger.debug("> 新しいトークンを発行します")
            ezsheets.init()
            logger.debug("> 新しいトークンの発行に成功しました")
            logger.info(">> 認証に成功しました")

        except Exception as e:
            logger.error(
                f"新しいトークンの発行時にエラーが発生しました: {e}"
            )
            raise e

    def _make_sheets_dict(self):
        '''
        '''
        try:
            logger.debug("> 複数のスプレッドシートを取得します")
            self.sheets_dict = ezsheets.listSpreadsheets()
            if not self.sheets_dict:
                logger.warning(
                    f">>> シートを取得できなかった: {len(self.sheets_dict)}"
                )
                raise

            logger.debug("> 複数のスプレッドシートを取得しました")
            logger.info(
                f">> {len(self.sheets_dict)}個のスプレッドシートを取得しました"
            )
            
            logger.debug("> コンソール上に出力します")
            for sheet_id, title in self.sheets_dict.items():
                logger.debug(
                    f"シート名: {title}, \nシートID: {sheet_id}"
                )

            return True

        except Exception as e:
            logger.error(
                f"複数のスプレッドシート取得時にエラーが発生した: {e}"
            )
            raise e

    def read_sheets_by_title(self, title_name):
        '''
        '''
        assert title_name, "検索したいシート名を渡して"
        assert isinstance(title_name, str), "シート名は文字列型にして"
        
        self._make_sheets_dict()
        target_id = None
        try:
            logger.debug(f"> {title_name}と一致するシートを検索します")
            for sheet_id, title in self.sheets_dict.items():
                if title == title_name:
                    target_id = sheet_id
                    logger.debug(
                        f"> {title_name}と一致するシートが見つかった"
                    )
                    break

            if target_id is None:
                logger.warning(
                    f">>> {title_name}と一致するシートが見つからなかった"
                )
                raise

            logger.info(
                f">> タイトル: {title_name} (ID: {target_id})を読み込む"
            )
            self.ss = ezsheets.Spreadsheet(target_id)

            return True

        except Exception as e:
            logger.error(
                f">>>> タイトルと一致するシート検索時にエラーが発生: {e}"
            )
            raise e


if __name__ == "__main__":
    from setup_logging import setup_logging
    import os

    os.chdir("../config/")
    logging_config = Path("./logging_config.yml")
    setup_logging(logging_config)

    secret_file = Path("./credentials-sheets.json")
    title_name  = "【駆けこみ寺】勤務表"
    SyncWithGoogleSheets(secret_file).read_sheets_by_title(title_name)
