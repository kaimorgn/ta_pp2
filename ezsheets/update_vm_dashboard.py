#!/usr/bin/env python3
#
# update_vm_dashboard.py
#
# [概要]
# テンプレートシート(https://docs.google.com/spreadsheets/d/1IVUYquk99pOLGGsfFbvJTJlw7-QZpCR5etbZ9IYsM8E/edit?gid=0#gid=0)を
# 複製して無限に情報を書き込み続けるプログラム
#

from features.sync_cpu import SyncCPU
from features.setup_logging import setup_logging
from features.sync_ram import SyncRAM
from features.sync_with_google_sheets import SyncWithGoogleSheets

from logging import getLogger
from pathlib import Path
import getpass
import os
import socket
import time

# 専用のロガーを作成
logger = getLogger(__name__)

# loggingの設定を反映
logging_config = Path("./config/logging_config.yml")
setup_logging(logging_config)


class UpdateVMDashboard:
    def __init__(self):
        self.sync_cpu = SyncCPU()
        self.sync_ram = SyncRAM()
        self.sync_with_google_sheets = SyncWithGoogleSheets()

    def _read_user_and_pc(self):
        '''
        [概要]
        getpassモジュールとsocketモジュールを使い
        ユーザ名とPC名を取得して辞書にまとめるメソッド
        _merge_static_info()メソッドで呼び出される
        '''
        return {
            "user": getpass.getuser(),
            "pc_name": socket.gethostname()
        }

    def _merge_static_info(self):
        '''
        [概要]
        他機能を使って取得した静的(PC稼働中に変化しない)情報を
        1つの辞書にまとめるメソッド
        '''
        try:
            logger.info(">> ユーザとCPU，RAMの静的情報を取得します")
            user_and_pc_name = self._read_user_and_pc()
            cpu_static_info = self.sync_cpu.collect_static_info()
            ram_static_info = self.sync_ram.collect_static_info()

            logger.info(">> ユーザとCPU，RAMの静的情報を取得しました")
            logger.debug(f"> ユーザ関連の静的情報: {len(user_and_pc_name)}")
            logger.debug(f"> CPUの静的情報辞書: {len(cpu_static_info)}")
            logger.debug(f"> RAMの静的情報辞書: {len(ram_static_info)}")

            self.static = user_and_pc_name | cpu_static_info | ram_static_info
            logger.debug(
                f"> CPUとRAMの静的情報を連結しました: {self.static}"
            )
            return True

        except Exception as e:
            logger.error(
                f"静的情報書き込み時にエラーが発生しました: {e}"
            )
            raise e

    def insert_static_info(self, template_sheet_name):
        '''
        [概要]
        静的な情報を書き込むためのメソッド
        一度しか実行しない
        '''
        self._merge_static_info()

        target_num = 5
        try:
            logger.info(">> テンプレートを複製して静的情報を書き込みます")
            new_sheet_name = f"{self.static['user']}@{self.static['pc_name']}"
            logger.debug(
                f"> {template_sheet_name}を{new_sheet_name}として複製します"
            )
            self.sync_with_google_sheets.copy_template_sheet(
                template_sheet_name, new_sheet_name
            )
            
            logger.info(">> 複製したシートに静的情報を書き込みます")
            for key, value in self.static.items():
                cell_num = f"C{target_num}"
                self.sync_with_google_sheets.edit_sheet_cell(
                    cell_num, value
                )
                target_num += 2
                time.sleep(3)

        except Exception as e:
            logger.error(
                f"静的情報を書き込み中にエラーが発生しました: {e}"
            )
            raise e

    def insert_dynamic_info(self, row_num):
        '''
        [概要]
        動的な情報を書き込むためのメソッド
        繰り返し処理の中で実行され続ける
        '''
        dynamic_info_list = [
            self.sync_cpu.read_cores_utilities(),
            self.sync_ram.read_latest_virtual_memory_percent()
        ]
        try:
            logger.debug("> CPUとRAMの動的な情報を書き込みます")
            self.sync_with_google_sheets.edit_sheet_row(
                row_num, dynamic_info_list
            )
            logger.debug("> CPUとRAMの動的な情報を書き込みました")

            return True

        except Exception as e:
            logger.error(
                f"動的な情報書き込み時にエラーが発生しました: {e}"
            )
            raise e


def main():
    '''
    [概要]
    全行程一括実行用の関数
    '''
    # client_secret_*.jsonがあるディレクトリへ移動
    os.chdir("./config/")

    # インスタンスを生成
    vm_updater = UpdateVMDashboard()
    vm_updater._merge_static_info()

    # 編集開始
    template_sheet_name = "25PP2_W11_VM-Monitor"
    vm_updater.insert_static_info(template_sheet_name)
    target_row_num = 35
    logger.debug("> 3秒おきに動的情報を書き込みます")
    logger.info(">> プログラムを停止する場合は Ctrl + c を押してください")
    try:
        # コマンド操作で停止されない限り無限に繰り返す
        while True:
            vm_updater.insert_dynamic_info(target_row_num)
            target_row_num += 1
            logger.debug("> 次の書き込みまで3秒待機します")
            time.sleep(3)

    except KeyboardInterrupt:
        logger.info(
            ">> 演習用のプログラムを停止しました．お疲れ様でした．"
        )


if __name__ == "__main__":
    main()
