// Auto-generated. Do not edit!

// (in-package common.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class RemoteControlMsg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.status = null;
      this.leftwheel = null;
      this.rightwheel = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('status')) {
        this.status = initObj.status
      }
      else {
        this.status = 0;
      }
      if (initObj.hasOwnProperty('leftwheel')) {
        this.leftwheel = initObj.leftwheel
      }
      else {
        this.leftwheel = 0;
      }
      if (initObj.hasOwnProperty('rightwheel')) {
        this.rightwheel = initObj.rightwheel
      }
      else {
        this.rightwheel = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type RemoteControlMsg
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [status]
    bufferOffset = _serializer.uint8(obj.status, buffer, bufferOffset);
    // Serialize message field [leftwheel]
    bufferOffset = _serializer.int32(obj.leftwheel, buffer, bufferOffset);
    // Serialize message field [rightwheel]
    bufferOffset = _serializer.int32(obj.rightwheel, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type RemoteControlMsg
    let len;
    let data = new RemoteControlMsg(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [status]
    data.status = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [leftwheel]
    data.leftwheel = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [rightwheel]
    data.rightwheel = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    return length + 9;
  }

  static datatype() {
    // Returns string type for a message object
    return 'common/RemoteControlMsg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '23c6596709461c8678d41a4214a56d44';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
    
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new RemoteControlMsg(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.status !== undefined) {
      resolved.status = msg.status;
    }
    else {
      resolved.status = 0
    }

    if (msg.leftwheel !== undefined) {
      resolved.leftwheel = msg.leftwheel;
    }
    else {
      resolved.leftwheel = 0
    }

    if (msg.rightwheel !== undefined) {
      resolved.rightwheel = msg.rightwheel;
    }
    else {
      resolved.rightwheel = 0
    }

    return resolved;
    }
};

// Constants for message
RemoteControlMsg.Constants = {
  REMOTE: 0,
  AUTONOMOUS: 1,
}

module.exports = RemoteControlMsg;
