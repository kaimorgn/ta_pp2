#!/usr/bin/env python3
#
# sync_ram.py
#
# [概要]
# RAMの情報を取得して返すプログラム
#

import psutil

from logging import getLogger

# 専用のロガーを作成
logger = getLogger(__name__)


class SyncRAM:
    def __init__(self):
        pass

    def _bytes_to_gb(self, bytes_int):
        '''
        [概要]
        バイト単位の数値をギガバイト(GB)単位に
        変換するメソッド
        '''
        assert bytes_int, "数値が渡されていません"
        assert isinstance(bytes_int, int), "整数型の数値を渡してください"
        
        return round(bytes_int / (1024 ** 3), 2)

    def read_total_virtual_memory(self):
        '''
        [概要]
        OSが認識している物理メモリの総量(静的情報)を取得して返すメソッド
        '''
        return self._bytes_to_gb(psutil.virtual_memory().total)

    def read_total_swap_memory(self):
        '''
        [概要]
        OSが認識しているスワップメモリの総量(静的情報)を取得して返すメソッド
        '''
        return self._bytes_to_gb(psutil.swap_memory().total)

    def read_latest_virtual_memory_percent(self):
        '''
        [概要]
        呼び出し時点での物理メモリ使用率を返すメソッド
        '''
        return psutil.virtual_memory().percent

    def read_latest_swap_memory_percent(self):
        '''
        [概要]
        呼び出し時点でのスワップメモリ使用率を返すメソッド
        '''
        return psutil.swap_memory().percent

    def collect_static_info(self):
        '''
        [概要]
        RAMの静的情報を期待通りに取得できているかを
        確認する(デバッグ用)ためのメソッド
        '''
        logger.debug("> RAMの静的情報を出力します")

        logger.debug(
            f"> RAM Virtual Memory: '{self.read_total_virtual_memory()}'"
        )
        logger.debug(
            f"> RAM Swap Memory: '{self.read_total_swap_memory()}'"
        )

        return {
            "ram_total_virtual_memoty": self.read_total_virtual_memory()
        }

    def collect_dynamic_info(self):
        '''
        [概要]
        RAMの動的情報を期待通りに取得できているかを
        確認する(デバッグ用)ためのメソッド
        '''
        logger.debug("> RAMの動的情報を出力します")

        logger.debug(
            f"> RAM Virtual(%): '{self.read_latest_virtual_memory_percent()}%'"
        )
        logger.debug(
            f"> RAM Swap(%): '{self.read_latest_swap_memory_percent()}%'"
        )


if __name__ == "__main__":
    from setup_logging import setup_logging
    from pathlib import Path

    logging_config = Path("../config/logging_config.yml")
    setup_logging(logging_config)

    sync_ram = SyncRAM()
    sync_ram.collect_static_info()
    sync_ram.collect_dynamic_info()
    
