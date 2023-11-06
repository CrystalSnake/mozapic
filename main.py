"""
Takes an image as input, processes it and produces a grid for a mosaic of specified colors.
"""
import sys
import os
import time
import numpy as np
from PIL import Image
from colors import palette
from settings import min_size, brick_size


colors_list = []
mosaic_map = []

def cls():
    """Function clear console."""
    os.system('cls' if os.name == 'nt' else 'clear')


def create_list_of_colors():
    """
    Creates a list of color dictionaries based on the `palette` (list) variable.
    
    Each dictionary contains an ID, RGB color code, and quantity.
    
    Example Usage:
    create_list_of_colors()
    
    Inputs:
    - None
    
    Outputs:
    - None
    """
    for i in enumerate(palette):
        color = {'id': i[0] + 1,
            'color_code_rgb': i[1],
            'qty': 0}
        colors_list.append(color)


def color_counter(list_of_colors_with_qty, color_code):
    """
    Counts the number of occurrences of a specific color code in a list of colors.

    Args:
        list_of_colors_with_qty (list): A list of dictionaries containing 
        color codes and their quantities.
        color_code (list): A list representing the RGB values of a color.

    Returns:
        None. The `colors_list` is modified in-place with the quantity 
        value updated for the matching color code.
    """
    for c in list_of_colors_with_qty:
        if color_code == c['color_code_rgb']:
            c['qty'] += 1


def fill_mosaic_map(colors, color_code):
    """
    Appends the ID of a given color code in the `colors` to the `mosaic_map` list.
    
    Args:
        colors (list): A list of color codes.
        color_code (str): A color code to be added to the `mosaic_map`.
    
    Returns:
        None
    """
    mosaic_map.append(colors.index(list(color_code)) + 1)


def print_mosaic_matrix(mosaic_pixels, height):
    """
    Prints the mosaic matrix and the colors legend.

    Args:
    - mosaic_pixels: A list of lists representing the mosaic pixels, 
    where each inner list contains the RGB values of a pixel.
    - height: An integer representing the height of the mosaic matrix.

    Returns:
    - None
    """
    matrix = [[] for _ in range(height)]
    i = 0
    for pixel in mosaic_pixels:
        matrix[i].append(pixel)
        if i < height - 1:
            i += 1
        else:
            i = 0
    cls()
    print("Color matrix")
    print(*matrix, sep="\n")
    print("Colors legend")
    print(*colors_list, sep="\n")


# open desired image
def open_image(path_to_file):
    """
    Opens an image file and returns the opened image object.

    Args:
        path_to_file (str): The path to the image file.

    Returns:
        PIL.Image.Image: The opened image object.

    Raises:
        FileNotFoundError: If the file is not found.

    Example:
        image = open_image("path/to/image.jpg")
        print(image)
    """
    try:
        img = Image.open(path_to_file)
        return img
    except FileNotFoundError:
        print("File not found =(")
        sys.exit()

# find its width & height
def check_image_min_size(image, image_min_size):
    """
    Check if the width and height of an image are greater than a specified minimum size.

    Args:
        image (PIL Image object): The image to be checked.
        image_min_size (int): The minimum size that the width or height of the image should be.

    Returns:
        list: The width and height of the image as a list.

    Raises:
        SystemExit: If the width or height of the image is less than 
        the minimum size, the function will print "Image too small. 
        Minimum size on the short side min_size pixels." and exit the program.
    """
    w, h = image.size
    if w < image_min_size or h < image_min_size:
        print(f"Image too small. Minimum size on the short side {min_size} pixels.")
        sys.exit()
    else:
        return [w, h]


def check_image_aspect_ratio(width, height):
    """
    Checks the aspect ratio of an image and determines the crop width and height based on the ratio.

    Args:
        width (int): The width of the image.
        height (int): The height of the image.

    Returns:
        list: A list containing the crop width and height.

    Raises:
        SystemExit: If none of the conditions for aspect ratio are met.

    Example:
        width = 800
        height = 600
        result = check_image_aspect_ratio(width, height)
        print(result)
    """
    if 0.63 < height/width < 0.7:
        crop_w = int(np.round(min_size/(2/3)))
        crop_h = min_size
    elif 0.63 < width/height < 0.7:
        crop_w = min_size
        crop_h = int(np.round(min_size/(2/3)))
    elif height == width:
        crop_w = crop_h = min_size
    else:
        print("Wrong image ratio")
        sys.exit()
    return [crop_w, crop_h]


# find closest color from palette for replace image pixel color
def closest(colors, color):
    """
    Returns the color from the list that is closest to the target color.

    Args:
        colors (list): A list of colors represented as tuples of RGB values.
        color (tuple): The target color represented as a tuple of RGB values.

    Returns:
        tuple: The closest color from the `colors` list to the target `color`.
    """
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2, axis=1))
    index_of_smallest = np.where(distances == np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return tuple(smallest_distance[0])


def replace_colors_of_image_to_palette(image):
    """
    Replaces the colors of an image with the closest color from a predefined palette.

    Args:
        image (PIL Image): The input image to be processed.

    Returns:
        None. The function modifies the input image by replacing its 
        colors with the closest colors from the palette.
    """
    pixels = image.load()  # create the pixel map
    create_list_of_colors()
    for i in range(image.size[0]):  # for every pixel:
        for j in range(image.size[1]):
            # change pixel color to palette
            color_replace = closest(palette, pixels[i, j])
            color_counter(colors_list, list(color_replace))
            fill_mosaic_map(palette, color_replace)
            pixels[i, j] = color_replace

def mosaic():
    """
    Creates a mosaic image from an input image file.

    This function opens the input image file, checks the size and aspect 
    ratio of the image, resizes the image, replaces the colors with 
    the closest colors from a predefined palette, and saves the resulting mosaic image.

    Inputs:
    - None

    Outputs:
    - None
    """

    image = open_image('./image.jpg')
    w, h = check_image_min_size(image, min_size)
    crop_w, crop_h = check_image_aspect_ratio(w, h)
    crop_img = image.resize((crop_w, crop_h), resample=None,
        box=None, reducing_gap=None)
    # find NEW dimensions from user-defined number (50% for example)
    new_w = crop_w * brick_size
    new_h = crop_h * brick_size
    # round to nearest whole number and convert from float to int
    new_w = int(np.round(new_w))
    new_h = int(np.round(new_h))
    # downsample image to these new dimensions
    down_sampled = crop_img.resize((new_w, new_h))
    replace_colors_of_image_to_palette(down_sampled)
    # upsample back to original size (using "4" to signify bicubic)
    up_sampled = down_sampled.resize((crop_w, crop_h), resample=4)
    # save the image
    timestr = time.strftime('%Y%m%d%H%M%S')
    up_sampled.save('./image_' + timestr + '.jpg')
    print("Success!")
    # print mosaic matrix
    print_mosaic_matrix(mosaic_map, new_h)


if __name__== "__main__":
    mosaic()
