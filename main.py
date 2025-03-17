#--------------------------------------- Author -----------------------------------------
# name          : Rizky Syarif Hidayatullah
# Phone         : +6285764374256
# Departement   : Mechatronic Engineering Education
#                 Yogyakarta State University
# Title Project : Sleep and Yawn Detection 
# Create        : 2022
#--------------------------------------- Library ----------------------------------------
import time
import sys
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import csv
import pyglet.media

cap =cv2.VideoCapture(0)

detector = FaceMeshDetector(maxFaces=1)

breakcount_s, breakcount_y = 0, 0
counter_s, counter_y = 0, 0
state_s, state_y = False, False

sound = pyglet.media.load("alarm.wav", streaming=False)

def alert():
    cv2.rectangle(img, (700, 20), (1250, 80), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, "DROWSINESS ALERT!!!", (710, 60),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img, faces = detector.findFaceMesh(img, draw=False)
    #print(len(faces[0]))
    if faces:
        face = faces[0]
        eyeLeft = [27, 23, 130, 243]  # up, down, left, right
        eyeRight = [257, 253, 463, 359]  # up, down, left, right
        mouth = [11, 16, 57, 287]  # up, down, left, right
        faceId = [27, 23, 130, 243, 257, 253, 463, 359, 11, 16, 57, 287]
        
        #calculate eye left distance ratio
        eyeLeft_ver, _ = detector.findDistance(face[eyeLeft[0]], face[eyeLeft[1]])
        eyeLeft_hor, _ = detector.findDistance(face[eyeLeft[2]], face[eyeLeft[3]])
        eyeLeft_ratio = int((eyeLeft_ver/eyeLeft_hor)*100)
        # calculate eye right distance ratio
        eyeRight_ver, _ = detector.findDistance(face[eyeRight[0]], face[eyeRight[1]])
        eyeRight_hor, _ = detector.findDistance(face[eyeRight[2]], face[eyeRight[3]])
        eyeRight_ratio = int((eyeRight_ver / eyeRight_hor) * 100)
        # calculate mouth distance ratio
        mouth_ver, _ = detector.findDistance(face[mouth[0]], face[mouth[1]])
        mouth_hor, _ = detector.findDistance(face[mouth[2]], face[mouth[3]])
        mouth_ratio = int((mouth_ver / mouth_hor) * 100)


        #display text on image
        #cv2.rectangle(img, (30,20), (400,150), (0,255,255), cv2.FILLED)
        cv2.putText(img, f'Eye Left Ratio: {eyeLeft_ratio}', (50, 60),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
        cv2.putText(img, f'Eye Right Ratio: {eyeRight_ratio}', (50, 80),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        cv2.putText(img, f'Eye Mouth Ratio: {mouth_ratio}', (50, 100),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

        #cv2.rectangle(img, (30, 200), (350, 300), (255,0,0), cv2.FILLED)
        cv2.putText(img, f'Sleep Count: {counter_s}', (40, 200),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
        cv2.putText(img, f'Yawn Count: {counter_y}', (40, 220),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

        #drowsiness detection logic

        #------------------------Eye-----------------------------
        if eyeLeft_ratio <= 50 and eyeRight_ratio <= 50:
            breakcount_s += 1
            if breakcount_s >= 10:
                alert()
                if state_s == False:
                    counter_s += 1
                    sound.play()
                    state_s = not state_s
        else:
            breakcount_s = 0
            if state_s:
                state_s = not state_s

        # ------------------------Mouth-----------------------------
        if mouth_ratio > 50:
            breakcount_y += 1
            if breakcount_y >= 10:
                alert()
                if state_y == False:
                    counter_y += 1
                    sound.play()
                    state_y = not state_y
        else:
            breakcount_y = 0
            if state_y:
                state_y = not state_y 


        for id in faceId:
            cv2.circle(img, face[id], 5, (0,255,0), cv2.FILLED)
        
        

    cv2.imshow("Image", img)
    cv2.waitKey(1)