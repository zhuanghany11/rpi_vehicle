#!/usr/bin/python3
# -*- coding: utf-8 -*-

import rospy
import sys
from datetime import datetime
import numpy as np

from common.msg import RemoteControlMsg
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Header

from web_server import WebServer
from flask import Flask, render_template, Response, request
from flask import redirect,url_for


class ServerNode:
    def __init__(self):
        # Define main algorithm object
        self.m_webServer = WebServer()

        # Define variables to publish topic
        # variables for remote_control_publisher
        # topic name="RemoteControl", message=RemoteControlMsg
        self.remote_control_msg = RemoteControlMsg()

        # Initialization
        rospy.init_node('server_node', anonymous=True)
        print(tstamp() + '\033[32m[Server]Node launched\033[0m')
        rospy.on_shutdown(self.shutdown)
        self.header_seq = 0

        # Define publisher and rate
        self.remote_control_publisher = rospy.Publisher(
            'remote_control', RemoteControlMsg, queue_size=10, latch=True
        )
        
        self.image_subscriber = rospy.Subscriber(
            '/front_camera/compressed', CompressedImage, self.callback_image_received
        )

        self.rate = rospy.Rate(20)

    def publishing(self):
        success = True
        while success and not rospy.is_shutdown():
            # Update remote control topic
            self.remote_control_msg = self.m_webServer.control_update(self.remote_control_msg)

            msg_header = Header()
            msg_header.seq = self.header_seq
            msg_header.stamp = rospy.Time.now()

            # Publish remote control topic
            self.remote_control_msg.header = msg_header
            self.remote_control_publisher.publish(self.remote_control_msg)

            # ROS sleep
            self.header_seq += 1

            # ROS sleep
            self.rate.sleep()

    def callback_image_received(self, compressed_image):
        self.m_webServer.image_update(compressed_image.data)

    def shutdown(self):
        print(tstamp() + '\033[31m[Server]Node shutdown\033[0m')
        self.m_webServer.web_shutdown()
        # self.wlk_canbus.canbus_shutdown()
        rospy.sleep(0.1)

def tstamp():
    """
    Print the current time stamp in accuracy of 0.001 ms.
    The format is like [2019-01-01 19:00:33.123]
    """
    return '[{}]'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])


if __name__ == '__main__':
    print(tstamp() + '\033[32m[Server]Running node on ' + sys.version + '\033[0m')
    try:
        server_node = ServerNode()
        server_node.publishing()
    except Exception as e:
        server_node.shutdown()
        print(tstamp() + '\033[31m[Server]Node terminated due to ', e, '\033[0m')

