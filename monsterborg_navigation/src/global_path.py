#! /usr/bin/env python

import numpy 
import rospy
from nav_msgs.msg import Path
#from std_msgs.msg import Bool 

def shutdown_hook():
    global x 
    global y 
    
    matrix = numpy.column_stack((x,y))
    numpy.savetxt("/home/moshahin/catkin_ws/src/monsterborg_navigation/misc/global_plan_6.csv", matrix, delimiter=",")


rospy.init_node('global_plan')

# This command listens to the topic once!
message = rospy.wait_for_message('/move_base/NavfnROS/plan', Path)
x = []
y = []
for element in message.poses:
    x.append(element.pose.position.x)
    y.append(element.pose.position.y)


rospy.on_shutdown(shutdown_hook)
rospy.spin()
