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
import os

# 専用のロガーを作成
logger = getLogger(__name__)


class SyncWithGoogleMail:
    def __init__(self):
        self.mail = self._refresh_token()

    def _refresh_token(self):
        '''
        [概要]
        client_secret_*.jsonを使ってトークンを発行するためのメソッド．
        インスタンス生成と同時に実行される．
        '''
        try:
            logger.debug("> 新しいトークンを発行します")
            return ezgmail.init()

        except:
            os.remove("token.json")
            return ezgmail.init()

    def search_thread(self, search_target):
        '''
        [概要]
        search_target(件名)と一致するメールを取得するメソッド
        '''
        assert search_target, "検索対象を文字列型で渡す"
        assert isinstance(search_target, str), "検索対象は文字列型を期待する"

        try:
            logger.debug(f"> '{search_target}' と一致するメールを取得する")
            self.searched_threads = ezgmail.search(search_target)
            logger.debug(
                f"> {len(self.searched_threads)} 件のメールを取得した"
            )
            logger.debug(
                f"> メール本文を表示します: \n{self.searched_threads[0]}"
            )
            
            logger.info(
                f">> {len(self.searched_threads)} 件のメールを取得した"
            )

        except Exception as e:
            logger.error(
                f"メール検索時にエラーが発生した: {e}"
            )
            raise e

    def send_mail(self, subject, body, recipient=None):
        '''
        [概要]
        件名，本文，宛先を引数で指定してメールを送信するメソッド
        宛先が明示されない場合は自分のメールアドレスに送信する
        '''
        assert subject, "件名を渡して"
        assert isinstance(subject, str), "件名は文字列型で渡して"
        assert body, "本文を渡して"
        assert isinstance(body, str), "本文は文字列型で渡して"

        try:
            if not recipient:
                recipient = self.mail
                
            logger.debug(f"> '{recipient}' 宛にメールを送信します")
            ezgmail.send(
                recipient, subject, body
            )
            logger.debug(
                f"> '{recipient}' 宛にメールを送信した"
            )
            logger.info(
                f">> '{recipient}' 宛にメールを送信した"
            )

        except Exception as e:
            logger.error(
                f"メール送信時にエラーが発生した: {e}"
            )
            raise e
            

if __name__ == "__main__":
    from setup_logging import setup_logging

    # loggingの設定を適用
    logging_config = Path("../config/logging_config.yml")
    setup_logging(logging_config)

    os.chdir("../config")
    sync_with_google_mail = SyncWithGoogleMail()

    #search_target = "【連絡】１２月１１日の落雷による被害"
    #sync_with_google_mail.search_thread(search_target)

    subject = "25PP2_W12_サンプルメール"
    body = "これは Python の ezgmail で送信したメールです"
    sync_with_google_mail.send_mail(subject, body)
