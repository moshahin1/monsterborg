#! /usr/bin/env python

import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist


class MonsterborgSquare:
    def __init__(self):
        self.ctrl_c = False
        self.pub_cmd = rospy.Publisher('/differential_drive/cmd_vel', Twist, queue_size=1)
        self.cmd_vel = Twist()
        self.rate = rospy.Rate(5)
        rospy.on_shutdown(self.shutdownhook)

    def shutdownhook(self):
        self.ctrl_c = True
        self.cmd_vel.linear.x = 0
        self.cmd_vel.angular.z = 0
        self.publish_once_in_cmd_vel()
        rospy.loginfo('Shutting down... ')

    def drive_forward(self):
        counter = 0
        self.cmd_vel.linear.x = 0.5
        self.cmd_vel.angular.z = 0
        while not counter == 1:
            self.pub_cmd.publish(self.cmd_vel)
            counter = counter + 0.2
            self.rate.sleep()

    def right_turn(self):
        # 0.785 rad/s
        counter = 0
        self.cmd_vel.linear.x = 0
        self.cmd_vel.angular.z = 0.785
        while not counter == 2:
            self.pub_cmd.publish(self.cmd_vel)
            counter = counter + 0.2
            self.rate.sleep()


rospy.init_node('square')
square = MonsterborgSquare()
while not rospy.is_shutdown():
    square.drive_forward()
    rospy.loginfo('Driving forward... ')
    square.right_turn()
    rospy.loginfo('Turning right... ')
