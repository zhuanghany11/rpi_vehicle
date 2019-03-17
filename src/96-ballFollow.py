# from gpiozero import Motor
# from time import sleep
# import cv2
# import numpy as np
# import imutils
#
# m = Motor(forward=17, backward=18) # fwd=cw bck=ccw
#
# boundaries = [ ( [60, 162, 174],    #lower color range
#                  [135, 237, 242] ) ]#upper color range
#
# cap = cv2.VideoCapture(0)
#
# ##cv2.imwrite("/media/pi/USB1/yellowBALL.jpg", frame)
#
# while True:
#
#     ret, frame = cap.read()
#
#     for (lower, upper) in boundaries:
#
#         lower = np.array(lower, dtype = "uint8")
#         upper = np.array(upper, dtype = "uint8")
#
#         mask = cv2.inRange(frame, lower, upper)
#
#         cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX$
#         cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#         center = None
#
#         if len(cnts) > 4:
#             c = max(cnts, key=cv2.contourArea)
#             ((x,y), radius) = cv2.minEnclosingCircle(c)
#             M = cv2.moments(c)
#             center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#
#             if radius > 10:
#                 cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255),2)
#                 cv2.circle(frame, center, 5, (0,0,255), -1)
#                 x, y = int(x), int(y)
#
#                 print x, y
#
#                 if (x > 260) and (x < 360):
#                     #continue
#                     print "middle" # do nothing, in ideal middle location
#                 elif (x <= 260) and (x > 100):
#                     m.backward(.6)
#                     sleep(.04)
#                     m.stop()
# ##                    sleep(.5)
#                 elif (x >= 360) and (x < 520):
#                     m.forward(.6)
#                     sleep(.04)
#                     m.stop()
# ##                    sleep(.5)
#                 elif (x <= 100):
#                     m.backward(1)
#                     sleep(.05)
#                     m.stop()
#                 elif (x >= 520):
#                     m.forward(1)
#                     sleep(.05)
#                     m.stop()
#         else:
#             continue
#
#         output = cv2.bitwise_and(frame, frame, mask = mask)
#
#         cv2.imshow("frame", np.hstack([frame, output]))
#
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# cap.release()
# cv2.destroyAllWindows()
# cv2.waitKey(1)
