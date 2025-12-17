#!/usr/bin/env python3
#
# sync_with_google_mail.py
#
# [概要]
# ezgmailモジュールを使って
# メールを送受信するプログラム
#

import ezgmail

from logging import getLogger
from pathlib import Path

# 専用のロガーを作成
logger = getLogger(__name__)


class SyncWithGoogleMail:
    def __init__(self):
        self._refresh_token()

    def _refresh_token(self):
        '''
        [概要]
        client_secret_*.jsonを使ってトークンを発行するためのメソッド．
        インスタンス生成と同時に実行される．
        '''
        try:
            logger.debug("> 新しいトークンを発行します")
            ezgmail.init()
            logger.debug("> 新しいトークンの発行に成功")
            logger.info(">> 認証に成功しました")

        except Exception as e:
            logger.error(
                f"新しいトークンの発行時にエラーが発生しました: {e}"
            )
            raise e


if __name__ == "__main__":
    sync_with_google_mail = SyncWithGoogleMail()
