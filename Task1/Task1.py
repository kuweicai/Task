# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 23:22:57 2019

@author: Alvin Chen
"""

import cv2
import numpy as np
#from matplotlib import pyplot as plt

#load image
#img = cv2.imread('E:\CV_20190331\Task1\Sudoku.jpg', 1)
img = cv2.imread('.\Sudoku.jpg', 1)

#convert color img to gray img
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#blur
img_blur = cv2.medianBlur(img_gray, 3)
img_blur = cv2.GaussianBlur(img_blur, (3, 3), 0)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
close = cv2.morphologyEx(img_blur, cv2.MORPH_CLOSE, kernel)
div = np.float32(img_blur) / close
img_brightness_adjust = np.uint8(cv2.normalize(div, div, 0, 255, cv2.NORM_MINMAX))

#threshold
img_thresh = cv2.adaptiveThreshold(img_brightness_adjust, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 7)

img_, contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)

#find max contours
max_area = 0
biggest_contour = None
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > max_area:
        max_area = area
        biggest_contour = cnt


#mask
mask = np.zeros(img_brightness_adjust.shape, np.uint8)
cv2.drawContours(mask, [biggest_contour], 0, 255, cv2.FILLED)
cv2.drawContours(mask, [biggest_contour], 0, 0, 2)
image_with_mask = cv2.bitwise_and(img_brightness_adjust, mask)

#transform
pts_src = np.float32([ [71,34],[34,461],[516,468],[488,18] ])
pts_dst = np.float32([ [25,25],[25,425],[425,425],[425,25] ])
M = cv2.getPerspectiveTransform(pts_src,pts_dst)
dst = cv2.warpPerspective(image_with_mask,M,(450,450))

cv2.imshow('img', img)
cv2.imshow('img4', dst) 
cv2.waitKey()