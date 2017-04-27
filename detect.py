
import numpy as np
import cv2


def detectHoop(screen):
    hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

    lower_orange = np.array([25, 100, 100])
    upper_orange = np.array([30, 255, 255])

    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    edges = cv2.Canny(mask, 50, 150, apertureSize = 3)

    lines = cv2.HoughLines(edges, 1, np.pi/180, 100)

    xmin = 1000000
    xmax = 0
    ymin = 1000000
    ymax = 0

    if lines is not None:
        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = int(a*rho)
            y0 = int(b*rho)

            if x0 > 0 and x0 < xmin:
                xmin = x0
            if x0 > xmax:
                xmax = x0

            if y0 > 0 and y0 < ymin:
                ymin = y0
            if y0 > ymax:
                ymax = y0

    return ((xmin + xmax) / 2, (ymin + ymax) / 2)

screen = cv2.imread('screengrab.png')

hoop = detectHoop(screen)

print 'hoop', hoop

cv2.circle(screen, hoop, 20, (0,0,255))
cv2.imshow('original', screen)

k = cv2.waitKey(0)

if k == 27:
    cv2.destroyAllWindows()
