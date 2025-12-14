#!/usr/bin/env python3
#
# sync_cpu.py
#
# [概要]
# CPUのスペックや稼働状況を
# 取得して返すプログラム
#

import cpuinfo
import platform
import psutil

from logging import getLogger

# 専用のロガーを作成
logger = getLogger(__name__)


class SyncCPU:
    def __init__(self):
        self.cpu_info = cpuinfo.get_cpu_info()

    def read_cpu_vendor(self):
        '''
        [概要]
        CPUのベンダー(製造元)を取得するメソッド
        '''
        return self.cpu_info["vendor_id_raw"]


    def read_cpu_brand(self):
        '''
        [概要]
        CPUのブランド名(製品名)を取得するメソッド
        '''
        return self.cpu_info["brand_raw"]

    def read_machine_type(self):
        '''
        [概要]
        マシンのアーキテクチャ(ハードウェアの種類)を
        取得するメソッド
        '''
        return platform.machine()

    def read_logical_cores(self):
        '''
        [概要]
        CPUの論理コア数を取得して返すメソッド
        '''
        return psutil.cpu_count(logical=True)

    def read_phisical_cores(self):
        '''
        [概要]
        CPUの物理コアを取得して返すメソッド
        '''
        return psutil.cpu_count(logical=False)

    def read_cores_utilities(self):
        '''
        [概要]
        CPU全体の平均使用率を取得して返すメソッド
        0.5秒間の平均使用率を計測して1つの数値として返している
        '''
        return psutil.cpu_percent(interval=0.5, percpu=False)

    def collect_static_info(self):
        '''
        [概要]
        CPUの静的情報を期待通りに取得できているかを
        確認する(デバッグ用)ためのメソッド
        '''
        logger.debug("> CPUの静的情報のみを出力します")

        logger.debug(f"> CPU Vendor: '{self.read_cpu_vendor()}'")
        logger.debug(f"> CPU Brand: '{self.read_cpu_brand()}'")
        logger.debug(f"> Machine Type: '{self.read_machine_type()}'")
        logger.debug(f"> Logical Cores: '{self.read_logical_cores()}'")
        logger.debug(f"> Phisical Cores: '{self.read_phisical_cores()}'")

        return {
            "cpu_vendor": self.read_cpu_vendor(),
            "cpu_brand": self.read_cpu_brand(),
            "machine_type": self.read_machine_type(),
            "logical_cores": self.read_logical_cores(),
            "phisical_cores": self.read_phisical_cores()
        }

    def collect_dynamic_info(self):
        '''
        [概要]
        CPUの動的情報を期待通りに取得できているかを
        確認する(デバッグ用)ためのメソッド
        今回はCPUの平均使用率のみを確認
        '''
        logger.debug("> CPUの動的情報のみを出力します")
        
        logger.debug(f"> CPU Utilities: '{self.read_cores_utilities()}'")
        
        return {
            "cpu_utilities": self.read_cores_utilities()
        }


if __name__ == "__main__":
    from setup_logging import setup_logging
    from pathlib import Path

    logging_config = Path("../config/logging_config.yml")
    setup_logging(logging_config)

    # CPUの静的情報と動的情報を出力チェック
    sync_cpu = SyncCPU()
    sync_cpu.collect_static_info()
    sync_cpu.collect_dynamic_info()
