
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import time
import os
import HandTrackingModule as htm
import numpy as np
import math
 
wCam, hCam = 640, 480
cap1 = cv2.VideoCapture(1)
cap1.set(3, wCam)
cap1.set(4, hCam)
pTime = 0
 
detector1 = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model1/keras_model.h5", "Model1/labels.txt")
 
offset = 20
imgSize = 300
 
folder = "Data/C"
counter = 0
 
labels = ["A", "B", "C"]
 
while True:
    success1, img1 = cap1.read()
    img1 = detector1.findHands(img1)
    lmList = detector1.findPosition(img1, draw=False)
    # print(lmList)
 
    if len(lmList) != 0:
        fingers = []
 
        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
 
        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
 
        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)
 
 
        cv2.rectangle(img1, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img1, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
 
    cv2.putText(img1, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
 
    cv2.imshow("Imagee", img1)
    
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
 
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
 
        imgCropShape = imgCrop.shape
 
        aspectRatio = h / w
 
        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            print(prediction, index)
 
        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
 
        cv2.rectangle(imgOutput, (x - offset, y - offset-50),
                      (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        cv2.rectangle(imgOutput, (x-offset, y-offset),
                      (x + w+offset, y + h+offset), (255, 0, 255), 4)
 
 
        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)

        
    cv2.imshow("Image", imgOutput)
    cv2.waitKey(1)
    cv2.waitKey(1)
    
