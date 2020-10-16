#! /usr/bin/env python

import numpy 
import rospy
from nav_msgs.msg import Path

def callback(msg):
    global x_traj
    global y_traj
    x_traj.append(00)
    y_traj.append(00)
    for element in msg.poses:
        x_traj.append(element.pose.position.x)
        y_traj.append(element.pose.position.y)
 

def shutdown_hook():
    global x_traj 
    global y_traj 

    matrix = numpy.column_stack((x_traj,y_traj))
    numpy.savetxt("/home/moshahin/catkin_ws/src/monsterborg_navigation/misc2/local_plan_3.csv", matrix, delimiter=",")


rospy.init_node('local_plan')
rospy.Subscriber('/move_base/TrajectoryPlannerROS/local_plan', Path, callback)

x_traj = []
y_traj = []

rospy.on_shutdown(shutdown_hook)
rospy.spin()
