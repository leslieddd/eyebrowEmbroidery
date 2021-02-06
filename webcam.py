import cv2
import os

def image_capture(name):
    camera_port = 0
    ramp_frames = 30
    camera = cv2.VideoCapture(camera_port)

    def get_image():
        retval, im = camera.read()
        return im

    for i in range(ramp_frames):
        temp = camera.read()
    camera_capture = get_image()

    face_detector = cv2.CascadeClassifier('haarcascade_profileface.xml')

    gray = cv2.cvtColor(camera_capture, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(camera_capture, (x, y), (x + w, y + h), (255, 0, 0), 2)


        dirname = "/Users/dongyirui/Desktop/eyebrows/main/static/main/customer"
        file_name = dirname + "/"
        cv2.imwrite(file_name + str(name) + ".jpg", camera_capture[y-50:y + h+50, x-50:x + w+50])





"""


     
def image_capture(name):
    def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    # face_id=input('enter your First Name: ')
    vid_cam = cv2.VideoCapture(0)

    face_detector = cv2.CascadeClassifier('haarcascade_profileface.xml')

    count = 0

    assure_path_exists("/Users/dongyirui/Desktop/eyebrows/main/static/main/customer")

    while (True):
        _, image_frame = vid_cam.read()
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            dirname = "/Users/dongyirui/Desktop/eyebrows/main/static/main/customer"
            file_name = dirname + "/"
            cv2.imwrite(file_name + str(name) + ".jpg", image_frame[y:y + h, x:x + w])
            cv2.imshow('frame', image_frame)

        key = cv2.waitKey(1)
        if key == ord('c'):
            break
        else:
            cv2.destroyAllWindows
    cv2.destroyAllWindows

"""

