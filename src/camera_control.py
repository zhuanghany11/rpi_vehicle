#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# camera_control.py

"""
Use opencv to control the camera and capture the image.
1. Image is processed by opencv to locate the target and send the location to servo control
2. Image is streamed to the website for visualization
"""

from flask import Flask, render_template, Response
import cv2
import numpy as np
import imutils

class VideoCamera:
    def __init__(self):
        self.color_lower = np.array([200, 0, 0])   #lower color raange
        self.color_upper = np.array([255, 200, 200])  #upper color range
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        mask = cv2.inRange(frame, self.color_lower, self.color_upper)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        center = None
        if len(cnts) > 4:
            c = max(cnts, key=cv2.contourArea)
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            if M['m00'] == 0:
                M['m00'] = 1e-5
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255),2)
                cv2.circle(frame, center, 5, (0,0,255), -1)
                x, y = int(x), int(y)
                print(x, y)
        else:
            return
        output = cv2.bitwise_and(frame, frame, mask = mask)
        # cv2.imshow("frame", np.hstack([frame, output]))

        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', output)
        return jpeg.tobytes()


web = Flask(__name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame:
            # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            print('no object found')

@web.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('index.html')


@web.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    web.run(host='0.0.0.0', debug=True, port=5000)
