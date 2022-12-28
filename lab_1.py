import cv2
import numpy as np
import os


# img1 = cv2.imread('/Users/danna_fely/Documents/картиночки/devushka_pantsir_zajts_167320_2560x1600.jpg', 33)
#
# cv2.namedWindow('Display window', cv2.WINDOW_GUI_NORMAL)
# cv2.imshow('Display window', img1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

def print_video():
    cap = cv2.VideoCapture('/Users/danna_fely/Downloads/2022-09-17 11.50.31.mp4', cv2.CAP_ANY)
    while True:
        ret, frame = cap.read()
        if not(ret):
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(16) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


# print_video()
def readIPWriteTOFile():
    video = cv2.VideoCapture('https://192.168.82.101:8080')
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter("output.mov", fourcc, 60, (w, h))
    while True:
        ok, img = video.read()
        cv2.imshow('img', img)
        video_writer.write(img)
        if cv2.waitKey(16) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()


readIPWriteTOFile()

def print_cam():
    cap = cv2.VideoCapture(1)
    cap.set(3, 640)
    cap.set(4, 480)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

vcap = cv2.VideoCapture("rtsp://admin:admin@192.168.213.62:1935/camera", cv2.CAP_FFMPEG)
while True:
    ret, frame = vcap.read()
    if ret == False:
        print("Frame is empty")
        break
    else:
        cv2.imshow('VIDEO', frame)
        cv2.waitKey(33)
# //https://medium.com/beesightsoft/opencv-python-connect-to-android-camera-via-rstp-9eb78e2903d5
# //Change “192.168.1.2” to your android device address



