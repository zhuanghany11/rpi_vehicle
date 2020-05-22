#!/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
import json
import os
import random
import ctypes
import logging
import time
from datetime import datetime
from flask import Flask, render_template, Response, request
from flask import redirect,url_for
from flask_socketio import SocketIO
from engineio.payload import Payload
from common.msg import RemoteControlMsg
from std_msgs.msg import Header


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# log.disabled = True
socketio = SocketIO(app)
DEBUG = False
Payload.max_decode_packets = 60

# Global variables used to communicate between web and ros
REMOTE_STATUS = RemoteControlMsg.REMOTE
REMOTE_LEFTWHEEL = 0
REMOTE_RIGHTWHEEL = 0
IMAGE_ENCODED = None
IMAGE_ARRIVED = False

class WebServer:
    def __init__(self):
        self.thread = None
        self.remote_control_msg = RemoteControlMsg()

        if DEBUG:
            run_web_thread()
        else:
            if self.thread is None:
                self.thread = threading.Thread(target=run_web_thread)
                self.thread.start()

    def control_update(self, remote_control_msg):
        global REMOTE_STATUS
        global REMOTE_LEFTWHEEL
        global REMOTE_RIGHTWHEEL
        
        self.remote_control_msg = remote_control_msg
        self.remote_control_msg.status = REMOTE_STATUS
        self.remote_control_msg.leftwheel = REMOTE_LEFTWHEEL
        self.remote_control_msg.rightwheel = REMOTE_RIGHTWHEEL

        return self.remote_control_msg

    def display_update(self, header, data):
        if data is None:
            print(tstamp() + '[Server][Web]\033[31mNone data is received\033[0m')
            return
        else:
            socketio.emit('display_update', {'header': header, 'data': data})

    def image_update(self, image_encoded):
        global IMAGE_ENCODED
        if image_encoded is not None:
            IMAGE_ENCODED = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image_encoded + b'\r\n'

    def web_shutdown(self):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(self.thread.ident)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(SystemExit))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

def gen():
    while True:
        if IMAGE_ENCODED is not None:
            yield(IMAGE_ENCODED)
        else:
            yield(b'Streaming stopped')

@app.route('/')
def index():
    return render_template('dashboard.html', control_msg='')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/video_feed')
# def video_feed():
#     for video_frame in gen():
#         socketio.emit('from_flask',{'data': video_frame})

@socketio.on('connected_at_web')
def handle_my_custom_event():
    print(tstamp() + '\033[32mWeb remote control connected!\033[0m')
    socketio.emit('connected_at_ros')


@socketio.on('disconnect')
def disconnected_socketio():
    print(tstamp() + '\033[31mWeb remote control disconnected!\033[0m')
    global remote_control_IsAutonomous
    remote_control_IsAutonomous = True


@socketio.on('key_pressed')
def key_pressed(remote_control):
    global REMOTE_STATUS
    global REMOTE_LEFTWHEEL
    global REMOTE_RIGHTWHEEL

    REMOTE_STATUS = remote_control['Status']

    direction = remote_control['Direction']
    left_gain = (remote_control['LeftGain']%101) if (remote_control['LeftGain'] > 0) else (0)
    right_gain = (remote_control['RightGain']%101) if (remote_control['RightGain'] > 0) else (0)
    #print(REMOTE_STATUS, direction, left_gain, right_gain)

    direction_str = 'NOT PRESSED'
    if direction == [1, 0, 0, 0]:
        direction_str = 'FORWARD'
        REMOTE_LEFTWHEEL = left_gain
        REMOTE_RIGHTWHEEL = right_gain
    elif direction == [0, 1, 0, 0]:
        direction_str = 'BACKWARD'
        REMOTE_LEFTWHEEL = - left_gain
        REMOTE_RIGHTWHEEL = - right_gain
    elif direction == [0, 0, 1, 0]:
        direction_str = 'LEFT'
        REMOTE_LEFTWHEEL = - left_gain
        REMOTE_RIGHTWHEEL = right_gain
    elif direction == [0, 0, 0, 1]:
        direction_str = 'RIGHT'
        REMOTE_LEFTWHEEL = left_gain
        REMOTE_RIGHTWHEEL = - right_gain
    elif direction == [1, 0, 1, 0]:
        direction_str = 'FORWARD-LEFT'
        REMOTE_LEFTWHEEL = round(left_gain * 0.2)
        REMOTE_RIGHTWHEEL = right_gain
    elif direction == [1, 0, 0, 1]:
        direction_str = 'FORWARD-RIGHT'
        REMOTE_LEFTWHEEL = left_gain
        REMOTE_RIGHTWHEEL = round(right_gain * 0.2)
    elif direction == [0, 1, 1, 0]:
        direction_str = 'BACKWARD-LEFT'
        REMOTE_LEFTWHEEL = - round(left_gain * 0.2)
        REMOTE_RIGHTWHEEL = - right_gain
    elif direction == [0, 1, 0, 1]:
        direction_str = 'BACKWARD-RIGHT'
        REMOTE_LEFTWHEEL = - left_gain 
        REMOTE_RIGHTWHEEL = - round(right_gain * 0.2)
    else:
        direction_str = 'N/A'
        REMOTE_LEFTWHEEL = 0
        REMOTE_RIGHTWHEEL = 0

    socketio.emit('key_feedback', direction_str)


def run_web_thread():
    if DEBUG:
        socketio.run(app=app, host='0.0.0.0', port=5000, debug=True, use_reloader=True)
    else:
        socketio.run(app=app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)


def tstamp():
    """
    Print the current time stamp in accuracy of 0.001 ms.
    The format is like [2019-01-01 19:00:33.123]
    """
    return '[{}]'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])


if __name__ == '__main__':
    DEBUG = True
    web_server = WebServer()
