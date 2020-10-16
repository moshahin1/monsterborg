#! /usr/bin/env python

import rospy
import rospkg
import os.path
import numpy
import geodesy.utm 
import tf 
import actionlib 
from geometry_msgs.msg import PointStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Bool

# ************************************ Global Variables ************************************:
PENDING = 0
ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4

rospack = rospkg.RosPack()
local_path = '/waypoints/waypoints.txt'
abs_path = rospack.get_path('monsterborg_navigation') + local_path

# *************************************** Functions ***************************************:

def NumOfWayPoints():
    """ The purpose of this function is to return the number of waypoints
        in the test (.txt) file. """

    global abs_path
    if os.path.exists(abs_path):
        file = open(abs_path)
        NumOfPoints = len(file.readlines())
        file.close()
        return NumOfPoints
    else:
        print("ERROR: File cannot be found or does not exist!")

def GetWaypoints_numpy():
    """ The purpose of this function is to transform the GPS coordinates into a n-by-2
        matrix using the numpy module. """

    global abs_path
    if os.path.exists(abs_path):
        # Creating a n-dimensional array <class numpy.ndarray>
        matrix = numpy.loadtxt(abs_path, dtype=float)
        return matrix
    else:
        print("ERROR: File cannot be found or does not exist!")
        rospy.logerr("File cannot be found or does not exist!")

def LatLongToUTM(latitude, longitude):
    """ The purpose of this function is:
        1. to convert GPS coordinates into UTM Coordinates. 
        2. convert the UTM Coordinates into a geometry_msg/PointStamped ROS message w.r.t the utm frame. """
    
    UTMPoint = PointStamped()   
    
    UTMCoords = geodesy.utm.fromLatLong(latitude, longitude).toPoint()

    UTMPoint.header.frame_id = 'utm'
    UTMPoint.header.stamp = rospy.Time(0)
    UTMPoint.point.x = UTMCoords.x 
    UTMPoint.point.y = UTMCoords.y 
    UTMPoint.point.z = UTMCoords.z 

    # print(UTMPoint)

    # Return geometry_msgs/PointStamped Message 
    return UTMPoint 

def PointTransformation(UTMPoint_input):
    """ The purpose of this function is to transform the POI from the UTM frame 
        to the odom frame (frame of the robot - this can later be changed to transform to map frame instead). 
        The input of this function is a geometry_msg/PointStamped w.r.t UTM frame.
        The OUTPUT of this function is a geometry_msg/PointStamped w.r.t odom/map frame. """

    TransformedPoint = PointStamped()
    listener = tf.TransformListener()
    notDone = True 

    while notDone:
        try:
            listener.waitForTransform('odom', 'utm', rospy.Time.now(), rospy.Duration(10.0))

            # Transforms geometry_msgs/PointStamped message to frame target_frame=odom 
            TransformedPoint = listener.transformPoint('odom', UTMPoint_input)
            notDone = False 
        except tf.Exception:
            print("tf.Exception occured! ")
            continue

    return TransformedPoint

def move_base_goal(curr_point, next_point, last_point):
    """ INPUT (curr_point:geometry_msgs/PointStamped, next_point:geometry_msgs/PointStamped, last_point:Bool)
		OUTPUT (goal:move_base_msgs/MoveBaseGoal)
		1.) curr_point is used to build (x,y,z) part of goal, the point the robot should reach
        2.) next_point/last_point are used to determine the goal orientation the robot should achieve.  """
    
    goal = MoveBaseGoal()

    # std_msgs/Header portion of goal geometry_msgs/PoseStamped:
    goal.target_pose.header.frame_id = 'odom'
    goal.target_pose.header.stamp = rospy.Time.now()

    # geometry_msgs/PointStamped of goal geometry_msgs/PoseStamped
    goal.target_pose.pose.position.x = curr_point.point.x 
    goal.target_pose.pose.position.y = curr_point.point.y 
    goal.target_pose.pose.position.z = 0 

    # geometry_msgs/Quaternion of goal geometry_msgs/PoseStamped
    if last_point == False: 
        x_next = next_point.point.x  
        y_next = next_point.point.y 

        x_current = curr_point.point.x 
        y_current = curr_point.point.y 

        delta_x = x_next - x_current
        delta_y = y_next - y_current
        
        yaw = numpy.arctan2(delta_y, delta_x)
        roll = 0; pitch = 0 
       
        # Converting RPY (euler) to quaternions: 
        quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
        goal.target_pose.pose.orientation.x = quaternion[0]
        goal.target_pose.pose.orientation.y = quaternion[1]
        goal.target_pose.pose.orientation.z = quaternion[2]
        goal.target_pose.pose.orientation.w = quaternion[3]
    
    else:
        goal.target_pose.pose.orientation.w = 1 

    return goal 
        
# ************************************ Main Program ************************************:
# Node name: 
rospy.init_node('gps_waypoint')

lat_curr = 51.423436
long_curr = -2.671505 
last_point = True

# Creating a client to connect with the MoveBase ActionServer:
client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)

# Waiting for move_base action server to be active
rospy.loginfo("Waiting for Action Server to connect to Action Client... ")
client.wait_for_server()
rospy.loginfo("Action Server is connected to the Action Client! ")

# Publisher to publish the current goal w.r.t odom frame for visualization in rviz:
pub_PointStamped = rospy.Publisher('/gps_point', PointStamped, latch=True, queue_size=1)

# Convert coordinates to UTM geometry_msgs/PointStamped w.r.t:
UTM_point = LatLongToUTM(lat_curr, long_curr)

# Convert utm -> odom frame
odom_point = PointTransformation(UTM_point)

goal = move_base_goal(odom_point, odom_point, last_point)

client.send_goal(goal)
while client.get_state() < DONE:
	odom_point.header.stamp = rospy.Time.now()
	pub_PointStamped.publish(odom_point) 
	rospy.loginfo("Achieving goal...")

if client.get_state() == DONE:
    rospy.loginfo("Goal achieved!")

else:
    rospy.signal_shutdown("Monsterborg was unable to reach the goal, shutting down node.")

rospy.loginfo("Monsterborg has reached all goals.")
rospy.spin()





