import numpy as np
import cv2
import imutils
import dlib
import argparse

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image")
# args = vars(ap.parse_args())

def golden_ratio(dirname, name):
    img = cv2.imread(dirname)
    # img = cv2.imread('sample_face01.jpg', 1)
    img = imutils.resize(img, width=500) #指定缩放后的width，则会根据比例计算缩放后的height

    detector = dlib.get_frontal_face_detector() #默认的人脸检测器
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") #标记人脸关键点

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale image
    rects = detector(gray, 1)

    # loop over the face detections
    for (i, rect) in enumerate(rects):
        landmarks = predictor(gray, rect)
        # points of interest
        ##1
        right_nostril = landmarks.part(34).x, landmarks.part(34).y
        ntl = landmarks.part(34).x, landmarks.part(22).y
        ##2
        rightnose_corner = landmarks.part(35).x, landmarks.part(35).y
        righteye_corner = landmarks.part(45).x, landmarks.part(45).y
        ##3
        iris1 = landmarks.part(43).x, landmarks.part(43).y
        iris2 = landmarks.part(46).x, landmarks.part(46).y
        x = landmarks.part(43).x + landmarks.part(46).x
        y = landmarks.part(43).y + landmarks.part(46).y
        iris = int(x / 2), int(y / 2)
        middle_nose = landmarks.part(33).x, landmarks.part(33).y
        ###

        img = cv2.circle(img, (landmarks.part(45).x, landmarks.part(45).y), 2, (255, 255, 255), 2)
        img = cv2.circle(img, (landmarks.part(33).x, landmarks.part(33).y), 2, (255, 255, 255), 2)
        img = cv2.circle(img, (landmarks.part(34).x, landmarks.part(34).y), 2, (255, 255, 255), 2)
        img = cv2.circle(img, (landmarks.part(35).x, landmarks.part(35).y), 2, (255, 255, 255), 2)
        img = cv2.circle(img, iris, 2, (255, 255, 255), 2)
        ###
        slo = ((landmarks.part(35).y - landmarks.part(45).y) / (landmarks.part(45).x - landmarks.part(35).x))
        xright = (landmarks.part(35).y - landmarks.part(22).y) / slo + landmarks.part(35).x
        sloiris = (landmarks.part(33).y - y / 2) / (x / 2 - landmarks.part(33).x)
        xmiddle = (landmarks.part(33).y - landmarks.part(25).y) / sloiris
        # golden ratio virtual lines
        img = cv2.line(img, (right_nostril), (ntl), (255, 255, 255), 1)
        img = cv2.line(img, (rightnose_corner), (int(xright), landmarks.part(22).y), (255, 255, 255), 1)
        img = cv2.line(img, (int(landmarks.part(33).x + xmiddle), landmarks.part(25).y), (middle_nose), (255, 255, 255),
                       1)

        cv2.imwrite("/Users/dongyirui/Desktop/eyebrows/main/static/main/PostSim/" + name + "_postsim.jpg", img)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    """# determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        # shape = predictor(gray, rect)
        # shape = face_utils.shape_to_np(shape)

        landmarks = predictor(gray, rect)
        
        righteye_corner = landmarks.part(26).x, landmarks.part(26).y
        rightnose_corner = landmarks.part(35).x, landmarks.part(35).y
        topbrow = landmarks.part(24).x, landmarks.part(24).y
        innerbrow = landmarks.part(22).x, landmarks.part(22).y
        middle_nose = landmarks.part(33).x, landmarks.part(33).y
        right_nostril = landmarks.part(34).x, landmarks.part(34).y
        righteye_inner = landmarks.part(42).x, landmarks.part(42).y

        #points of interest
        cv2.circle(img, topbrow, 2, (0, 0, 255), 2)
        cv2.circle(img, innerbrow, 2, (0, 0, 255), 2)
        cv2.circle(img, righteye_corner, 2, (0, 0, 255), 2)
        cv2.circle(img, rightnose_corner, 2, (0, 0, 255), 2)

        # golden ratio virtual lines
        img = cv2.line(img, (rightnose_corner), (righteye_corner), (0, 255, 0), 2)
        img = cv2.line(img, (rightnose_corner), (topbrow), (0, 255, 0), 2)
        img = cv2.line(img, (rightnose_corner), (innerbrow), (0, 255, 0), 2)"""