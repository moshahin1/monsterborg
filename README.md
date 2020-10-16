# Monsterborg
This repository contains 3 ROS packages: 
* `monsterborg_description` 
* `monsterborg_control`
* `monsterborg_navigation`

**IMPORTANT**: Before starting anything it is important to check you have certain ROS packages installed in ROS in order to successfully run each package. Check the `pacakage.xml` file of each packages to find the package dependencies. Secondly, open up a terminal tab (and do not close the tab) and run the command: `roscore`
********************************************************************
**AUTONOMOUS NAVIGATION**
To view autonomous GPS-based navigation, execute the following in different terminal tabs:
1. `roslaunch monsterborg_navigation outdoor_nav.launch` : A Gazebo world and RVIZ world should will pop up. The `move_base` node is up and running. Sometimes Gazebo crashes when this executed this command. If this occurs, re-execute the launch file. 
1. For single point navigation:
`rosrun monsterborg_navigation single_move_base_nav.py`
2. For multiple point navigation:
`rosrun monsterborg_navigation multiple_move_base_nav.py`

Once the Monsterborg is done navigating, the terminal running `roslaunch monsterborg_navigation outdoor_nav.launch` should terminate and display a message the Monsterborg has achieved its goals. 

********************************************************************
The `monsterborg_description` package contains the launch file (`spawn_in_gazebo.launch`) that spawns the model into Gazebo and most importantly loads the robot description into the parameter server under the variable `robot_description`. The `monsterborg_control` package contains the launch file (`monsterborg_control.launch`) that loads the controllers required to control the monsterborg. To get everything running: 

**FIRST**: To spawn the robot, open up a new terminal tab and enter the following command: `roslaunch monsterborg_description spawn_in_gazebo.launch` 

**SECOND**: To load the controllers, open another terminal and enter: `roslaunch monsterborg_control monsterborg_control.launch`

The `monsterborg_control` package contains a python file (`square.py`) that moves the monsterborg in a square indefinitely. To execute the python file open up another 
terminal tab and enter: `rosrun monsterborg_control square.py' 

Whenever you would like to stop the movement enter in the same terminal that is running the `square.py` file: `Ctrl + C` 

If you would like to control the monsterborg yourself, there exists a ROS topic with the name: `/differential_drive/cmd_vel`. To publish a message 
to this topic enter: `rostopic pub /differential_drive/cmd_vel [TAB][TAB] [TAB][TAB]`

A message will occur where you enter the linear and angular velocity of the monsterborg. Press `ENTER` to publish the message. However, due to the nature 
of the package used that implements 4WD differential control, I advise to generate your own python file and publish the commands in a `while` loop to constantly
publish messages to the topic. 

This project was conducted on ROS Melodic, Gazebo and Ubuntu 18.04 LTS. When installing everything on Ubuntu install ROS Melodic first, choosing the desktop-full installation. This installation option will install all the important packages to get started (including all packages that connect ROS with Gazebo such as the plug-ins etc...). ALso please refer to the `package.xml` file of each package to install the additional packages to get everything running smoothly. After installing ROS, install Gazebo. 







