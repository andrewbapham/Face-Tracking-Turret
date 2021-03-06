import cv2
import sys
import logging as log
import datetime as dt
import time
import pyfirmata
import numpy

cascPath = "C:/Users/Andrew/Documents/Big Brain Project/haarcascade_eye_tree_eyeglasses.xml"
eyeCascade = cv2.CascadeClassifier(cascPath)
# Makes log file
log.basicConfig(filename='webcam.log',level=log.INFO)

# 0 is main webcam, 1 is laptop cam, 2 is droidcam
video_capture = cv2.VideoCapture(1)
anterior = 0

startTime = time.time()
endingTime = time.time()
elapsedTime = 0

def shootFace():
    while True:
        cascPath2 = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath2)
        ret, frame = video_capture.read()

        # Convert to grayscale
        gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray2,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draws rectangle around eyes
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            print("Position is: " + str((x+w)/2))
            print(x)
            print(w)


        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            video_capture.release()
            cv2.destroyAllWindows()
        


while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        time.sleep(5)
        pass

    # Captures frames from camera
    ret, frame = video_capture.read()

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    eyes = eyeCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draws rectangle around eyes
    for (x, y, w, h) in eyes:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Writes to log file when eyes are detected
    if anterior != len(eyes):
        anterior = len(eyes) 
        log.info("faces: "+str(len(eyes))+" at "+str(dt.datetime.now()))
        startTime = time.time()

    if len(eyes) == 0:
        elapsedTime = endingTime - startTime
        if elapsedTime > 2:
            print("eyes closed for 2 seconds")
            shotTime = time.time()
            shootFace()
            startTime = time.time()
        endingTime = time.time()
    


    # shows video feed in window
    cv2.imshow('Video', frame)

    # Close program with q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Releases camera
video_capture.release()
cv2.destroyAllWindows()