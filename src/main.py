#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# main.py

"""
The main frame of the vehicle program.
"""

from flask import Flask, render_template, Response, request
from flask import redirect,url_for
import cv2
import numpy as np
import imutils
import time
from gpiozero import Servo
# from camera_control import VideoCamera
from camera_control_thread import VideoCamera

web = Flask(__name__)
global streaming
streaming = 1

def gen(camera):
	while True:
		frame = camera.get_frame()
		if frame is not None and streaming == 1:
			# 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
		else:
			yield('Streaming stopped')

@web.route('/')  # 主页
def index():
	return render_template('index.html')
	
@web.route('/live')  # 主页
def live():
	return render_template('streaming.html')

@web.route('/streaming_switch', methods=['GET', 'POST'])
def streaming_switch():
	global streaming
	
	if request.method == 'POST':
		switch = request.form['switch']
		print(switch, switch.__class__)
		if switch == '1':
			streaming = 1
		else:
			streaming = 0
	return redirect('/')

@web.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
	return Response(gen(VideoCamera()),
					mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	web.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
