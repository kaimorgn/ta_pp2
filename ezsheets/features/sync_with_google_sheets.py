#!/usr/bin/env python3
#
# sync_with_google_sheets.py
# 
# [概要]
# ezsheetsモジュールを使って
# Google スプレッドシートを編集する
# プログラム
# 
# タイトル(ファイル名)からIDを取得したり
# セルを編集する(データを書き込む)処理を
# クラス内に定義している
#

import ezsheets

from logging import getLogger
from pathlib import Path

# 専用のロガーを作成
logger = getLogger(__name__)


class SyncWithGoogleSheets:
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
            ezsheets.init()
            logger.debug("> 新しいトークンの発行に成功しました")
            logger.info(">> 認証に成功しました")

        except Exception as e:
            logger.error(
                f"新しいトークンの発行時にエラーが発生しました: {e}"
            )
            raise e

    def _make_sheets_dict(self):
        '''
        [概要]
        listSpreadsheets()を使って，編集権限と閲覧権限がある
        スプレッドシートを辞書型で取得するメソッド．
        取得した辞書型は self.sheets_dict インスタンス変数で保持される．
        また，コンソール上には取得したシートのタイトルとIDを出力する．
        '''
        try:
            logger.debug("> 複数のスプレッドシートを取得します")
            self.sheets_dict = ezsheets.listSpreadsheets()
            if not self.sheets_dict:
                logger.warning(
                    f">>> シートを取得できなかった: {len(self.sheets_dict)}"
                )

            logger.debug("> 複数のスプレッドシートを取得しました")
            logger.info(
                f">> {len(self.sheets_dict)}個のスプレッドシートを取得しました"
            )
            
            logger.debug("> コンソール上に出力します")
            for sheet_id, title in self.sheets_dict.items():
                logger.debug(
                    f"シート名: {title}, \nシートID: {sheet_id}"
                )

            return True

        except Exception as e:
            logger.error(
                f"複数のスプレッドシート取得時にエラーが発生した: {e}"
            )
            raise e

    def _read_sheet_id_by_title(self, title_name):
        '''
        [概要]
        self._make_sheets_dict()を実行して作成した
        self.sheets_dictを参照し，引数で渡される title_name と一致する
        スプレッドシートのIDを取得するメソッド．
        取得したIDを参照してスプレッドシートのオブジェクトを作成する．
        なお，オブジェクトは self.ss インスタンス変数が保持する．
        '''
        assert title_name, "検索したいシート名を渡して"
        assert isinstance(title_name, str), "シート名は文字列型にして"
        
        self._make_sheets_dict()
        target_id = None
        try:
            logger.debug(f"> {title_name}と一致するシートを検索します")
            for sheet_id, title in self.sheets_dict.items():
                if title == title_name:
                    target_id = sheet_id
                    logger.debug(
                        f"> {title_name}と一致するシートが見つかった"
                    )
                    break

            if target_id is None:
                logger.warning(
                    f">>> {title_name}と一致するシートが見つからなかった"
                )

            logger.info(
                f">> タイトル: {title_name} (ID: {target_id})を読み込む"
            )

            return target_id

        except Exception as e:
            logger.error(
                f">>>> タイトルと一致するシート検索時にエラーが発生: {e}"
            )
            raise e

    def copy_template_sheet(self, template_sheet_name, new_sheet_name):
        '''
        [概要]
        テンプレートシートを複製するメソッド
        '''
        assert template_sheet_name, "テンプレートシートの名前を渡して"
        assert isinstance(template_sheet_name, str), "文字列型を渡して"
        assert new_sheet_name, "複製後のシート名を渡して"
        assert isinstance(new_sheet_name, str), "文字列型を渡して"

        template_id = self._read_sheet_id_by_title(template_sheet_name)
        template_ss = ezsheets.Spreadsheet(template_id)
        downloads_path = Path(f"./{new_sheet_name}.xlsx")
        try:
            logger.debug(
                f"> テンプレート {template_sheet_name} を複製する"
            )
            template_ss.downloadAsExcel(downloads_path)

            if downloads_path.exists() == True:
                self.ss = ezsheets.upload(downloads_path.name)
                downloads_path.unlink(missing_ok=True)
                logger.debug(
                    f"> 複製時にダウンロードしたファイルを削除した"
                )
            
            logger.debug(
                f"> テンプレートの複製に成功した -> {new_sheet_name}"
            )
            logger.info(
                f">> テンプレートを複製した -> {new_sheet_name}"
            )

            return True

        except Exception as e:
            logger.error(
                f">>>> テンプレートの複製時にエラーが発生した: {e}"
            )
            raise e

    def edit_sheet_cell(self, cell, data, sheet_num=0):
        '''
        [概要]
        特定のシート内のセルを編集する(データを書き込む)ためのメソッド
        '''
        assert cell, "編集対象のセルを渡してください"
        assert isinstance(cell, str), "編集対象のセルは文字列で指定する"
        assert data, "セルに書き込むデータを渡してください"

        sheet = self.ss[sheet_num]
        try:
            logger.debug(f"'{cell}' セルに {data} を書き込みます")
            sheet[cell] = data
            logger.debug(f"'{cell}' セルに {data} を書き込みました")

            return True

        except Exception as e:
            logger.error(
                f"セルにデータを書き込む際にエラーが発生しました: {e}"
            )
            raise e

    def edit_sheet_row(self, row_num, data_list, sheet_num=0):
        '''
        [概要]
        特定のシート内の行を編集する(データを書き込む)ためのメソッド
        '''
        assert row_num, "データを挿入する行を数値で指定してください"
        assert isinstance(row_num, int), "行は整数型で渡してください"
        assert data_list, "data_listが空です"
        assert isinstance(data_list, list), "データはリスト型で渡して"

        sheet = self.ss[sheet_num]
        try:
            logger.info(">> データを追加します")
            sheet.updateRow(row_num, data_list)
            logger.debug("> データを追加しました")

            return True

        except Exception as e:
            logger.error(
                f">>>> データ更新中にエラーが発生しました: {e}"
            )
            raise e

    
if __name__ == "__main__":
    from setup_logging import setup_logging
    import os
    import time

    os.chdir("../config/")
    logging_config = Path("./logging_config.yml")
    setup_logging(logging_config)

    template_sheet_name  = "25PP2_W11_VM-Monitor"
    new_sheet_name = "m26d003@mse08vm03"
    sync_with_google_sheets = SyncWithGoogleSheets()
    sync_with_google_sheets.copy_template_sheet(
        template_sheet_name, new_sheet_name
    )
    data_lists = [
        [4.5, 9.2],
        [5.2, 10.6],
        [6.1, 10.7],
        [6.5, 10.9],
        [8.5, 12.2]
    ]
    for index, row_num in enumerate(data_lists):
        row_num = index + 1
        sync_with_google_sheets.edit_sheet_row(row_num, data_list)
        logger.debug("> 次のデータ挿入まで3秒待機します")
        time.sleep(3)
