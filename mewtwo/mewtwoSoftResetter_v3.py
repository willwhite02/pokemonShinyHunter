import time
import serial
import cv2
import numpy as np
import random

# set up capture card
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

# connect arduino
arduino = serial.Serial("COM7", 9600, timeout=1)
time.sleep(2)

numResets = 1795 # current reset counter
# I got it in 3849 resets with this code!
resetLength = 29 # in seconds

# average patch colors of normal and shiny
normal_avg = np.array([203.97916667, 121.97916667, 170.97916667]) # deep purple
shiny_avg  = np.array([66.90740741, 201.7962963, 146.40740741]) # weird nasty 2000's green

# get average color of a patch. we do a patch to be safe
def avg_patch_color(img, x1, y1, x2, y2):
    patch = img[y1:y2, x1:x2]
    return np.mean(patch, axis=(0, 1))  # BGR average

def color_distance(c1, c2):
    return np.linalg.norm(c1 - c2)

def arduino_send_reset():
    # left program button hits reset combo
    arduino.write(b"L")
    return

def arduino_press_A():
    # right program button presses A
    arduino.write(b"R")
    return

# wait AND show feed
def liveWait(cap, seconds):
    endTime = time.time() + seconds
    while time.time() < endTime:
        ret, frame = cap.read()
        cv2.imshow(f"Displaying feed from reset {numResets}...", frame)
        cv2.waitKey(1)

# sequence of inputs for reset sequence
def resetSequence(cap):
    cv2.destroyAllWindows()
    arduino_send_reset() # soft reset
    liveWait(cap, resetLength + random.uniform(0.0, 2.0)) # 30 seconds plus a bit for FR/LG
    arduino_press_A() # progress from title screen
    liveWait(cap, random.uniform(5.0, 10.0))
    arduino_press_A() # select save
    # get through recap screens and initially interact with mewtwo
    for screen in range(6):
        liveWait(cap, 2)
        arduino_press_A()
    # should have talked to mewtwo and chatbox is still onscreen
    liveWait(cap, random.uniform(8.0, 12.0)) 
    arduino_press_A()
    liveWait(cap, 8)

def testShiny(cap):
    # get average patch color of target area
    ret, frame = cap.read() # look at screen
    live_avg = avg_patch_color(frame, 935, 220, 950, 236) # target area is mewtwo's tail in the front
    normal_score = np.linalg.norm(live_avg - normal_avg)
    shiny_score = np.linalg.norm(live_avg - shiny_avg)
    return live_avg, normal_score, shiny_score

# keep loop going until we get the shiny
while True:
    live_avg, normal_score, shiny_score = testShiny(cap)
    # normal_score < shiny_score if deoxys not shiny
    if normal_score < shiny_score:
        numResets += 1
        print(f"Reset number {numResets}... last result {live_avg}") # show results
        resetSequence(cap)
    else:
        print(f"Shiny after {numResets} resets!")
        cv2.waitKey(0)
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()