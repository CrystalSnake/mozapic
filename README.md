# mozapic

The program takes an image as input, processes it and produces a grid for a mosaic of specified colors.

_Requires Python 3.12.0 or higher._

## Before run

`pip install -r requirements.txt`

Copy your image in the program directory.

The image should be:

- named image.jpg (jpg format is required)
- approximately 2x3, 2x2 or 3x2 aspect ratio.
- it is advisable that the main part of the image of the ball is more contrasting than the background.

You can add or remove color from palette in the colors.py file. Color must be in RGB color space.
In settings.py you can define mosaic grid size `brick_qty`. Default 24px x 2 (2x3, 2x2 or 3x2 squares).

## Run

`Run file main.py in console`

After processing, the program will create a new image in its directory with the name
image\_{current date and time}.jpg and will output to the console a matrix with the color numbers for the assembly, with a legend and the number of pixels of each color.
