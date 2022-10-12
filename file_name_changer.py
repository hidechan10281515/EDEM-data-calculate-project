# 必要なライブラリのインポート
import os
import re
from glob import glob
import pandas as pd
 
 
# 一括変更するファイルのディレクトリパスを指定
file_dir = input("directory path >> ")
file_dir = re.sub(r"[\"\' ]", "", file_dir)
 
# 一括変更するファイルの拡張子を指定（複数可）
exts = input("extensions >> ")
exts = [ext.replace(" ", "") for ext in exts.split(" ")]
 
# 新しく統一するファイル名を指定
new_name_temp = input("new name >> ")
 
# 指定した拡張子のファイルパスをすべて取得する
file_paths = []
for ext in exts:
    for path in glob(os.path.join(file_dir, f"*.{ext}")):
        file_paths.append(path)
 
old_names = []   # 変更前のファイル名のリスト
new_names = []   # 変更後のファイル名のリスト
 
for i, file_path in enumerate(file_paths):
    old_name = os.path.basename(file_path)   # 変更前のファイル名
    ext = old_name.split(".")[-1]   # 拡張子を取得
    new_name = f"{new_name_temp}{i+1:02d}." + ext   # 変更後のファイル名
    os.rename(file_path, os.path.join(file_dir, new_name))   # ファイル名変更
 
    old_names.append(old_name)   # リストに追加
    new_names.append(new_name)   # リストに追加
 
# ログをCSVファイルとして保存
logs = pd.DataFrame({"old name": old_names, "new name": new_names})
logs.to_csv(os.path.join(file_dir, "logs.csv"), index=False)