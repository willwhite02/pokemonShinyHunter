import time
import serial
import cv2
import numpy as np

# set up capture card
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

# connect arduino
arduino = serial.Serial("COM7", 9600, timeout=1)
time.sleep(2)

numResets = 0 # current reset counter
# I got it in 5102 resets with this code!

# average patch colors of normal and shiny
normal_avg = np.array([235.75324675, 231.83116883, 224.90909091]) # almost white
shiny_avg  = np.array([157.34313725, 225.7254902, 254.27124183]) # gold
battle_button_avg = np.array([[77.96865889, 65.48760933, 191.75145773]])

# get average color of a patch. we do a patch to be safe
def avg_patch_color(img, x1, y1, x2, y2):
    patch = img[y1:y2, x1:x2]
    return np.mean(patch, axis=(0, 1))  # BGR average

def color_distance(c1, c2):
    return np.linalg.norm(c1 - c2)

def arduino_connect_controller():
    # sends connect controller signal to leo
    arduino.write(b"c")
    time.sleep(2)
    return

def arduino_send_reset():
    # sends reset signal this computer -> uno -> leo. leo handles reset
    arduino.write(b"r")
    return

def arduino_press_A():
    # tells leo to press A
    arduino.write(b"a")
    return

# wait AND show feed
def liveWait(cap, seconds):
    endTime = time.time() + seconds
    while time.time() < endTime:
        ret, frame = cap.read()
        cv2.imshow(f"Displaying feed from reset {numResets}...", frame)
        cv2.waitKey(1)

def battle_menu_visible(frame):
    targetArea = avg_patch_color(frame, 1120, 432, 1168, 459) # area where battle menu option is
    # returns true if sufficiently close
    return np.linalg.norm(targetArea - battle_button_avg) < 5

# sequence of inputs for reset sequence
def resetSequence(cap):
    cv2.destroyAllWindows()
    arduino_send_reset() # soft reset
    liveWait(cap, 4) # wait 4 seconds for reset sequence to complete
    arduino_press_A() # select BDSP on home menu
    liveWait(cap, 1)
    arduino_press_A() # select user, game starts loading
    """
    liveWait(cap, 25)
    arduino_press_A() # skip opening credits, end up at title screen
    liveWait(cap, 4)
    arduino_press_A() # progress from title screen
    liveWait(cap, 11.5)
    arduino_press_A() # interact with uxie
    liveWait(cap, 2.5)
    arduino_press_A() # progresses from dialogue with uxie, battle actually starts
    liveWait(cap, 18)
    """
    last_press = time.time()
    while True:
        ret, frame = cap.read()
        # Look for the battle menu
        if battle_menu_visible(frame):
            break
        # Press A every 2 seconds
        arduino_press_A()
        liveWait(cap, 2)

def testShiny(cap):
    # get average patch color of target area
    ret, frame = cap.read() # look at screen
    live_avg = avg_patch_color(frame, 830, 523, 840, 529) # target area is chest
    normal_score = np.linalg.norm(live_avg - normal_avg)
    shiny_score = np.linalg.norm(live_avg - shiny_avg)
    return live_avg, normal_score, shiny_score

# connect controller
# arduino_connect_controller()

# initial reset
numResets += 1
print(f"Reset number {numResets}... last result {normal_avg}") # show results
resetSequence(cap)

# keep loop going until we get the shiny
while True:
    live_avg, normal_score, shiny_score = testShiny(cap)
    # normal_score < shiny_score if deoxys not shiny
    if normal_score < shiny_score:
        numResets += 1
        print(f"Reset number {numResets}... last result {live_avg}") # show results
        resetSequence(cap)
    else:
        #ret, frame = cap.read()
        #cv2.imwrite("capture_test.png", frame)
        print(f"Shiny after {numResets} resets! {live_avg}")
        cv2.waitKey(0)
        break

"""
# get picture if needed
resetSequence(cap)
ret, frame = cap.read()
cv2.imwrite("capture_test.png", frame)
"""

cap.release()
arduino.close()
cv2.destroyAllWindows()