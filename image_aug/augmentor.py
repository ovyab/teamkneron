import os, scipy, imageio
import imgaug as ia
from imgaug import augmenters as iaa
import numpy as np
import pandas as pd

def main():

    ia.seed(1)
    numAugs = 4;

    img = imageio.imread("original.jpg") #demo image

    images = np.array(
        [img for _ in range(numAugs)], dtype=np.uint8)

    # creates 32 enhanced images using the methods below:

    seq = iaa.Sequential([
        iaa.Fliplr(0.5), # horizontal flips
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
    ], name="img_augmentation", random_order=True) #apply augmenters in random order

    images_aug = seq.augment_images(images)

    for i in range(numAugs):
        imageio.imwrite('/results/' + str(i)+'new.jpg', images_aug[i])  #write all changed images

def test():
    df_train = pd.read_csv('driver_imgs_list.csv', low_memory=True)
    print('Number of samples in data set : {}'.format(df_train.shape[0]))
    print('Number of classes : {}'.format(len((df_train.classname).unique())))

if __name__ == "__main__":
    test()