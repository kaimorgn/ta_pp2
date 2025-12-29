#!/usr/bin/env python3
#
# web_service_monitor.py
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

import pyinputplus as pyip

from features.setup_logging import setup_logging

from logging import getLogger
from pathlib import Path
import multiprocessing
import platform
import subprocess
import time
import threading

# 専用のロガーを作成
logger = getLogger(__name__)

# loggingの設定を適用
logging_config = Path("./config/logging_config.yml")
setup_logging(logging_config)


class WebServiceMonitor:
    def __init__(self, target_hosts):
        self.target_hosts = target_hosts

    @staticmethod
    def _check_server_task(host):
        '''
        [概要]
        実際にWebサービスへ通信を飛ばすメソッド
        ＊ multiprocessing による並列処理時に
           バグが起きないように静的メソッドとして定義している
        '''
        assert host, "hostを渡して"
        assert isinstance(host, str), "hostは文字列型"

        try:
            logger.debug(
                f"> {host} と通信します"
            )
            param = "-n" if platform.system().lower() == "windows" else "-c"
            command = [
                "ping", param, "3", host
            ]
            response = subprocess.run(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            logger.info(
                f">> {host} との通信結果: OK"
            )
            return True

        except Exception as e:
            logger.error(
                f"{host} との通信時にエラー発生: {e}"
            )
            raise e

    def run_sequential(self):
        '''
        [概要]
        通常の直列(上から順に)実行するメソッド
        '''
        start = time.time()

        try:
            logger.debug(
                "> 通常の直列処理を実行"
            )
            for host in self.target_hosts:
                self._check_server_task(host)

            logger.debug(
                f"> 直列処理の実行時間: {time.time() - start:.2f} 秒"
            )

        except Exception as e:
            logger.error(
                f"直列処理の実行時にエラー発生: {e}"
            )
            raise e

    def run_threading(self):
        '''
        [概要]
        threading モジュールを使って並行処理を実演するメソッド
        '''
        start = time.time()
        workers = []
        try:
            logger.debug(
                "> threading による並行処理を実行"
            )
            for host in self.target_hosts:
                thread = threading.Thread(
                    target=self._check_server_task,
                    args=(host,)
                )
                thread.start()
                workers.append(thread)

            for worker in workers:
                worker.join()

            logger.debug(
                f"> 並行処理の実行時間: {time.time() - start} 秒"
            )
            return True

        except Exception as e:
            logger.error(
                f"並行処理実行時にエラー発生: {e}"
            )
            raise e

    def run_multiprocessing(self):
        '''
        [概要]
        multiprocessing モジュールを使って並行処理を実演するメソッド
        '''
        start = time.time()
        workers = []

        try:
            logger.debug(
                "> multiprocessing モジュールによる並行処理を実行"
            )
            for host in self.target_hosts:
                process = multiprocessing.Process(
                    target=self._check_server_task,
                    args=(host,)
                )
                process.start()
                workers.append(process)

            for worker in workers:
                worker.join()

            logger.debug(
                f"> 並行処理の実行時間: {time.time() - start} 秒"
            )
            return True

        except Exception as e:
            logger.error(
                f"並行処理の実行時にエラー発生: {e}"
            )
            raise e


if __name__ == "__main__":
    targets = [
        "google.com", "github.com", "yahoo.co.jp",
        "amazon.co.jp", "bing.com", "python.org"
    ]

    logger.debug(f"監視対象のWebサービス数: {len(targets)} 個")

    mode = pyip.inputMenu(
        choices=["Sequentials", "Threading", "Multiprocessing"],
        prompt="実行モードを選択してください:\n",
        numbered=True
    )

    monitor = WebServiceMonitor(targets)

    if mode == "Sequentials":
        monitor.run_sequential()

    elif mode == "Threading":
        monitor.run_threading()

    elif mode == "Multiprocessing":
        monitor.run_multiprocessing()
