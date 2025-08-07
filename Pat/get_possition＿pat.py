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
    result_image = cv2.rectangle(result_image, upper_left, bottom_right, color = (0, 0, 0), thickness = -1)
    rectangle_mask = np.zeros((image.shape[0], image.shape[1], 3), dtype = np.uint8)
    
    rectangle_shape = (bottom_right[1]-upper_left[1]+1, bottom_right[0]-upper_left[0]+1, 3)
    colorA_matrix = np.full(rectangle_shaep, colorA, dtype=np.uint8)
    colorB_matrix = np.full(rectangle_shape, colorB, dtype=np.uint8)
    A_probs = np.random.random(rectangle_shape)
    B_probs = np.ones(rectangle_shape) - A_probs
    rectangle = np.multiply(colorA_matrix, A_probs) + np.multiply(colorB_matrix, B_probs)
    
    rectangle_mask[upper_left[1]:bottom_right[1]+1, upper_left[0]:bottom_right[0]+1] = rectangle
    
    result_image = cv2.bitwise_or(result_image, rectangle_mask)
    return result_image
    
def get_positions(event, x, y, flage, param):
    global drawing, ix, iy, position_list, image, temp_image
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2. EVENT_MOUSEMOVE:
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
    path = 'sample/data_001.jpg'
    image = cv2.imread(path)
    temp_image = image.copy()
    cv2.nameWindow('get possition')
    cv2.setMouseCallback('get possition', get_positions)
    while(True):
        cv2.imshow('get possition', image)
        if cv2.waitKey(20) & 0xFF == ord('d'):
            print(positon_list)
            path_and_name, suffix = splitext(path)
            image__rename = path_and_name + '_whiteout' + '.png'
            ##collect information of positions
            with open(path_and_name + 'positions.txt', 'w') as position_file:
                position_file.write(str(position_list))
            ##save image with white out
            cv2.imwrite(image_rename, image)
        elif cv2.waitKey(20) & 0xFF == ord('x'):
            break
    cv2.destroyAllWindows()