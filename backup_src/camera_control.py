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

class VideoCamera:
    def __init__(self):
        self.lower_color = np.array([125, 43, 46])  # in hsv. red 0, blue 100, purple 125
        self.upper_color = np.array([150, 255, 255])  # in hsv. red 10, blue 124, purple 150
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture(0)
        # self.video.set(cv2.CAP_PROP_FPS, 15)
        # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
        # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
    def __del__(self):
        self.video.release()

    def get_frame(self):
        time_start = time.time()
        success, frame = self.video.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_hsv = cv2.inRange(hsv, self.lower_color, self.upper_color)
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
                image, contours, hierarchy = cv2.findContours(component.copy(), mode=cv2.RETR_EXTERNAL,
                                                              method=cv2.CHAIN_APPROX_SIMPLE)
                x_centroid, y_centroid = centroid
                (x_enclose, y_enclose), r_enclose = cv2.minEnclosingCircle(contours[0])
                area_enclose = int(np.pi * r_enclose * r_enclose)
                detected_circle = np.array([int(x_enclose), int(y_enclose), int(r_enclose)])
                circles = np.vstack([circles, detected_circle]) if circles is not None else [detected_circle]
                print(area_enclose, area_component)
                if np.sqrt((x_centroid - x_enclose) ** 2 + (y_centroid - y_enclose) ** 2) < 100:
                    confidence.append(np.abs((area_component - area_enclose) / area_component) )
                else:
                    confidence.append(None)
                mask_component = mask_component + component
        # print('Time to find circles', time.time() - time_start)
        if circles is not None:
            if len(set(confidence)) >= 1 and set(confidence) != {None}:
                idx = confidence.index(min(confidence))
                c = circles[idx]
                cv2.circle(frame, (c[0], c[1]), c[2], (0, 255, 255), 2)
                cv2.circle(frame, (c[0], c[1]), 2, (0, 0, 255), 2)
            else:
                print('no circle shape detected')
        cv2.putText(frame, "frame time: {0:.5f}".format(1/(time.time() - time_start)), (10, 40), 1, 1, (255, 255, 255))
        mask_component = cv2.cvtColor(mask_component * 255, cv2.COLOR_GRAY2BGR)
        frame = np.hstack([frame, mask_component])
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        # print('Time to draw the most confident circle', time.time() - time_start)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
