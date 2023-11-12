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


mosaic_map = []

def cls():
    """Function clear console."""
    os.system('cls' if os.name == 'nt' else 'clear')


def brightness(color):
    """
    Calculate the brightness of a color by summing up the RGB values.

    Args:
        color (tuple): A tuple representing the RGB values of a color.

    Returns:
        int: The brightness value of the color.

    Example Usage:
        >>> color = (255, 128, 0)
        >>> brightness_value = brightness(color)
        >>> print(brightness_value)
        383
    """
    return sum(color[1])

def create_list_of_colors(image):
    """
    Creates a list of color based on the `palette` (list) variable.
    
    Each dictionary contains a tuple with RGB color code for original and replace color, id and quantity for each color.
    
    Example Usage:
    create_list_of_colors()
    
    Inputs:
    - None
    
    Outputs:
    - None
    """
    colors_list = []
    origin_colors = image.getcolors()
    sorted_origin_colors = sorted(origin_colors, key=brightness)
    used_colors = []
    id = 1
    for c in sorted_origin_colors:
        replace_colors = closest(palette, c[1])
        for rc in replace_colors:
            if rc in used_colors:
                continue
            else:
                color = (c[1], tuple(rc), id, c[0]) #(original color, replace color, id, quantity)
                colors_list.append(color)
                used_colors.append(rc)
                id += 1
                break
    print(colors_list)
    return colors_list


def print_mosaic_matrix(mosaic_pixels, height, list_of_colors):
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
    for color in list_of_colors:
        color_id = color[2]
        color_code = color[1]
        color_qty = color[3]
        print(f'ID: {color_id} - color: {color_code} qty: {color_qty}')


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


def quantize_image(image, n):
    """
    Converts the input image to a quantized image with a reduced color palette.

    Args:
        image (PIL.Image.Image): The input image to be quantized.
        n - desired number of colors on image

    Returns:
        PIL.Image.Image: The quantized image with a reduced color palette.
    """
    result_image = image.convert("P").quantize(colors=n, dither=Image.Dither.FLOYDSTEINBERG)
    return result_image

def closest(colors, color):
    """
    Returns a list of colors from the input list that are closest to the target color.

    Args:
        colors (list): A list of RGB color tuples.
        color (tuple): The target RGB color tuple.

    Returns:
        list: A list of RGB color tuples from the `colors` list that 
        are closest to the `color` tuple.
    """
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2, axis=1))
    data = list(zip(colors, distances))
    sorted_data = sorted(data, key=lambda x: x[1])
    color_values = [color[0].tolist() for color in sorted_data]
    return color_values


def replace_colors_of_image_to_palette(image, list_of_colors):
    """
    Replaces the colors of an image with the closest color from a predefined palette.

    Args:
        image (PIL Image): The input image to be processed.

    Returns:
        None. The function modifies the input image by replacing its 
        colors with the closest colors from the palette.
    """
    pixels = image.load()  # create the pixel map
    for i in range(image.size[0]):  # for every pixel:
        for j in range(image.size[1]):
            # change pixel color to palette
            for c in list_of_colors:
                if pixels[i, j] == c[0]:
                    pixels[i, j] = c[1]
                    mosaic_map.append(c[2])

def mosaic(path_to_file):
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

    image = open_image(path_to_file)
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
    low_colors_image = quantize_image(down_sampled, len(palette)).convert( mode = 'RGB' )
    list_of_colors = create_list_of_colors(low_colors_image)
    replace_colors_of_image_to_palette(low_colors_image, list_of_colors)
    # upsample back to original size (using "4" to signify bicubic)
    up_sampled = low_colors_image.resize((crop_w, crop_h), resample=4)
    # save the image
    timestr = time.strftime('%Y%m%d%H%M%S')
    up_sampled.save('./image_' + timestr + '.jpg')
    print("Success!")
    print_mosaic_matrix(mosaic_map, new_h, list_of_colors)


if __name__== "__main__":
    mosaic('./image.jpg')
