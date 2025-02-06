import os
import time
import cv2

#Image from CSI camera
def img_csi():
  os.system("libcamera-still -o csi_img.jpg")
  
# Image from USB camera
def img_USB():
  cap = cv2.VideoCapture(0)
  
