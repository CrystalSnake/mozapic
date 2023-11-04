from PIL import Image
import numpy as np
import sys
import os
import time
from colors import list_of_colors
from settings import min_size, brick_size


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


cls()


colors_list = []
for i in enumerate(list_of_colors):
    color = {'id': i[0] + 1,
             'color_code_rgb': i[1],
             'qty': 0}
    colors_list.append(color)


def pixel_counter(colors_list, color_code):
    for color in colors_list:
        if color_code == color['color_code_rgb']:
            color['qty'] += 1


# open desired image
try:
    img = Image.open('./image.jpg')
except FileNotFoundError:
    print("File not found =(")
    sys.exit()

# find its width & height
w, h = img.size
if w < min_size or h < min_size:
    print("Image too small")
    sys.exit()


def mosaic(img):
    # Checking the aspect ratio of the image to select a mode
    if 0.63 < h/w < 0.7:
        crop_w = int(np.round(min_size/(2/3)))
        crop_h = min_size
    elif 0.63 < w/h < 0.7:
        crop_w = min_size
        crop_h = int(np.round(min_size/(2/3)))
    elif h == w:
        crop_w = crop_h = min_size
    else:
        print("Wrong image ratio")
        sys.exit()
    crop_img = img.resize((crop_w, crop_h), resample=None,
                          box=None, reducing_gap=None)
    # find NEW dimensions from user-defined number (50% for example)
    new_w = crop_w * brick_size
    new_h = crop_h * brick_size
    # round to nearest whole number and convert from float to int
    new_w = int(np.round(new_w))
    new_h = int(np.round(new_h))
    # downsample image to these new dimensions
    down_sampled = crop_img.resize((new_w, new_h))

    pixels = down_sampled.load()  # create the pixel map

    for i in range(down_sampled.size[0]):  # for every pixel:
        for j in range(down_sampled.size[1]):
            # change pixel color to palette
            color_replace = closest(list_of_colors, pixels[i, j])

            pixel_counter(colors_list, list(color_replace))
            pixels[i, j] = color_replace

    # upsample back to original size (using "4" to signify bicubic)
    up_sampled = down_sampled.resize((crop_w, crop_h), resample=4)
    # save the image
    timestr = time.strftime('%Y%m%d%H%M%S')
    up_sampled.save('./image_' + timestr + '.jpg')
    print("Success!")


# find closest color from palette for replace image pixel color
def closest(colors, color):
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2, axis=1))
    index_of_smallest = np.where(distances == np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return tuple(smallest_distance[0])


mosaic(img)
print(*colors_list, sep="\n")
