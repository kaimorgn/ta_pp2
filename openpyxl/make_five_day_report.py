#!/usr/bin/env python3
#
# make_five_day_report.py
#
# [概要]
# 秋県大のキャリア情報センターが配布している
# インターンシップ実習報告書（1~3日間，5日間，10日間）を
# 自動編集して保存するプログラム．
# 
# なお，openpyxlを使った操作は
# features/excel_editor.py を参照すること．
#

from datetimejp import JDatetime

from features.copy_template import copy_template
from features.datetime_manager import make_internship_period, make_date_list
from features.excel_editor import load_worksheet, edit_cell, save_workbook, insert_internship_info, insert_internship_schedule, insert_internship_summary, insert_message_for_junior
from features.txt_reader import read_txt

from logging import getLogger
from pathlib import Path

# 専用のロガーを作成
logger = getLogger(__name__)


def make_five_day_report(save_dir, txt_path):
    '''
    '''
    assert isinstance(save_dir, Path), "save_dirはPathオブジェクトにして"

    five_day_report_path = Path(
        "input/internship_training_report_5_day_format.xlsx"
    )
    save_path = save_dir / "internship_training_report_5day.xlsx"

    try:
        wb_obj, ws = load_worksheet(five_day_report_path, "5day")
                
        base_date = JDatetime.today()
        days_delta = 5
        e_column_list = [
            "経営システム工学科",
            "XXX株式会社",
            "由利本荘市部",
            make_internship_period(base_date, days_delta),
        ]

        w_column_list = [
            "吉田 快",
            "土谷字海老ノ口84-4"
        ]
        insert_internship_info(
            ws, base_date, days_delta, e_column_list, w_column_list
        )
        date_list = make_date_list(base_date, days_delta)
        content_list, comment_list = read_txt(txt_path, days_delta)
        insert_internship_schedule(ws, date_list, content_list, comment_list)
        
        num = 15
        summary = """
        今回の5日間の実習では、主に社内の開発フローの見学と、
        基礎的なテスト業務の体験をさせていただきました。
        大学の講義で習うプログラミングとは異なり、
        実際の現場では「読みやすさ」や「保守性」が徹底して重視されている点に
        大きな衝撃を受けました。
        特に朝会（デイリースクラム）への参加を通じて、
        チーム全体で進捗を共有し、問題発生時に即座に助け合う文化を
        肌で感じることができました。
        短期間ではありましたが、エンジニアとして働く
        具体的なイメージを持つことができた貴重な3日間でした。
        """
        insert_internship_summary(ws, summary, num)

        num = 17
        message = """
        5日間という短い期間ですが、得られるものは非常に多いです。
        最初は緊張して質問を躊躇してしまうかもしれませんが、
        社員の方々は「学生が何を知らないか」を理解してくれているので、
        恐れずに質問することをお勧めします。
        技術的なことだけでなく、オフィスの雰囲気や社員同士の会話のテンポなど、
        現場に行かないと分からない「空気感」を大事にしてください。
        挨拶は大きな声ですると好印象です！
        """
        insert_message_for_junior(ws, message, num)
        
        save_workbook(wb_obj, save_path)
        
        return True

    except Exception as e:
        logger.error(
            f"実習報告書(5日間)の編集中にエラーが発生しました: {e}"
        )
        raise e


if __name__ == "__main__":
    from features.setup_logging import setup_logging

    setup_logging()

    save_dir = Path("output")
    if save_dir.exists() == False:
        save_dir.mkdir(exist_ok=True)
        logger.debug(f"{save_dir}を新規作成しました")

    else:
        logger.debug(f"{save_dir}は作成済みです")

    txt_path = Path("./input/report_data_5day.txt")
    make_five_day_report(save_dir, txt_path)
