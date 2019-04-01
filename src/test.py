import cv2
import numpy as np
import time
from gpiozero import Servo

cap = cv2.VideoCapture(0)
width, height = cap.get(3), cap.get(4)
print(width, height)
# cap.set(cv2.CAP_PROP_FPS, 15)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width // 2)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height // 2)
# print(cap.get(3), cap.get(4))

fps = cap.get(cv2.CAP_PROP_FPS)
servo_io = 18

servo = Servo(servo_io, min_pulse_width=0.45/1000,max_pulse_width=2.3/1000)
found = 0

while True:
	start_time = time.time()
	
	ret, frame = cap.read()

	# By Houghcircle detection
	# blurred = cv2.pyrMeanShiftFiltering(frame, 10, 100)
	# cv2.imshow('blurred', blurred)
	
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_color = np.array([100, 0, 0])  # red 0, blue 100, organe 11
	upper_color = np.array([180, 255, 255])  # red 10, blue 124, organe 25
	mask_hsv = cv2.inRange(hsv, lower_color, upper_color)
	# element = cv2.getStructuringElement(cv2.MORPH_ERODE, (5, 5))
	# mask_hsv = cv2.erode(mask_hsv, element)
	mask_component = np.zeros_like(mask_hsv, dtype=np.uint8)
	# mask_hsv = cv2.dilate(mask_hsv, element)
	# cv2.imshow('mask_hsv', mask_hsv)

	circles = None
	confidence = []

	num_label, label_img, stats, centroids = cv2.connectedComponentsWithStats(mask_hsv, connectivity=8)
	
	for (label, stat, centroid) in zip(range(0, num_label + 1), stats, centroids):
		area_component = stat[cv2.CC_STAT_AREA]
		if area_component < 5000 or label == 0:
			continue
		else:
			component = np.zeros_like(mask_hsv, dtype=np.uint8)
			component[label_img == label] = 1

			image, contours, hierarchy = cv2.findContours(component.copy(), mode=cv2.RETR_EXTERNAL,
														  method=cv2.CHAIN_APPROX_SIMPLE)
			x_centroid, y_centroid = centroid
			(x_enclose, y_enclose), r_enclose = cv2.minEnclosingCircle(contours[0])
			area_enclose = int(np.pi * r_enclose * r_enclose)
			# print(area_component, str(area_enclose))
			detected_circle = np.array([int(x_enclose), int(y_enclose), int(r_enclose)])
			circles = np.vstack([circles, detected_circle]) if circles is not None else [detected_circle]
			# print(x_centroid, y_centroid, area_component,x_enclose ,y_enclose, area_enclose)
			# print(x_centroid.__class__, y_centroid.__class__, area_component.__class__, x_enclose.__class__, y_enclose.__class__, area_enclose.__class__)
			if abs(area_enclose / area_component - 1) < 1:
				confidence.append(np.abs(area_component - area_enclose) + (x_centroid - x_enclose) ** 2 + (
						y_centroid - y_enclose) ** 2)
			else:
				confidence.append(None)
			mask_component = mask_component + component
	if circles is not None:
		print(confidence)
		if len(set(confidence)) >= 1:
			idx = confidence.index(min(confidence))
			# for c in circles[idx]:
			c = circles[idx]
			cv2.circle(frame, (c[0], c[1]), c[2], (0, 255, 255), 2)
			cv2.circle(frame, (c[0], c[1]), 2, (0, 0, 255), 2)
			print('circle found at:', c[0], ', ', c[1])
		else:
			pass
			# print('no circle shape detected')
	# cv2.putText(frame, "frame time: {0:.5f}".format(1/(time.time() - start_time)), (10, 40), 1, 1, (255, 255, 255))
	print(1/(time.time() - start_time))
	mask_component = cv2.cvtColor(mask_component * 255, cv2.COLOR_GRAY2BGR)
	cv2.imshow('frame', frame)
	cv2.imshow('mask', mask_component)
	time1 = time.time()
	if cv2.waitKey(1) & 0xFF == ord('q'):
		print(time.time() - time1)
		break

cap.release()
cv2.destroyAllWindows()
