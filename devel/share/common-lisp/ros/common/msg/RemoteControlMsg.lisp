; Auto-generated. Do not edit!


(cl:in-package common-msg)


;//! \htmlinclude RemoteControlMsg.msg.html

(cl:defclass <RemoteControlMsg> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (status
    :reader status
    :initarg :status
    :type cl:fixnum
    :initform 0)
   (leftwheel
    :reader leftwheel
    :initarg :leftwheel
    :type cl:integer
    :initform 0)
   (rightwheel
    :reader rightwheel
    :initarg :rightwheel
    :type cl:integer
    :initform 0))
)

(cl:defclass RemoteControlMsg (<RemoteControlMsg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <RemoteControlMsg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'RemoteControlMsg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name common-msg:<RemoteControlMsg> is deprecated: use common-msg:RemoteControlMsg instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <RemoteControlMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader common-msg:header-val is deprecated.  Use common-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'status-val :lambda-list '(m))
(cl:defmethod status-val ((m <RemoteControlMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader common-msg:status-val is deprecated.  Use common-msg:status instead.")
  (status m))

(cl:ensure-generic-function 'leftwheel-val :lambda-list '(m))
(cl:defmethod leftwheel-val ((m <RemoteControlMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader common-msg:leftwheel-val is deprecated.  Use common-msg:leftwheel instead.")
  (leftwheel m))

(cl:ensure-generic-function 'rightwheel-val :lambda-list '(m))
(cl:defmethod rightwheel-val ((m <RemoteControlMsg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader common-msg:rightwheel-val is deprecated.  Use common-msg:rightwheel instead.")
  (rightwheel m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<RemoteControlMsg>)))
    "Constants for message type '<RemoteControlMsg>"
  '((:REMOTE . 0)
    (:AUTONOMOUS . 1))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'RemoteControlMsg)))
    "Constants for message type 'RemoteControlMsg"
  '((:REMOTE . 0)
    (:AUTONOMOUS . 1))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <RemoteControlMsg>) ostream)
  "Serializes a message object of type '<RemoteControlMsg>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'status)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'leftwheel)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'rightwheel)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <RemoteControlMsg>) istream)
  "Deserializes a message object of type '<RemoteControlMsg>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'status)) (cl:read-byte istream))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'leftwheel) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'rightwheel) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<RemoteControlMsg>)))
  "Returns string type for a message object of type '<RemoteControlMsg>"
  "common/RemoteControlMsg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RemoteControlMsg)))
  "Returns string type for a message object of type 'RemoteControlMsg"
  "common/RemoteControlMsg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<RemoteControlMsg>)))
  "Returns md5sum for a message object of type '<RemoteControlMsg>"
  "23c6596709461c8678d41a4214a56d44")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'RemoteControlMsg)))
  "Returns md5sum for a message object of type 'RemoteControlMsg"
  "23c6596709461c8678d41a4214a56d44")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<RemoteControlMsg>)))
  "Returns full string definition for message of type '<RemoteControlMsg>"
  (cl:format cl:nil "Header header~%~%uint8 status~%uint8 REMOTE = 0~%uint8 AUTONOMOUS = 1~%~%# -100 means backward in max speed.~%# +100 means forward in max speed.~%int32 leftwheel~%int32 rightwheel~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'RemoteControlMsg)))
  "Returns full string definition for message of type 'RemoteControlMsg"
  (cl:format cl:nil "Header header~%~%uint8 status~%uint8 REMOTE = 0~%uint8 AUTONOMOUS = 1~%~%# -100 means backward in max speed.~%# +100 means forward in max speed.~%int32 leftwheel~%int32 rightwheel~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <RemoteControlMsg>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     1
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <RemoteControlMsg>))
  "Converts a ROS message object to a list"
  (cl:list 'RemoteControlMsg
    (cl:cons ':header (header msg))
    (cl:cons ':status (status msg))
    (cl:cons ':leftwheel (leftwheel msg))
    (cl:cons ':rightwheel (rightwheel msg))
))
