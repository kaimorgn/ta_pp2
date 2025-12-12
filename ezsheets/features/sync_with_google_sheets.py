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
        client_secret.jsonを使ってトークンを発行するためのメソッド．
        インスタンス生成と同時に実行される．
        '''
        assert secret_file, "無効なclient_secret.jsonのパスが渡されました"
        assert isinstance(secret_file, Path), "Pathオブジェクトを渡して"

        try:
            logger.debug(">>> 新しいトークンを発行します")
            ezsheets.init()
            logger.debug(">>> 新しいトークンの発行に成功しました")

        except Exception as e:
            logger.error(
                f"新しいトークンの発行時にエラーが発生しました: {e}"
            )
            raise e


if __name__ == "__main__":
    from setup_logging import setup_logging
    import os

    os.chdir("../config/")
    logging_config = Path("./logging_config.yml")
    setup_logging(logging_config)

    secret_file = Path("./credentials-sheets.json")
    SyncWithGoogleSheets(secret_file)
