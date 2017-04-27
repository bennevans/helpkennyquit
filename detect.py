
import numpy as np
import cv2
import pyscreenshot as ImageGrab
import time
import pyautogui

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

#returns an approximate location of the ball
def getBallLocation():
    return (425, 1300)

def getVector(start, end, offset, scal = 0.1):
    # hooptoballdist = end[1] - start[1]
    # sub =  
    return ((end[0] - start[0])*scal + offset, (end[1] - start[1])*scal)

def timeInAir(ball, y):
    print 'time', (ball[1] - y) * -10
    return (ball[1] - y)*-10 + 100000000

def shoot(ball, hoop, velocity):
    print 'shoot', ball, hoop, velocity
    offset = timeInAir(ball, hoop[1]) * velocity
    print 'offset', offset
    vec = getVector(ball, hoop, offset)

    ballx, bally = (550, 820)
    print 'moving'
    pyautogui.click(ballx, bally)
    time.sleep(0.2)
    print 'dragging'
    pyautogui.dragRel(vec[0], vec[1])
    print 'vec', vec

xprev = 0
tprev = 0

while True:
    im = ImageGrab.grab(bbox = (350, 170, 425, 700), childprocess=False)
    im = np.array(im)
    screen = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_RGB2BGR)

    hoop = detectHoop(screen)
    ball = getBallLocation()

    velocity = (hoop[0] - xprev) / (time.time() - tprev)

    print 'b,h,v', ball, hoop, velocity
    
    cv2.circle(screen, hoop, 40, (0,0,255), thickness=3)
    cv2.circle(screen, ball, 40, (0,0,255), thickness=3)

    height, width = screen.shape[:2]
    smaller = cv2.resize(screen, (width / 3, height / 3), interpolation=cv2.INTER_CUBIC)
    cv2.imshow('screen', smaller)

    k = cv2.waitKey(200) 

    if k & 0xFF == 27:
        break
    elif k & 0xFF == ord('s'):
        shoot(ball, hoop, velocity)

    xprev = hoop[0]

cv2.destroyAllWindows()



# cv2.circle(screen, hoop, 20, (0,0,255))
# cv2.circle(screen, ball, 20, (255,0,0))

# cv2.imshow('original', screen)
