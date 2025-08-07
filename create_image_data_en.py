import cv2
import numpy as np
import textwrap
from os.path import splitext
from PIL import Image, ImageDraw, ImageFont

def read_image_pil(image_path: str) -> Image.Image:
    image = Image.open(image_path)
    if image is None:
        raise FileNotFoundError(image_path + ' not found')
    return image

def save_image_pil(image: Image.Image, image_path: str) -> None:
    image.save(image_path)

def clip_words(text: str, font: ImageFont.ImageFont, limit: int):
    result = []
    line = ""

    for word in text.split(" "):  # 英文用空格斷詞
        test_line = line + (" " if line else "") + word
        test_width = font.getbbox(test_line)[2] - font.getbbox(test_line)[0]

        if test_width <= limit:
            line = test_line
        else:
            if line:
                result.append(line)
            line = word

    if line:
        result.append(line)

    return result

def fill_text(position: list, image: Image.Image, size: int, text: str) -> Image.Image:
    pillow_image = image.copy()
    limit = position[1][0] - position[0][0]
    draw = ImageDraw.Draw(pillow_image)

    # font_path = "/System/Library/Fonts/STHeiti Medium.ttc"  # macOS 內建中文字體
    font_path = "/System/Library/Fonts/Arial.ttf"  #mac 純英文字
    try:
        font = ImageFont.truetype(font_path, size=size)
    except OSError:
        print("❌ 無法載入字型，改用預設字型")
        font = ImageFont.load_default()

    font_height = font.getbbox("國")[3] - font.getbbox("國")[1]

    clipped_text = []
    for each_line in text.split('\n'):
        clipped_text.extend(clip_words(each_line, font, limit))

    for line_count, sentence in enumerate(clipped_text):
        line_spacing = 1.4
        text_position = (position[0][0], position[0][1] + int(line_count * font_height* line_spacing))
        draw.text(text_position, sentence, fill=(20, 20, 20), font=font)

    return pillow_image

def test_text_size(position: list, image: Image.Image, size: int, text: str) -> int:
    result_image = fill_text(position, image, size, text)
    result_image.show()
    control_size = input('✅ 若字體大小合適請輸入 "Y"，否則輸入新字體大小：')
    if control_size.upper() == 'Y':
        return size
    else:
        return test_text_size(position, image, int(control_size), text)

def auto_fill(list_of_positions: list, image: Image.Image, size: int, list_of_text: list) -> Image.Image:
    result_image = image.copy()
    for idx, position in enumerate(list_of_positions):
        result_image = fill_text(position, result_image, size, list_of_text[idx])
    return result_image

def first_auto_fill(list_of_positions: list, image: Image.Image, size: int, list_of_text: list):
    proper_size = test_text_size(list_of_positions[0], image, size, list_of_text[0])
    return auto_fill(list_of_positions, image, proper_size, list_of_text), proper_size

def apply_fake_text(image_path: str, position_path: str, fake_text_list: list, default_size: int = 24):
    image = read_image_pil(image_path)
    with open(position_path, 'r') as f:
        positions = eval(f.read())
    if len(fake_text_list) != len(positions):
        raise ValueError(f"假資料筆數（{len(fake_text_list)}）與位置數量（{len(positions)}）不符！")

    filled_image, used_size = first_auto_fill(positions, image, default_size, fake_text_list)

    path_and_name, suffix = splitext(image_path)
    output_path = path_and_name + '_filled' + suffix
    save_image_pil(filled_image, output_path)
    print(f"已儲存填入假資料後圖片：{output_path}")
    print(f"✏️ 使用字體大小：{used_size}")
