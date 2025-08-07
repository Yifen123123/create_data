import cv2
import numpy as np
from os.path import splitext

drawing = False
ix, iy = -1, -1
position_list = []

def draw_rectangle(image: np.ndarray, upper_left: tuple, bottom_right: tuple):
    colorA = image[upper_left[1]][upper_left[0]]
    colorB = image[bottom_right[1]][bottom_right[0]]

    result_image = image.copy()
    ##混合兩個角的顏色
    # result_image = cv2.rectangle(result_image, upper_left, bottom_right, color=(0, 0, 0), thickness=-1)

    # rectangle_mask = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

    # rectangle_shape = (bottom_right[1] - upper_left[1] + 1, bottom_right[0] - upper_left[0] + 1, 3)
    # colorA_matrix = np.full(rectangle_shape, colorA, dtype=np.uint8)
    # colorB_matrix = np.full(rectangle_shape, colorB, dtype=np.uint8)
    # A_probs = np.random.random(rectangle_shape)
    # B_probs = 1.0 - A_probs
    # rectangle = (colorA_matrix * A_probs + colorB_matrix * B_probs).astype(np.uint8)

    # rectangle_mask[upper_left[1]:bottom_right[1]+1, upper_left[0]:bottom_right[0]+1] = rectangle
    # result_image = cv2.bitwise_or(result_image, rectangle_mask)
    
    ##白色覆蓋
    result_image = cv2.rectangle(result_image, upper_left, bottom_right, color=(255, 255, 255), thickness=-1)
    return result_image

def get_positions(event, x, y, flags, param):
    global drawing, ix, iy, position_list, image, temp_image
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            image = temp_image.copy()
            cv2.rectangle(image, (ix, iy), (x, y), (0, 255, 0), 2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        print([[ix, iy], [x, y]])
        temp_image = draw_rectangle(temp_image, (ix, iy), (x, y))
        image = temp_image.copy()
        position_list.append([[ix, iy], [x, y]])

if __name__ == '__main__':
    path = 'sample/data_004.jpg'
    image = cv2.imread(path)
    temp_image = image.copy()
    cv2.namedWindow('get_position')
    cv2.setMouseCallback('get_position', get_positions)

    while True:
        cv2.imshow('get_position', image)
        key = cv2.waitKey(20) & 0xFF

        if key == ord('d'):
            print(position_list)
            path_and_name, suffix = splitext(path)
            image_rename = path_and_name + '_whiteout' + '.png'

            # 儲存框選座標
            with open(path_and_name + '_positions.txt', 'w') as f:
                f.write(str(position_list))

            # 儲存遮蔽圖片
            cv2.imwrite(image_rename, image)
            print(f"遮蔽圖片：{image_rename}")
            print(f"座標：{path_and_name + '_positions.txt'}")

        elif key == ord('x'):
            break

    cv2.destroyAllWindows()