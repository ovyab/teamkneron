import os, scipy, cv2, imageio
import imgaug as ia
from imgaug import augmenters as iaa
import numpy as np

ia.seed(1)

img = imageio.imread("original.jpg") #demo image

images = np.array(
    [img for _ in range(32)], dtype=np.uint8)

  # creates 32 enhanced images using the methods below:

seq = iaa.Sequential([
    iaa.Fliplr(0.5), # horizontal flips

    iaa.Crop(percent=(0, 0.1)), # random crops

    # motion blur with a kernel size of 15x15 pixels and a blur angle of either -45 or 45 degrees
    iaa.Sometimes(0.5,
        iaa.MotionBlur(k=15, angle=[-45, 45])
    ),

    # strengthen or weaken contrast
    iaa.contrast.LinearContrast((0.75, 1.5)),

    # gaussian noise
    iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),

    # make some images brighter, some darker
    iaa.Multiply((0.8, 1.2), per_channel=0.2),

    # randomly make some images super bright
    iaa.Sometimes(0.2, iaa.imgcorruptlike.Brightness(severity=4)),

    # affine transformations; scale/zoom, translate/move, rotate, and shear
    iaa.Affine(
        scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
        translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
        rotate=(-25, 25),
        shear=(-8, 8)
    )
], random_order=True) #apply augmenters in random order

images_aug = seq.augment_images(images)

for i in range(32):
    imageio.imwrite(str(i)+'new.jpg', images_aug[i])  #write all changed images