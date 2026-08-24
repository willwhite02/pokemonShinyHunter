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

numResets = 93 # current reset counter
# I got it in 234 resets with this code!
resetLength = 30 # in seconds

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

def display_top_right_corner():
    ret, frame = cap.read() # look at screen
    crop = frame[0:360, 640:1280] # crop to get only the pokemon in the view
    cv2.imshow(f"Displaying image from reset {numResets}...", crop) # show the pokemon as a sanity check
    cv2.waitKey(1) # keeps image up
    return

def display_full_screen():
    ret, frame = cap.read()
    #crop = frame[0:360, 640:1280]
    cv2.imshow(f"Displaying image from reset {numResets}...", frame)
    cv2.waitKey(1)
    return

# keep loop going until we get the shiny
while True:
    # here is where we test if the pokemon is shiny
    display_top_right_corner()

    # get average patch color of target area
    ret, frame = cap.read() # look at screen
    crop = frame[0:360, 640:1280] # crop to get only the pokemon in the view
    live_avg = avg_patch_color(frame, 935, 220, 950, 236) # target area is mewtwo's tail in the front
    normal_score = np.linalg.norm(live_avg - normal_avg)
    shiny_score = np.linalg.norm(live_avg - shiny_avg)
    # normal_score < shiny_score if deoxys not shiny
    if normal_score < shiny_score:
        numResets += 1
        print(f"Reset number {numResets}... last result {live_avg}") # show screen
        arduino_send_reset() # start reset sequence
        cv2.destroyAllWindows() # delete picture
        # next loop presses A at 'correct' times in spirit of RNG manipulation
        for second in range(resetLength):
            display_full_screen()
            time.sleep(1)
            cv2.destroyAllWindows()
        # now we start pressing A at random intervals. we are at title screen
        time.sleep(random.uniform(0.5, 2.0))
        arduino_press_A() # title screen -> save select
        display_full_screen()
        time.sleep(random.uniform(7.5, 10.0))
        arduino_press_A() # save select -> recap screens
        time.sleep(2)
        cv2.destroyAllWindows()
        display_full_screen()
        # this loop moves through all the recap screens and interact with mewtwo and get chat box
        for screen in range(6):
            arduino_press_A()
            cv2.destroyAllWindows()
            display_full_screen()
            time.sleep(2)
        # now we are in game standing in front of mewtwo
        cv2.destroyAllWindows()
        display_full_screen()
        # time.sleep(4) # last recap window takes a second to go down
        # arduino_press_A() # interact with mewtwo
        # cv2.destroyAllWindows()
        # display_full_screen()
        time.sleep(random.uniform(5.0, 10.0))
        arduino_press_A() # go from chat to battle
        for second in range(7): # give time for battle to start
            #arduino_press_A()
            cv2.destroyAllWindows()
            display_full_screen()
            time.sleep(1)
        cv2.destroyAllWindows()
        # now we can test if mewtwo is shiny and restart the loop
        
    else:
        print(f"Shiny after {numResets} resets!")
        cv2.waitKey(0)
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()