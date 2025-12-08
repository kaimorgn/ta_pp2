#!/usr/bin/env python3
#
# make_snapshot.py
#
# [概要]
# zipfile モジュールを使って
# スナップショット(ZIPファイル)を
# 作成するためのプログラム．
#

from logging import getLogger
from pathlib import Path
import zipfile

# 専用のロガーを作成
logger = getLogger(__name__)


def make_snapshot(data_path, snapshot_path):
    '''
    [概要]
    第 8 週目で扱った zipfile モジュールを使って
    ZIPファイルを作成する関数．
    '''
    assert isinstance(data_path, Path), "data_pathはPathオブジェクトにする"
    assert isinstance(snapshot_path, Path), "snapshot_pathもPathオブジェクト"

    try:
        logger.info("スナップショット（ZIPファイル）を作成します")

        items = list(data_path.iterdir())
        with zipfile.ZipFile(snapshot_path, "w") as zf:
            for i, item in enumerate(items):
                zf.write(item)

        logger.info(f"スナップショットを作成しました ->  {snapshot_path}")

        return True

    except FileNotFoundError as e:
        logger.error(
            f"対象のディレクトリ/ファイルが見つかりませんでした: {e}"
        )
        raise e

    except Exception as e:
        logger.error(
            f"スナップショットの作成中にエラーが発生しました: {e}"
        )
        raise e


if __name__ == "__main__":
    from setup_logging import setup_logging
    from pathlib import Path

    setup_logging()
    data_path = Path("XXX")
    snapshot_path = Path("XXX")
    make_snapshot(data_path, snapshot_path)
