import os
import imgaug as ia
from imgaug import augmenters as iaa
import scipy
import cv2
import numpy as np
import imageio
import csv
import pandas as pd
# optional check my hint import scipy.misc import imwrite
# optional check my hint import scipy.misc import imsave

def augment(name, folder):
    ia.seed(1)

    img = imageio.imread(name) #read you image
    print("Name: " + name)
    name2 = name[:-4]
    print("Name2: " + name2)


    images = np.array(
        [img for _ in range(6)], dtype=np.uint8)
    # 32 means creat 32 enhanced images using following methods.

    seq = iaa.Sequential([
        iaa.Fliplr(0.5), # horizontal flips
        iaa.Crop(percent=(0, 0.1)), # random crops
        # Small gaussian blur with random sigma between 0 and 0.5.
        # But we only blur about 50% of all images.
        iaa.Sometimes(0.5,
            iaa.GaussianBlur(sigma=(0, 0.5))
            
        ),

        iaa.Sometimes(0.2,
            iaa.imgcorruptlike.Brightness(severity=5)
        ),
        # Strengthen or weaken the contrast in each image.
        iaa.contrast.LinearContrast((0.75, 1.5)),
        # Add gaussian noise.
        # For 50% of all images, we sample the noise once per pixel.
        # For the other 50% of all images, we sample the noise per pixel AND
        # channel. This can change the color (not only brightness) of the
        # pixels.
        iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
        # Make some images brighter and some darker.
        # In 20% of all cases, we sample the multiplier once per channel,
        # which can end up changing the color of the images.
        iaa.Multiply((0.8, 1.2), per_channel=0.2),
        # Apply affine transformations to each image.
        # Scale/zoom them, translate/move them, rotate them and shear them.
        iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
            translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
            rotate=(-25, 25),
            shear=(-8, 8)
        )
    ], random_order=True) # apply augmenters in random order
    images_aug = seq.augment_images(images)

    for i in range(6):
        imageio.imwrite(name2 + str(i)+'new.jpg', images_aug[i])



for subdir, dirs, files in os.walk("."):
    for filename in files:
        filepath = subdir + os.sep + filename

        if filepath.endswith(".jpg"):
            print("Augmenting: " + filepath)
            f = filepath[8:10]
            #print(f)
            augment(filepath, f)

