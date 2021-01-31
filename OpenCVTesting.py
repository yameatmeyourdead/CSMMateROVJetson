# from PIL import Image, ImageFilter, ImageOps
import cv2
import time
import numpy as np
# CHAPTER 5
def empty(a):
    pass
# winName = "TrackBars"
# cv2.namedWindow(winName)
# cv2.resizeWindow(winName, 640, 240)
# cv2.createTrackbar("Hue Min", winName, 0, 179, empty)
# cv2.createTrackbar("Hue Max", winName, 179, 179, empty)
# cv2.createTrackbar("Sat Min", winName, 0, 255, empty)
# cv2.createTrackbar("Sat Max", winName, 255, 255, empty)
# cv2.createTrackbar("Val Min", winName, 0, 255, empty)
# cv2.createTrackbar("Val Max", winName, 255, 255, empty)
# img = cv2.imread("test.png")
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
while 1:
    success, img = cap.read()
    cv2.imshow("video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # h_min = cv2.getTrackbarPos("Hue Min", winName)
    # h_max = cv2.getTrackbarPos("Hue Max", winName)
    # s_min = cv2.getTrackbarPos("Sat Min", winName)
    # s_max = cv2.getTrackbarPos("Sat Max", winName)
    # v_min = cv2.getTrackbarPos("Val Min", winName)
    # v_max = cv2.getTrackbarPos("Val Max", winName)
    # lower = np.array([h_min, s_min, v_min])
    # upper = np.array([h_max, s_max, v_max])
    #
    # mask = cv2.inRange(imgHSV, lower, upper)
    mask_white = cv2.inRange(imgHSV, np.array([0, 0, 200]), np.array([179, 100, 255]))
    mask_pink = cv2.inRange(imgHSV, np.array([150, 70, 0]), np.array([179, 230, 255]))
    # to get the full pipe system (which we will need), add these i guess? unless anyone has any better ideas
    # cv2.imshow("Original", img)
    # cv2.imshow("HSV", imgHSV)
    # cv2.imshow("Mask", mask)
    cv2.imshow("white mask", mask_white)
    cv2.imshow("pink mask", mask_pink)
    #time.sleep(1)
    cv2.waitKey(1)
# CHAPTER 4 - shapes and colors and such
#
# img = np.zeros((512, 512, 3), np.uint8)
# img[:] = 255, 0, 0                                # WHOLE IMAGE
# img[200:300, 100:200]= 255, 0, 0                    # part of image
# cv2.line(img, (100, 200), (500, 300), (0, 0, 255), 3)     # draw line on image
# cv2.rectangle(img, (200, 100), (400, 400), (0, 255, 0), 10)
# cv2.circle(img, (300, 200), 30, (255, 255, 255), 3)
# cv2.putText(img, "Hello, world!", (5, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 0, 255), 1)
#
# cv2.imshow("Original", img)
#
# cv2.waitKey(0)
# CHAPTER 3 - resizing and cropping
# img = cv2.imread("test.png")
# print(img.shape)
#
# imgResized = cv2.resize(img,(2000, 400))
# print(imgResized.shape)
#
# imgCropped = img[200:800, 500:1000]
#
# cv2.imshow("Original", img)
# cv2.imshow("Resized", imgResized)
# cv2.imshow("Cropped", imgCropped)
#
# cv2.waitKey(0)
# CHAPTER 2 - filters
# img = cv2.imread("test.png")
#
# kernel = np.ones((5, 5), np.uint8)
#
# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# imgBlur = cv2.GaussianBlur(img, (15,15),0)
# imgCanny = cv2.Canny(img, 50, 50)
# imgDilation = cv2.dilate(imgCanny, kernel, iterations=1)
# imgEroded = cv2.erode(imgDilation, kernel, iterations=1)
#
# cv2.imshow("Original", img)
# cv2.imshow("Gray", imgGray)
# cv2.imshow("Blur", imgBlur)
# cv2.imshow("Canny", imgCanny)
# cv2.imshow("Dilate", imgDilation)
# cv2.imshow("Erode", imgEroded)
# cv2.waitKey(0)
# CHAPTER 1 - video/img/webcam
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
#
# while True:
#     success, img = cap.read()
#     cv2.imshow("video", img)
#     if cv2.waitKey(1) & 0xFF ==ord('q'):
#         break