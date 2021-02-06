import cv2
import numpy as np
import dlib
from math import hypot
import argparse
import imutils

def put_that_eyebrow(dirname, eyebrowpath, name):
    # Loading Camera and Brow image and Creating mask
    brow_image = cv2.imread(eyebrowpath)

    rows, cols, _ = brow_image.shape
    brow_mask = np.zeros((rows, cols), np.uint8) #返回来一个给定形状和类型的用0填充的数组

    # Loading Face detector
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # load the input image, resize it, and convert it to grayscale
    image = cv2.imread(dirname)
    # image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale image
    rects = detector(gray, 1)

    brow_mask.fill(0)

    # faces = detector(frame)
    for face in rects:
        landmarks = predictor(gray, face)

        # brow coordinates
        top_brow = (landmarks.part(24).x, landmarks.part(24).y)
        center_brow = (((landmarks.part(22).x + landmarks.part(24).x + landmarks.part(26).x)/3), 
                        ((landmarks.part(22).y + landmarks.part(24).y + landmarks.part(26).y)/3)) #重心
        # center_brow = (landmarks.part(24).x, landmarks.part(24).y)
        left_brow = (landmarks.part(22).x, landmarks.part(22).y)
        right_brow = (landmarks.part(26).x, landmarks.part(26).y)

        middle_nose = (landmarks.part(29).x, landmarks.part(29).y)  #鼻梁中间

        brow_width = int(hypot(left_brow[0] - right_brow[0],
                            left_brow[1] - right_brow[1]) * 1) # sqrt(x*x + y*y)
        brow_height = int(brow_width * 0.3)

        # New brow position ***
        top_left = (int(center_brow[0] - brow_width / 2),
                                int(center_brow[1] - brow_height / 2))
        bottom_right = (int(center_brow[0] + brow_width / 2),
                        int(center_brow[1] + brow_height / 2))

        # Adding the new brow
        eyebrow = cv2.resize(brow_image, (brow_width, brow_height))
        eyebrow_gray = cv2.cvtColor(eyebrow, cv2.COLOR_BGR2GRAY)
        _, brow_mask = cv2.threshold(eyebrow_gray, 25, 255, cv2.THRESH_BINARY_INV)   ###阀值




        ##########################
        browarea_mask_黑眉毛 = image[0::, 0::]  ###阀值
        browarea_mask_黑眉毛[0::, 0::] = 0
        browarea_mask_黑眉毛[top_left[1] - 10: top_left[1] + brow_height - 7,
        top_left[0]: top_left[0] + brow_width] = 255

        cv2.imwrite("/Users/dongyirui/PycharmProjects/换脸/存图/" + " browarea_mask_黑眉毛.jpg", browarea_mask_黑眉毛)

        img = cv2.imread(dirname)  # input
        mask = cv2.imread('/Users/dongyirui/PycharmProjects/换脸/存图/ browarea_mask_黑眉毛.jpg', 0)  # mask

        dst_NS = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)

        ###黑眉毛
        image2 = dst_NS
        brow_area黑 = image2[top_left[1]: top_left[1] + brow_height, top_left[0]: top_left[0] + brow_width]
        brow_area_no_brow黑 = cv2.bitwise_and(brow_area黑, brow_area黑, mask=brow_mask)

        brow_area_no_brow黑 = cv2.GaussianBlur(brow_area_no_brow黑, (3, 3), 0)

        eyebrow = cv2.GaussianBlur(eyebrow, (3, 3), 0)
        final_brow黑_add对比 = cv2.add(eyebrow, brow_area_no_brow黑)



        final_brow黑_add对比 = cv2.GaussianBlur(final_brow黑_add对比, (3, 3), 0)
        image2[top_left[1]: top_left[1] + brow_height,
        top_left[0]: top_left[0] + brow_width] = final_brow黑_add对比


        ############################






        break



    cv2.imwrite("/Users/dongyirui/Desktop/eyebrows/main/static/main/eyebrow/" + name + "_eyebrow.jpg", image2)