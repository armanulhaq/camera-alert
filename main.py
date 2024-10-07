import cv2
import os
import time
import glob
from send_email import send_email
from threading import Thread

video = cv2.VideoCapture(0) #Initializes the webcam (device 0 refers to the default webcam).
time.sleep(1) #Give the camera some time to settle

first_frame = None
status_list = []
count = 0

def clean_image_folder():
    print("Clean start")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("Clean finish")

while True:
    status = 0
    check, frame = video.read() #video.read() returns a tuple. Check shows last frame's status, frame is current frame captured by the webcam
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #We don't need the coloured frame for the comparision we are about to do. So we saving processing time. COLOR_BGR2GRAY is the algorithm used
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21,21), 0) # The frame will be blurred a bit as we don't need that much precision and performance is more important. (21,21) is the blur value and 0 is the standard deviation which is generally kept 0

    if first_frame is None: # it is a way of preserving first frame for the purpose of comparison at later stage
        # We check if 'first_frame' is None because we only want to set it once at the beginning of the video feed.
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    threshold_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1] #Any value above 30 will be 255 and ideally rest of the frame should be black. So we test different values and ended up on 60
    dil_frame = cv2.dilate(threshold_frame, None, iterations=2) #it helps in making the white areas (which represent motion) more visible and connected, eliminating small noise or gaps.
    cv2.imshow("My video", threshold_frame) #Displays the frames in a window titled "My video"

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Find all the contours in the frame, i.e., the outline of the new objects in the frame

    for contour in contours:
        if cv2.contourArea(contour) < 15000: #If the new object is of the size less than 10k pixel, it's mostly a fake object detected due to change in lighting condition
            continue
        x, y, w, h = cv2.boundingRect(contour) #extract the edges and the width
        rectangle = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3) # make a (0,255,0) (green) coloured rectangle of width 3
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            image_with_object = all_images[int(len(all_images)/2)]


    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True
        #send_email(image_with_object) #The frames hang when the object leaves the frame. So we introduced Threading
        clean_thread = Thread(target=clean_image_folder)
        clean_thread.daemon = True

        email_thread.start()

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1) #Waits for 1 millisecond (loop is also for 1 millisecond each) and saves the key pressed in key variable

    if key == ord("q"): # Converts 'q' to its ASCII value
        break

video.release()
clean_thread.start()
clean_thread.join()  # Wait for the cleaning thread to finish before exiting
