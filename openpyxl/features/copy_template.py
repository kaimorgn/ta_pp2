#!/usr/bin/env python3
#
# copy_template.py
#
# [概要]
# shutil モジュールを使って
# ファイルを複製するためのプログラム．
#

from logging import getLogger
import shutil

# 専用のロガーを作成
logger = getLogger(__name__)


def copy_template(template_path, output_path):
    '''
    [概要]
    第 8 週目で扱った shutil モジュールを使って
    テンプレートファイルを複製する関数．
    
    例: Word, Excelなど
    '''
    assert isinstance(template_path, Path), "templateはPathオブジェクトにする"
    assert isinstance(output_path, Path), "outputもPathオブジェクトにする"

    try:
        logger.info(f"{template_path} を複製します")

        shutil.copy(
            template_path, output_path
        )
        
        logger.info(f"{template_path} を複製しました ->  {output_path}")

        return True
    
    except Exception as e:
        logger.error(
            f"テンプレートの複製中にエラーが発生しました: {e}"
        )
        raise e


if __name__ == "__main__":
    from setup_logging import setup_logging
    from pathlib import Path

    setup_logging()
    template_path = Path("XXX")
    output_path = Path("XXX")
    copy_template(template_path, output_path)
