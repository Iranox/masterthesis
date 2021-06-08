import cv2
import numpy as np
import os


"""It has mainly three parts.

    Image pre-processing
    segmentation and feature extraction
    recognition

In case of Image pre-processing , you have to undergo the image through different processes to remove noises, for skew-correction and binarization.
It mainly involves gray scale conversion, different noise removal techniques (like median filtering, spatial filtering) and binarization.

In case of segmentation and feature extraction also you can apply any algorithm suitable for you.

In case of recognition, you can use SVM or Neural Networks.

    """

import cv2
from matplotlib import pyplot as plt
image = cv2.imread("/home/iranox/Projects/lehrer-schueler-beziehung/workbench/copy_checker/test_zeugnisse/Testtemplate.jpg")
#image = cv2.resize(image, (image.shape[1]*2, image.shape[0]*2))
image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
image_gray_filter = cv2.medianBlur(image_gray, 3) # gut gegen Salt-Paper-Noise


image2 = cv2.imread("/home/iranox/Projects/lehrer-schueler-beziehung/Daten/Ressources/Zeugnisse/00006000/00006031.jpg")
#image = cv2.resize(image, (image.shape[1]*2, image.shape[0]*2))
image_gray2 = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
image_gray_filter2 = cv2.medianBlur(image_gray2, 3) # gut gegen Salt-Paper-Noise

sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(image_gray_filter,None)
kp2, des2 = sift.detectAndCompute(image_gray_filter2,None)
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)
#matches = sorted(matches, key = lambda x:x.distance)
good = []
for m,n in matches:
    if m.distance < 0.8*n.distance:
        good.append([m])

# cv2.drawMatchesKnn expects list of lists as matches.
img3 = cv2.drawMatchesKnn(image,kp1,image2,kp2,good,None,flags=2)


plt.imshow(img3),plt.show()
