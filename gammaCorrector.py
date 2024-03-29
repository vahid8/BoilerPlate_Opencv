#!/usr/bin/env python
""" Evaluate the brightness and contrast and
    improve it
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import tqdm



__author__ = "vahid jani"
__copyright__ = "Copyright 2021"
__credits__ = ["Vahid jani"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Vahid jani"
__email__ = "aghajanivahid1@gmail.com"
__status__ = "Development"

def plot_histogram(image,show=False):
    # calculate mean value from RGB channels and flatten to 1D array
    pixel_values = image.ravel()
    pixel_values = pixel_values[pixel_values!=0]
    pixel_values = pixel_values[pixel_values<250]
    mean_pixel = np.mean(pixel_values)
    if show:
        std = np.std(pixel_values)
        print("mean {}, std {}".format(mean,std))
        plt.hist(pixel_values, 256, [0, 256])
        plt.show()
    return mean_pixel

def adjust_gamma(image, gamma=1.0):
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
	return cv2.LUT(image, table) # apply gamma correction using the lookup table


if __name__ == '__main__':
    input_dir = "camera 1"
    output_dir = "det"
    images = [item for item in os.listdir(input_dir) if item.endswith(".jpg")]
    for item in tqdm.tqdm(images):
        img = cv2.imread(os.path.join(input_dir, item))
        mean = plot_histogram(img)
        gamma_value = round((100-int(mean))/10, 1)
    
        if gamma_value>2.2: # we dont want to make the image brighter than this
            gamma_value = 2.2

        if gamma_value > 1.0: # in the current project we only have dark images to be brighter. needs to be changed for specific projects
            new_image = adjust_gamma(img, gamma_value)
            cv2.imwrite(os.path.join(output_dir, item), new_image)
