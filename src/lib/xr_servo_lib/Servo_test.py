#coding:utf-8
'''
树莓派WiFi无线视频小车机器人驱动源码
作者：liuviking
版权所有：小R科技（深圳市小二极客科技有限公司www.xiao-r.com）；WIFI机器人网论坛 www.wifi-robots.com
本代码可以自由修改，但禁止用作商业盈利目的！
本代码已申请软件著作权保护，如有侵权一经发现立即起诉！
'''
'''
文 件 名：_Servo_test.py
功    能：舵机测试代码，_XiaoRGEEK_SERVO_.so 、XiaoRGEEK.jpg、_XiaoRGEEK_about_.py三个文件需要放到同一个目录才能正常执行
调用接口：
from _XiaoRGEEK_SERVO_ import XR_Servo
Servo = XR_Servo()
Servo.XiaoRGEEK_SetServoAngle(ServoNum,angle)#设置ServoNum号舵机角度为angle
Servo.XiaoRGEEK_SaveServo()#存储所有角度为上电初始化默认值
Servo.XiaoRGEEK_ReSetServo()#恢复所有舵机角度为保存的默认值
'''
from _XiaoRGEEK_SERVO_ import XR_Servo
Servo = XR_Servo()
import time

offset = -20

Servo.XiaoRGEEK_ReSetServo()#恢复所有舵机角度为保存的默认值

Servo.XiaoRGEEK_SetServoAngle(1,90 + offset)#设置1号舵机角度为30度
time.sleep(2)#延迟1秒
Servo.XiaoRGEEK_SaveServo()#存储所有角度为上电初始化默认值
time.sleep(1)#延迟1秒
Servo.XiaoRGEEK_SetServoAngle(1,120+offset)#设置1号舵机角度为150度
time.sleep(1)#延迟1秒
Servo.XiaoRGEEK_SetServoAngle(1,150+offset)#设置1号舵机角度为150度
time.sleep(1)#延迟1秒



Servo.XiaoRGEEK_SetServoAngle(1, 60+offset)#设置1号舵机角度为150度
time.sleep(1)#延迟1秒
Servo.XiaoRGEEK_SetServoAngle(1,30+offset)#设置1号舵机角度为150度
time.sleep(1)#延迟1秒




Servo.XiaoRGEEK_ReSetServo()#恢复所有舵机角度为保存的默认值
