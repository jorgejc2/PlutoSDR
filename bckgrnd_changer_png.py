"""
Very basic code to change background of PNG color and save as JPG image. 

Goal 1 (easy): enable input to take an image and a color (DONE)

Goal 2 (easy): create an input option so that if a folder path instead of an image is given,
a color is applied to every PNG image in the folder (DONE)

Goal 3 (medium and tedious): create tkinter GUI and allow ability to drag and drop images and get user input

Goal 4 (hard): Obtain a raspberry pi and run as a backend server and give a compilation of scripts it can 
run. Once set up, add parameters to its API that makes it use the functionality of this script to create 
API calls so that an image with configurations can be given to this script, and a JPG image is returned
"""

from PIL import Image
import argparse
import os

if __name__ == "__main__":

    """ obtain arguments """
    parser = argparse.ArgumentParser(description='Process user RGB inputs and PNG files.')
    parser.add_argument('-path', type=str, required=True, help='Enter a file or directory path to your PNG or collection of PNG images')
    parser.add_argument('-color', type=str, default='255,255,255', help='Insert an RGB value in the format (int),(int),(int). The default color is white or 255,255,255.')

    """ parse arguments and initialization """
    args = parser.parse_args()

    path = args.path
    if not os.path.exists(path):
        raise ValueError('Please enter a valid path to your image or directory')

    color = args.color
    rgb = [int(x) for x in color.split(',',2)]
    if len(rgb) != 3:
        raise ValueError('Please enter an RGB value in the specified format')

    save_directory = os.getcwd() + '/converted_png_images' # directory where final PNG images will be saved
    os.makedirs(save_directory, exist_ok=True)  # create the directory

    if not path.endswith('.png'):
        """ directory path was given """
        for root, dirs, files in os.walk(path, topdown=False):
            for img_name in files:
                if img_name.endswith('.png'):
                    im = Image.open(os.path.join(root, img_name))
                    fill_color = (rgb[0],rgb[1],rgb[2])  # your new background color

                    im = im.convert("RGBA")   # it had mode P after DL it from OP
                    if im.mode in ('RGBA', 'LA'):
                        background = Image.new(im.mode[:-1], im.size, fill_color)
                        background.paste(im, im.split()[-1]) # omit transparency
                        im = background

                    new_img_name = str(img_name.split('.', 1)[0] + '.jpg')  # format image to .jpg
                    im.convert("RGB").save(os.path.join(save_directory, new_img_name))

    else:
        """ file path was given """
        im = Image.open(path)
        img_name = os.path.basename(path)  # get name of the image

        fill_color = (rgb[0],rgb[1],rgb[2])  # your new background color

        im = im.convert("RGBA")   # it had mode P after DL it from OP
        if im.mode in ('RGBA', 'LA'):
            background = Image.new(im.mode[:-1], im.size, fill_color)
            background.paste(im, im.split()[-1]) # omit transparency
            im = background

        new_img_name = str(img_name.split('.', 1)[0] + '.jpg')  # format image to .jpg
        im.convert("RGB").save(os.path.join(save_directory, new_img_name))