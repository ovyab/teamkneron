import numpy as np
import skimage.io as io
from skimage.exposure import adjust_gamma
from skimage.transform import rotate, AffineTransform, warp
from skimage.util import random_noise
from skimage.filters import gaussian
from matplotlib import pyplot as plt

def augment():
    print('running...')
    image = io.imread('images/original.jpg')

    flip(image)
    noise(image)
    blur(image)
    darken(image)
    lighten(image)

    print('success')

def flip(image):
    flip = np.fliplr(image)
    plt.imsave('images/flipped.jpg',flip);

def noise(image):
    sigma = 0.155
    noise = random_noise(image, var=sigma**2)
    plt.imsave('images/noise.jpg',noise);

def blur(image):
    blur = gaussian(image, sigma=3, multichannel=True)
    plt.imsave('images/blurred.jpg',blur)

def darken(image):
    darken = adjust_gamma(image, gamma=3, gain=1)
    plt.imsave('images/darkened.jpg', darken)

def lighten(image):
    lighten = adjust_gamma(image, gamma=1/4, gain=1)
    plt.imsave('images/lightened.jpg', lighten)

if __name__ == "__main__":
    augment()