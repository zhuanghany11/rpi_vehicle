import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

while True:
    start_time = time.time()
    ret, frame = cap.read()
    frame_hough = frame.copy()
	
    # By Houghcircle detection
    # blurred = cv2.pyrMeanShiftFiltering(frame, 10, 100)
    # cv2.imshow('blurred', blurred)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_color = np.array([100, 43, 46])       #red 0, blue 100
    upper_color = np.array([124, 255, 255])     #red 10, blue 124
    mask_hsv = cv2.inRange(hsv, lower_color, upper_color)
    # element = cv2.getStructuringElement(cv2.MORPH_ERODE, (5, 5))
    # mask_hsv = cv2.erode(mask_hsv, element)
    mask_component = np.zeros_like(mask_hsv, dtype=np.uint8)
    # mask_hsv = cv2.dilate(mask_hsv, element)
    # cv2.imshow('mask_hsv', mask_hsv)

    circles = None
    confidence = []
    num_label, label_img, stats, centroids = cv2.connectedComponentsWithStats(mask_hsv, connectivity=8)
    for (label, stat, centroid) in zip(range(0, num_label+1), stats, centroids):
        area_component = stat[cv2.CC_STAT_AREA]
        if area_component < 5000 or label == 0:
            continue
        else:
            component = np.zeros_like(mask_hsv, dtype=np.uint8)
            component[label_img == label] = 1

            image, contours, hierarchy = cv2.findContours(component.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
            x_centroid, y_centroid = centroid
            (x_enclose, y_enclose), r_enclose = cv2.minEnclosingCircle(contours[0])
            area_enclose = int(np.pi * r_enclose * r_enclose)
            # print(area_component, str(area_enclose))
            detected_circle = np.array([int(x_enclose), int(y_enclose), int(r_enclose)])
            circles = np.vstack([circles, detected_circle]) if circles is not None else [detected_circle]
            # print(x_centroid, y_centroid, area_component,x_enclose ,y_enclose, area_enclose)
            # print(x_centroid.__class__, y_centroid.__class__, area_component.__class__, x_enclose.__class__, y_enclose.__class__, area_enclose.__class__)
            confidence.append(np.abs(area_component - area_enclose) + (x_centroid - x_enclose) ** 2 + (y_centroid - y_enclose) ** 2)
            mask_component = mask_component + component
    if circles is not None:
        print(confidence)
        idx = confidence.index(min(confidence))
        #for c in circles[idx]:
        c = circles[idx]
        cv2.circle(frame_hough, (c[0], c[1]), c[2], (0, 255, 255), 2)
    cv2.putText(frame_hough, "FPS {0:.5f}".format(1 / (time.time() - start_time)), (10, 400), 1, 2, (255, 255, 255))
    mask_component = cv2.cvtColor(mask_component*255, cv2.COLOR_GRAY2BGR)
    cv2.imshow('hough', np.hstack([frame_hough, mask_component]))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
