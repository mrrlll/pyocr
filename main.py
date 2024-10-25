import os
import cv2
import pytesseract
from tkinter import Tk, filedialog, Listbox, Frame, Label, Canvas, Scrollbar, Text
from tkinter.ttk import Notebook
from PIL import Image, ImageTk
import configparser
from tkinter.filedialog import askdirectory


# config.iniの読み込み
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

# 設定を読み込み
preprocess_image = config.getboolean('OCR', 'preprocess_image', fallback=False)
ocr_lang = config.get('OCR', 'language', fallback='eng')
tesseract_cmd = config.get('OCR', 'tesseract_cmd', fallback=r'C:\Program Files\Tesseract-OCR\tesseract.exe')

# Tesseract のパスを設定
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

def process_image(image_path):
    # 画像を読み込む
    img = cv2.imread(image_path)

    if preprocess_image:
        # 解像度を確認し、必要であれば300dpiに調整
        dpi = img.shape[1] / (img.shape[0] / 300)  # 簡易的なDPI計算
        if dpi != 300:
            height = int(img.shape[0] * 300 / dpi)
            img = cv2.resize(img, (img.shape[1], height), interpolation=cv2.INTER_CUBIC)

        # グレースケール化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # バイラテラルフィルタでノイズ除去
        blur = cv2.bilateralFilter(gray, 9, 75, 75)

        # 二値化
        img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    return img

def main():
    # Tkinterを使ってフォルダ選択ダイアログを表示
    root = Tk()
    root.withdraw()
    folder_path = askdirectory(
        title="画像フォルダを選択してください"
    )

    if not folder_path:
        print("フォルダが選択されていません。")
        return

    # 選択されたフォルダ内の画像ファイルを取得
    image_extensions = (".jpg", ".jpeg", ".png", ".bmp")
    image_paths = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(image_extensions)
    ]

    # 画像ファイルを処理
    for image_path in image_paths:
        try:
            # 画像を処理
            processed_img = process_image(image_path)

            # pytesseractでOCR実行
            text = pytesseract.image_to_string(processed_img, lang=ocr_lang)

            # ファイル名を取得し、拡張子を.txtに変更
            file_name, _ = os.path.splitext(image_path)
            txt_file_path = f"{file_name}.txt"

            # テキストファイルを書き込み
            with open(txt_file_path, 'w', encoding='utf-8') as f:
                f.write(text)

            print(f"{image_path} のOCR処理が完了しました。")

        except Exception as e:
            print(f"{image_path} の処理中にエラーが発生しました: {e}")

if __name__ == "__main__":
    main()
