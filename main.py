import cv2
import mss
import face_recognition
import numpy as np
import time
from PIL import Image
import simpleaudio as sa

Sean = face_recognition.load_image_file("Sean.jpg")
Sean_encoding = face_recognition.face_encodings(Sean)[0]
Sean_loc = face_recognition.face_locations(Sean)

my_sound = sa.WaveObject.from_wave_file("Is it True Yes lalala.wav")
last_played = 0
cooldown = 30


sct = mss.mss()
info_monitor = sct.monitors[1]
monitor = {"top": info_monitor["top"], "left": info_monitor["left"], "width": 1500, "height": 1230}

while True:
    screenshare = sct.grab(monitor)
    img = np.array(screenshare)
    screenshare_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    location = face_recognition.face_locations(screenshare_bgr)
    encoding = face_recognition.face_encodings(screenshare_bgr, location)

    for (face_encoding, (top, right, bottom, left)) in zip(encoding, location):
        match = face_recognition.compare_faces([Sean_encoding], face_encoding)
        if match[0]:
            name = "Sean"
            color = (0, 255, 0)
            if time.time() - last_played > cooldown:
                play_sound = my_sound.play()
                last_played = time.time()
        else:
            name = "Unknown"
            color = (0, 0, 255)

        cv2.rectangle(screenshare_bgr, (left, top), (right, bottom), color, 2)
        cv2.putText(screenshare_bgr, name, (right, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    cv2.imshow("Screenshare", screenshare_bgr)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()




