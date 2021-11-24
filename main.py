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

# 0 is default webcam
video_capture = cv2.VideoCapture(0)
anterior = 0

#Replace COM port and pins with whatever your hardware is connected on
serPort = 'COM5'
pinX = 'd:9:s'
pinY = 'd:7:s'
pinShoot = 'd:8:s'


board = pyfirmata.Arduino('COM5')
servoX = board.get_pin(pinX)
servoY = board.get_pin(pinY)
servoShoot = board.get_pin(pinShoot)

startTime = time.time()
endingTime = time.time()
elapsedTime = 0

def shootFace():
    shotInitTime = time.time()
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
            print("y position is: " + str((x)))
            print(numpy.interp((y), [90, 200], [65, 80]))
            servoX.write(numpy.interp((x+w)/2, [90, 305], [115, 55]))
            servoY.write(numpy.interp((y), [80, 200], [65, 80]))

        if (time.time()-shotTime) >= 4:
            servoShoot.write(140)
            if time.time() - shotInitTime > 10:
                return

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            video_capture.release()
            cv2.destroyAllWindows()
        

servoX.write(80)
servoY.write(72.50)
servoShoot.write(120)
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
        servoShoot.write(120)

    if len(eyes) == 0:
        elapsedTime = endingTime - startTime
        if elapsedTime > 5:
            shotTime = time.time()
            shootFace()
            startTime = time.time()
            servoShoot.write(120)
        endingTime = time.time()
    


    # shows video feed in window
    cv2.imshow('Video', frame)

    # Close program with q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Releases camera
video_capture.release()
cv2.destroyAllWindows()

