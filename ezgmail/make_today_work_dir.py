#!/usr/bin/env python3
#
# make_today_work_dir.py
#
# [概要]
#
#
#
#

from features.setup_logging import setup_logging
from features.sync_with_google_mail import SyncWithGoogleMail

from datetime import datetime
from logging import getLogger
from pathlib import Path
import os
import zipfile

# 専用のロガーを作成
logger = getLogger(__name__)

# YAMLで定義したloggingの設定を反映
logging_config = Path("./config/logging_config.yml")
setup_logging(logging_config)


class MakeTodayWorkDir(SyncWithGoogleMail):
    def _make_dirs(self):
        '''
        '''
        self.dir_path = Path(
            f"../{datetime.today().strftime('%Y%m%d_work_dir')}"
        )
        try:
            if self.dir_path.exists() == False:
                self.dir_path.mkdir(exist_ok=True)
                logger.debug(f"> {self.dir_path.name}を新規作成しました")

            return True

        except Exception as e:
            logger.error(
                f"ディレクトリを新規作成時にエラーが発生: {e}"
            )
            raise e

    def execute_all(self):
        '''
        '''
        self._make_dirs()
        
        try:
            from_address = "has:attachment"
            logger.debug(
                f"> ディレクトリ '{self.dir_path}'にファイルをダウンロードする"
            )
            self.download_attached_files(
                from_address,
                download_path=self.dir_path
            )
            logger.debug(
                f"> ディレクトリ '{self.dir_path}'にファイルをダウンロードした"
            )

            logger.debug("> スナップショットを作成する")
            items = list(self.dir_path.iterdir())
            with zipfile.ZipFile("../snapshot.zip", "w") as zf:
                for i, item in enumerate(items):
                    zf.write(item)
            logger.debug("> スナップショットを作成した")

        except Exception as e:
            logger.error(
                f"'{self.dir_path}' にダウンロードする際にエラー発生: {e}"
            )
            raise e


if __name__ == "__main__":
    os.chdir("./config/")
    dir_maker = MakeTodayWorkDir()
    dir_maker.execute_all()
