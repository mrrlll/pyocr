import os
import tkinter as tk
from tkinter import filedialog
import re

def remove_multibyte(text):
    """マルチバイト文字を削除する関数"""
    return re.sub(r'[^\x00-\x7F]+', '', text)

def select_folder_and_rename():
    """フォルダーを選択し、画像ファイルの名前を変更する関数"""

    # ルートウィンドウを作成
    root = tk.Tk()
    root.withdraw()

    # フォルダー選択ダイアログを開く
    folder_path = filedialog.askdirectory()

    if folder_path:
        # 選択したフォルダー内のファイルとディレクトリを取得
        for filename in os.listdir(folder_path):
            # ファイルの場合
            if os.path.isfile(os.path.join(folder_path, filename)):
                # ファイル名からマルチバイト文字を削除
                new_filename = remove_multibyte(filename)
                # ファイル名を変更
                os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))

        print("ファイル名の変更が完了しました。")

if __name__ == "__main__":
    select_folder_and_rename()