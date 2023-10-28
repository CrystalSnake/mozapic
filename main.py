from PIL import Image
import numpy as np
import sys
from colors import list_of_colors
from settings import min_size, brick_size


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

crop_img = img.resize((min_size, min_size), resample=None,
                      box=None, reducing_gap=None)
crop_w, crop_h = crop_img.size
# find NEW dimensions from user-defined number (50% for example)
new_w = crop_w * brick_size
new_h = crop_h * brick_size
# round to nearest whole number and convert from float to int
new_w = np.round(new_w)
new_w = int(new_w)
new_h = np.round(new_h)
new_h = int(new_h)
# downsample image to these new dimensions
down_sampled = crop_img.resize((new_w, new_h))


# find closest color from palette for replace image pixel color
def closest(colors, color):
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2, axis=1))
    index_of_smallest = np.where(distances == np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return smallest_distance


pixels = down_sampled.load()  # create the pixel map

for i in range(down_sampled.size[0]):  # for every pixel:
    for j in range(down_sampled.size[1]):
        # change pixel color to palette
        color_replace = closest(list_of_colors, pixels[i, j])
        pixels[i, j] = tuple(color_replace[0])


# upsample back to original size (using "4" to signify bicubic)
up_sampled = down_sampled.resize((crop_w, crop_h), resample=4)
# save the image
up_sampled.save('./new_image.jpg')
print("Success!")
