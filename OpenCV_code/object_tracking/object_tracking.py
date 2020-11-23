"""Tracking d'objet avec OpenCV"""

import cv2
import sys
import os; os.chdir(r"C:\Users\Armand\Dropbox\ISEP\a1\AIR\Sandbox\OpenCV\object_tracking")

def track(video_path, tracker_type, bbox, gui=False):
    print("tracker_type: {}".format(tracker_type))
    def create_tracker():
        if tracker_type == "BOOSTING":
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == "MIL":
            tracker = cv2.TrackerMIL_create()
        if tracker_type == "KCF":
            tracker = cv2.TrackerKCF_create()
        if tracker_type == "TLD":
            tracker = cv2.TrackerTLD_create()
        if tracker_type == "MEDIANFLOW":
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == "GOTURN":
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == "MOSSE":
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()
        return tracker

    tracker = create_tracker()

    # Read video
    video = cv2.VideoCapture(video_path)

    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print("Cannot read video file")
        sys.exit()

    # if gui:
    #     # Uncomment the line below to select a different bounding box
    #     bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    tracker.init(frame, bbox)

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)
        print("bbox: {}".format(bbox))

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw bounding box
        if ok:
            if gui:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        if gui:
            # Display tracker type on frame
            cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

            # Display result
            cv2.imshow("Tracking", frame)

            # sleep(.1)
            # os.system('pause')

            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break


video_path = "video.mp4"
video = cv2.VideoCapture(video_path)
status, frame = video.read()
if status:
    cv2.imwrite("frame.jpg", frame)
else:
    print("Could not load video first frame")

cX, cY = 355, 390  # coordonnées du centre de l'objet à tracker sur la première image de la vidéo
radius = 60  # moitié de la longueur du côté du cadre initial qu'on choisit autour de l'objet à tracker
bbox = (cX-radius, cY-radius, 2*radius, 2*radius)  # définition du cadre initial

tracker_types = ["BOOSTING", "MIL", "KCF", "TLD", "MEDIANFLOW", "GOTURN", "MOSSE", "CSRT"]
tracker_type = tracker_types[7]  # choisir un algorithme de tracking; KCF et CSRT semble bien fonctionner

track(video_path, tracker_type, bbox, gui=True)
