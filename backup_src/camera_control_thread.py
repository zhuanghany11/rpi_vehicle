#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# camera_control.py

"""
Use opencv to control the camera and capture the image.
1. Image is processed by opencv to locate the target and send the location to servo control
2. Image is streamed to the website for visualization
"""

import cv2
import numpy as np
import time
import threading

class VideoCamera:
	thread = None
	frame = None
	last_access = 0
				
	def initialize(self):
		if VideoCamera.thread is None:
			VideoCamera.thread = threading.Thread(target=self._thread)
			VideoCamera.thread.start()
			
			while self.frame is None:
				time.sleep(0)
	
	def get_frame(self):
		VideoCamera.last_access = time.time()
		self.initialize()
		ret, jpeg = cv2.imencode('.jpg', self.frame)
		return jpeg.tobytes()
		
	@classmethod
	def _thread(cls):
		lower_color = np.array([125, 40, 40])  # in hsv. red 0, blue 100, purple 125
		upper_color = np.array([160, 255, 255])  # in hsv. red 10, blue 124, purple 150
		video = cv2.VideoCapture(0)
		# video.set(cv2.CAP_PROP_FPS, 15)
		# video.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
		# video.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
		while True:
			time_start = time.time()
			success, frame = video.read()
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			mask_hsv = cv2.inRange(hsv, lower_color, upper_color)
			element = cv2.getStructuringElement(cv2.MORPH_ERODE, (5, 5))
			mask_hsv = cv2.erode(mask_hsv, element, iterations=2)
			mask_component = np.zeros_like(mask_hsv, dtype=np.uint8)
			circles = None
			confidence = []
			num_label, label_img, stats, centroids = cv2.connectedComponentsWithStats(mask_hsv, connectivity=4)
			# print('Time to find connected part', time.time() - time_start)
			for (label, stat, centroid) in zip(range(0, num_label + 1), stats, centroids):
				area_component = stat[cv2.CC_STAT_AREA]
				if area_component < 300 or area_component > 100000 or label == 0:
					continue
				else:
					component = np.zeros_like(mask_hsv, dtype=np.uint8)
					component[label_img == label] = 1
					image, contours, hierarchy = cv2.findContours(component.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
					x_centroid, y_centroid = centroid
					(x_enclose, y_enclose), r_enclose = cv2.minEnclosingCircle(contours[0])
					area_enclose = int(np.pi * r_enclose * r_enclose)
					detected_circle = np.array([int(x_enclose), int(y_enclose), int(r_enclose)])
					circles = np.vstack([circles, detected_circle]) if circles is not None else [detected_circle]
					if np.sqrt((x_centroid - x_enclose) ** 2 + (y_centroid - y_enclose) ** 2) < 100:
						confidence.append(np.abs((area_component - area_enclose) / area_component) )
					else:
						confidence.append(None)
					mask_component = mask_component + component
			info = 'no circle'
			if circles is not None:
				if len(set(confidence)) >= 1 and set(confidence) != {None}:
					idx = confidence.index(min(confidence))
					c = circles[idx]
					cv2.circle(frame, (c[0], c[1]), c[2], (0, 255, 255), 2)
					cv2.circle(frame, (c[0], c[1]), 2, (0, 0, 255), 2)
					info = 'circle at: ' + str(c[0]) + ', ' + str(c[1])
			print('Find circles: ', info, ' in ', time.time() - time_start)
			cv2.putText(frame, "frame time: {0:.5f}".format(1/(time.time() - time_start)), (10, 40), 1, 1, (255, 255, 255))
			mask_component = cv2.cvtColor(mask_component * 255, cv2.COLOR_GRAY2BGR)
			cls.frame = np.hstack([frame, mask_component])
			if time.time() - cls.last_access > 2:
				break
		video.release()
		cv2.destroyAllWindows()
