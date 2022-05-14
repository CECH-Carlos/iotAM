#!/usr/bin/python 
#-*- coding: utf-8 -*-
import gtts
from playsound import playsound
import pytesseract
import cv2

cap = cv2.VideoCapture(0)

while True:
    res, frame = cap.read()

    if not res:
        break

    #* Your code here.

    #* Show result
    cv2.imshow('iot AM', frame)

    #* Wait for key 'ESC' to quit
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

#* That's how you exit
cap.release()
cv2.destroyAllWindows()
