import cv2 as cv
import numpy as np


img=cv.imread('Lab10_lane.jpg')
def canny(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    blur = cv.GaussianBlur(gray,(5, 5), sigmaX=0,sigmaY=0)
    canny = cv.Canny(blur, 50, 150)
    return canny

def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv.fillPoly(mask, polygons, 255)
    masked_image=cv.bitwise_and(image,mask)
    return masked_image

def make_coordinates(image, line_parameters):
    try:
        slope, intercept = line_parameters
    except TypeError:
        slope, intercept = 0.1, 0.1
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

#Image process
# canny=canny(img)
# ROI=region_of_interest(canny)
# lines = cv.HoughLinesP(ROI, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
# averaged_lines = average_slope_intercept(img, lines)
# line_image = display_lines(img, averaged_lines)
# combo_image = cv.addWeighted(img, 0.8, line_image, 1, 1)
#
# cv.imwrite('image_01_01.png',combo_image)
#
# cv.waitKey(0)
# cv.destroyAllWindows()

#Video process

cap = cv.VideoCapture('Lab10_test2.mp4')\

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

size = (frame_width, frame_height)
out = cv.VideoWriter('video_01_01.mp4',0x7634706d, 20, size,isColor=True)

while(cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv.addWeighted(frame, 0.8, line_image, 1, 1)
    cv.imshow('',combo_image)
    # out.write(combo_image)
    if cv.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
out.release()
