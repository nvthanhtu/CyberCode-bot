import os
from turtle import color
from cv2 import threshold
import pyautogui as ag
import cv2 as cv
import numpy as np

screen_shot_img = cv.imread('Image/Screenshot.png', cv.IMREAD_UNCHANGED)
nearby_enemy_img = cv.imread('Image/Nearby_Enemy.png', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(screen_shot_img, nearby_enemy_img, cv.TM_CCORR_NORMED)

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

print('Best match loc: %s,%s'% (str(max_loc), str(min_loc)))
print('Match confidence: %s' %max_val)


threshold = 0.8
if max_val >= threshold:
    
    nearby_w = nearby_enemy_img.shape[1]
    nearby_h = nearby_enemy_img.shape[0]
    
    
    top_left = max_loc
    bottom_right = (top_left[0]+nearby_w, top_left[1]+nearby_h)
    
    cv.rectangle(screen_shot_img, top_left, bottom_right, color=(0,255,0), thickness=2, lineType=cv.LINE_4)
    cv.imshow('Result', screen_shot_img)
    cv.waitKey()