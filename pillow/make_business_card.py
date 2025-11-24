#!/usr/bin/env python3
#
# make_business_card.py
#
# [概要]
# Web スクレイピングの講義で取得した
# ポケモンの画像を使い，
# ゲームフリークリスペクトな
# 名刺を作成するプログラム．
#

from PIL import Image, ImageDraw, ImageFont

from features.setup_logging import setup_logging

from logging import getLogger
from pathlib import Path

# logging の設定を反映してロガーを作成
setup_logging()
logger = getLogger(__name__)


def make_draw_object(w, h, bg_color):
    base_img = Image.new(
        "RGB",
        (w, h),
        bg_color
    )
    drw_obj = ImageDraw.Draw(base_img)
    logger.info("ベース画像を新規作成しました")

    return drw_obj, base_img


def font_settings():
    try:
        font_path_bold = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
        font_path_reg = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc"
        font_eng = ImageFont.truetype(font_path_bold, 18)
        font_name = ImageFont.truetype(font_path_bold, 45)
        font_title = ImageFont.truetype(font_path_reg, 24)
        font_info = ImageFont.truetype(font_path_reg, 18)

        logger.info(
            "フォントオブジェクトを設定し，辞書型で返します"
        )
        
        return {
            "eng": font_eng,
            "name": font_name,
            "title": font_title,
            "info": font_info
        }
        
    except OSError:
        logger.error(
            f"警告: フォントが見つかりません: {e}"
        )
        raise


def paste_pokemon_img(h, pokemon_image_path, base_img):
    img_area_size = 300
    img_margin_x = 1
    img_margin_y = int((h - img_area_size) / 2)

    try:
        pokemon_img = Image.open(pokemon_image_path).convert("RGBA")
        logger.info(
            f"ポケモンの画像を読み込みました: {pokemon_image_path}"
        )

        target_height = int(h * 1.5)
        aspect_ratio = pokemon_img.width / pokemon_img.height
        target_width = int(target_height * aspect_ratio)
        pokemon_img = pokemon_img.resize(
            (target_width, target_height),
            Image.Resampling.LANCZOS
        )
        paste_y = (h - target_height) // 2
        paste_x = -100

        base_img.paste(
            pokemon_img,
            (paste_x, paste_y),
            pokemon_img
        )

        logger.info("ポケモン画像の貼り付けが完了しました")

        return True

    except Exception as e:
        logger.error(
            f"ポケモン画像の貼り付け中にエラーが発生しました: {e}"
        )
        raise


def insert_text(base_img, bg_color, w, font_dict, my_title, my_name, save_path):
    new_drw_obj = ImageDraw.Draw(base_img)

    text_start_x = 280
    current_y = 100
    text_color = (10, 10, 10)
    stroke_w = 4
    stroke_c = bg_color
    try:
        eng_organization = "Akita Prefectural University"
        bbox = new_drw_obj.textbbox(
            (0, 0),
            eng_organization,
            font=font_dict["eng"]
        )
        eng_organization_w = bbox[2] - bbox[0]
        new_drw_obj.text(
            (w - eng_organization_w - 20, 20),
            eng_organization,
            font=font_dict["eng"],
            fill=(0, 0, 0),
            stroke_width=stroke_w,
            stroke_fill=stroke_c
        )
        
        # 役職名の挿入
        new_drw_obj.text(
            (text_start_x, current_y),
            my_title,
            font=font_dict["title"],
            fill=text_color,
            stroke_width=stroke_w,
            stroke_fill=stroke_c
        )
        current_y += 35

        # 氏名を挿入
        new_drw_obj.text(
            (text_start_x, current_y),
            my_name,
            font=font_dict["name"],
            fill=text_color,
            stroke_width=stroke_w,
            stroke_fill=stroke_c
        )
        current_y += 65

        # 黒線を描画
        new_drw_obj.line(
            (text_start_x, current_y, w - 30, current_y),
            fill=(0, 0, 0),
            width=2
        )
        current_y += 20

        jp_organization = "秋田県立大学"
        address_text = "〒015-0834\n秋田県由利本荘市\n土谷字海老ノ口 84-4"

        # アドレスを挿入
        new_drw_obj.text(
            (text_start_x, current_y),
            jp_organization,
            font=font_dict["info"],
            fill=text_color,
            stroke_width=stroke_w,
            stroke_fill=stroke_c
        )
        current_y += 30

        new_drw_obj.text(
            (text_start_x, current_y),
            address_text,
            font=font_dict["info"],
            fill=(60, 60, 60),
            spacing=6,
            stroke_width=stroke_w,
            stroke_fill=stroke_c
        )

        base_img.save(save_path)
        logger.info(
            f"名詞が完成しました! 出力先をご確認ください!: {save_path}"
        )
        return True

    except Exception as e:
        logger.error(
            f"名詞作成中にエラーが発生しました: {e}"
        )
        raise


def main(pokemon_image_path, my_title, my_name, save_path):
    w, h = 600, 360
    bg_color = (250, 250, 240)
    drw_obj, base_img = make_draw_object(w, h, bg_color)
    font_dict = font_settings()
    paste_pokemon_img(h, pokemon_image_path, base_img)
    insert_text(base_img, bg_color, w, font_dict, my_title, my_name, save_path)

    
if __name__ == "__main__":
    pokemon_image_path = Path("./input/favorite_pokemon.png")
    my_title = "Teaching Assistant"
    my_name = "吉田 快"
    save_dir_path = Path("output")
    save_dir_path.mkdir(exist_ok=True)
    save_image_path = save_dir_path / "my_business_card.png"

    main(pokemon_image_path, my_title, my_name, save_image_path)
