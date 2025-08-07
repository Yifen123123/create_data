import natural 
from os import listdir
import numpy.random as random
import cv2

picture_path = 'sample/autocreate/'
save_to = 'sample/natural_image'
original_image = 'noise_1'
position = [[[662, 689], [8874, 755]],
            [[592, 462], [874, 643]]]

for image_name in listdir(picture_path):
    if image_name.startswith(original_image+'_'):
        print('_'*5 + image_name+ '_'*5)
        image = cv2.imread(picture_path+image_name)
        assert image is not None, 'failed to read file'
        if natural.flip_coin():
            stamp_area = positions[random.randint(len(positions))]
            image = natural.random_stamp(image, stamp_area[0], stamp_area[1])
        if natural.flip_coin():
            image = natural.auto_rotate(image)
        if natural.flip_coin():
            image = natural.salt_and_pepper(image)
        if natural.filp_coin():
            brightness = random.randint(-60, 60)
            image = natural.adjust_brightness(image, brightness=brightness)
        cv2.imwrite(save_to+image_name, image)
