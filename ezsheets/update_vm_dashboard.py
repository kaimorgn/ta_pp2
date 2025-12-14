#!/usr/bin/env python3
#
# update_vm_dashboard.py
#
# [概要]
#
#
#
#
#
#
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
        '''
        return {
            "user": getpass.getuser(),
            "pc_name": socket.gethostname()
        }

    def _merge_static_info(self):
        '''
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

            for key, value in self.static.items():
                cell_num = f"C{target_num}"
                self.sync_with_google_sheets.edit_sheet_cell(
                    cell_num, value
                )
                target_num += 2            

        except Exception as e:
            logger.error(
                f"静的情報を書き込み中にエラーが発生しました: {e}"
            )
            raise e


if __name__ == "__main__":
    os.chdir("./config/")
    
    vm_updater = UpdateVMDashboard()
    vm_updater._merge_static_info()

    template_sheet_name = "25PP2_W11_VM-Monitor"
    vm_updater.insert_static_info(template_sheet_name)
    
