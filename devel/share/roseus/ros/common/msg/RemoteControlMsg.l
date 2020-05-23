;; Auto-generated. Do not edit!


(when (boundp 'common::RemoteControlMsg)
  (if (not (find-package "COMMON"))
    (make-package "COMMON"))
  (shadow 'RemoteControlMsg (find-package "COMMON")))
(unless (find-package "COMMON::REMOTECONTROLMSG")
  (make-package "COMMON::REMOTECONTROLMSG"))

(in-package "ROS")
;;//! \htmlinclude RemoteControlMsg.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(intern "*REMOTE*" (find-package "COMMON::REMOTECONTROLMSG"))
(shadow '*REMOTE* (find-package "COMMON::REMOTECONTROLMSG"))
(defconstant common::RemoteControlMsg::*REMOTE* 0)
(intern "*AUTONOMOUS*" (find-package "COMMON::REMOTECONTROLMSG"))
(shadow '*AUTONOMOUS* (find-package "COMMON::REMOTECONTROLMSG"))
(defconstant common::RemoteControlMsg::*AUTONOMOUS* 1)
(defclass common::RemoteControlMsg
  :super ros::object
  :slots (_header _status _leftwheel _rightwheel ))

(defmethod common::RemoteControlMsg
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:status __status) 0)
    ((:leftwheel __leftwheel) 0)
    ((:rightwheel __rightwheel) 0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _status (round __status))
   (setq _leftwheel (round __leftwheel))
   (setq _rightwheel (round __rightwheel))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:status
   (&optional __status)
   (if __status (setq _status __status)) _status)
  (:leftwheel
   (&optional __leftwheel)
   (if __leftwheel (setq _leftwheel __leftwheel)) _leftwheel)
  (:rightwheel
   (&optional __rightwheel)
   (if __rightwheel (setq _rightwheel __rightwheel)) _rightwheel)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; uint8 _status
    1
    ;; int32 _leftwheel
    4
    ;; int32 _rightwheel
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; uint8 _status
       (write-byte _status s)
     ;; int32 _leftwheel
       (write-long _leftwheel s)
     ;; int32 _rightwheel
       (write-long _rightwheel s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; uint8 _status
     (setq _status (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; int32 _leftwheel
     (setq _leftwheel (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _rightwheel
     (setq _rightwheel (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get common::RemoteControlMsg :md5sum-) "23c6596709461c8678d41a4214a56d44")
(setf (get common::RemoteControlMsg :datatype-) "common/RemoteControlMsg")
(setf (get common::RemoteControlMsg :definition-)
      "Header header

uint8 status
uint8 REMOTE = 0
uint8 AUTONOMOUS = 1

# -100 means backward in max speed.
# +100 means forward in max speed.
int32 leftwheel
int32 rightwheel

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

")



(provide :common/RemoteControlMsg "23c6596709461c8678d41a4214a56d44")


