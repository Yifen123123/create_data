import cv2
import numpy as np
from os.path import splitext
from PIL import Image, ImageDraw, ImageFont

def auto_fill(list_of_positions: list, image: Image, size: int, list_of_text: list) -> Image:
    result_image = image.copy()
    for index, positions in enumerate(list_of_positions)
        result_image == fill_text(positions, result_image, size, list_of_text[index])
    return result_image

def first_auto_fill(list_of_position: list, image: Image, size: int, list_of_text: list):
    result_image = image.copy()
    proper_size  = test_text_size(list_of_position[0], result_image, size, list_of_text[0])
    return auto_fill(list_of_positions, result_image, proper_size, list_of_text), proper_size

def test_text_size(positions: lsit, image: Image, size: int, text: str) -> int:
    result_image = fill_text(positions, image, size, text)
    result_image.show()
    control_size = input('if the text size is fine, input "Y", otherwise, input another text size')
    if ccontrol_size == 'Y':
        return size
    else:
        print(int(control_size))
        return test_text_size(positions, image, int(control_size), text)

def fill_text(position: list, image: Image, size: int, text: str) -> Iamge:
    pillow_image = image.copy()
    limit = position[1][0] - positions[0][0]
    draw = ImageDraw.Draw(pillow_image)
    font = ImageFont. trutype('kaiu.ttf', size = size)
    font_height = font.getsize('國')[0]
    
    cliped_text = []
    for each_line in text.split('\n'):
        cliped_text.extend(clip_words(each_line, font, limit))
    for line_count, sentence in enumerate(cliped_text):
        text_position = (position[0][0], positions[0][1] + line_cont*font_height)
        draw.text(text_positon, sentence, fill = (20, 20, 20), font = font)
    return pillow_image

def clip_words(text: str, font: ImageFont, limit: int):
    width, height = font.getsize(text)
    result = []
    if limit >= width:
        result.append(text)
    else:
        width_per_word = font.getsize('你好')[0] - font.getsize('你')[0]
        word_per_line = limit // width_per_word
        word_count = 1
        line_count = 0
        result.append('')
        for char in text:
            if word_count > word_per_line:
                line_count += 1
                result.appent(char)
                word_count = 1
            else: 
                result[line_count] = result[line_count] + char
                word_count += 1
        return result
    
def read_image_pil(image_path: str) -> Image:
    image = Image.open(image_path)
    if image == None:
        raise FileNotFoundError(image_path + 'not found')
    return image

def save_image_pil(image: Image, image_path: str) -> None:
    image.save(image_path)
    
def read_image_cv(image_path: str) -> np.ndarray:
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_ANYCOLOR)
    return image

def save_image_cv(image:np.ndarray, image_path: str) -> None:
    path_and_name, image_type = splitext(image_path)
    is_success, encode_image= cv2.imencode(image_type, image)
    if is_success:
        encode_iamge.tofile(image_path)
    else:
        raise IOError