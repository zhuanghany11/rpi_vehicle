
(cl:in-package :asdf)

(defsystem "common-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "RemoteControlMsg" :depends-on ("_package_RemoteControlMsg"))
    (:file "_package_RemoteControlMsg" :depends-on ("_package"))
  ))