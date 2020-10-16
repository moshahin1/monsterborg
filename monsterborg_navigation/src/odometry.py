#! /usr/bin/env python

import rospy 
import numpy 
from nav_msgs.msg import Odometry

def callback(msg):
    global x_pos
    global y_pos

    x_pos.append(msg.pose.pose.position.x)
    y_pos.append(msg.pose.pose.position.y)

def shutdown_hook():
    global x_pos
    global y_pos

    matrix = numpy.column_stack((x_pos,y_pos))
    numpy.savetxt("/home/moshahin/catkin_ws/src/monsterborg_navigation/misc2/odom_3.csv", matrix, delimiter=",")


rospy.init_node("robot_position")
rospy.Subscriber('/odometry/filtered', Odometry, callback)

x_pos = []
y_pos =[]

rospy.on_shutdown(shutdown_hook)
rospy.spin()
