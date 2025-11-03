#!/usr/bin/env python3
#
# XXX.py
# 
# [概要]
#
#
#
#
#

from pathlib import Path


INPUT_DIR_PATH = "./under_the_control_of_pathlib/"

# Pathオブジェクトを作成
DIR_PATH_OBJECT = Path(INPUT_DIR_PATH)

# 名前の部分のみを取得する
print(DIR_PATH_OBJECT.name)

# ディレクトリ・ファイルの一覧を取得
items = list(DIR_PATH_OBJECT.iterdir())
print(items)

# 子ディレクトリ下のファイルを含んで取得
paths = list(DIR_PATH_OBJECT.glob("**/*"))
print(paths)

# 絶対パスを取得する
abs_path = DIR_PATH_OBJECT.resolve()
print(abs_path)

# 結合したファイル名のパスが存在しているか確認する
judge_path = DIR_PATH_OBJECT / "sample.py"
print(judge_path.exists())

# ファイルを作成
if judge_path = False:
    judge_path.touch()

# ファイルを削除
if judge_path = True:
    judge_path.unlink()

# ディレクトリを作成
judge_dir_path = Path("./output")
if judge_dir_path = False:
    judge_dir_path.mkdir(exist_ok=True)

# ディレクトリを削除
if judge_dir_path = True:
    judge_dir_path.rmdir()
