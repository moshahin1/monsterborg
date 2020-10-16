#! /usr/bin/env python 

import rospy 
from gazebo_msgs.srv import DeleteModel, DeleteModelRequest
import sys 

rospy.init_node('delete_model')
rospy.loginfo('Waiting for service... ')
rospy.wait_for_service('/gazebo/delete_model')

handler = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
request = DeleteModelRequest()
request.model_name = 'monsterborg'

response = handler(request)
rospy.loginfo('Deleting Model... ')
print(response)
