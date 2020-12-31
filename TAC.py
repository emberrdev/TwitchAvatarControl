
from fer import FER
from fer import Video
import cv2
import pprint
import os
import numpy as np
import msvcrt
import time

# Emotions trained:
# amgry, disgust, fear, happy, sad, surprise, neutral

DEBUG = False

path = r'D:\\Users\\Aden\Desktop\\Twitch Avatar Control'
avatar_path = path + r'\\emotions'
neutralState = "happy"

detector = FER()

cap = cv2.VideoCapture(0)
windowTitle = 'Twitch Avatar Control'

# TODO:
# Make copy of results array with each emotion having a value
# Using the values of the results, every 2nd or so frame lerp the values
# Introduce inbetween states (i.e. happy1, happy2, happy3 for 0.33, 0.66, 0.99)


def detectEmotion(filename):

    img = cv2.imread(path + '\\' + filename)

    if(img.size == 0):
        return 0

    result = detector.detect_emotions(img)

    if(DEBUG):
        print(result)

    # get top emotion
    if(len(result) != 0):
        emotion, amount = detector.top_emotion(img)

        return emotion

    return "none"

def getAvatarImages():
    for f in avatar_path:
        if(f.endswith(".png") or (f.endswith(".jpg"))):
            avatar_images.append(f)

def showAvatarState(emotion):
    img = None
    for filename in os.listdir(avatar_path):
        ext = os.path.splitext(filename)[-1].lower()
        if(ext == ".png" or ext == ".jpg"):
            if(filename.startswith(emotion)):
                img = cv2.imread(avatar_path + '\\' + filename, 1)
            elif(emotion == "none"):
                img = cv2.imread(avatar_path + '\\' + neutralState + ext, 1)

    print("Current Emotion: " + emotion)
    if (img.size != 0):
        cv2.imshow(windowTitle, img)



while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Save frame as image
    img_name = "opencv-frame-capture.png"
    cv2.imwrite(img_name, frame)

    # Detect emotion in image
    currentEmotion = detectEmotion(img_name)

    # Display the corresponding image
    showAvatarState(currentEmotion)

    # Display the resulting frame
    #cv2.imshow(windowTitle, frame)


    if (cv2.waitKey(250) & 0xFF) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

