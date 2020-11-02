# Monsterborg
This repository contains 3 ROS packages: 
* `monsterborg_description` 
* `monsterborg_control`
* `monsterborg_navigation`

**IMPORTANT**: Before starting anything it is important to check you have certain ROS packages installed in ROS in order to successfully run each package. Check the `pacakage.xml` file of each packages to find the package dependencies. Secondly, open up a terminal tab (and do not close the tab) and run the command: `roscore`
********************************************************************
**AUTONOMOUS NAVIGATION**

To view autonomous GPS-based navigation, execute the following in different terminal tabs:
1. `roslaunch monsterborg_navigation outdoor_nav.launch` : A Gazebo world and RVIZ world will pop up. The `move_base` node is up and running. Sometimes Gazebo crashes when this executed this command. If this occurs, re-execute the launch file. 

1. For single point navigation:
`rosrun monsterborg_navigation single_move_base_outdoor_nav.py`
2. For multiple point navigation:
`rosrun monsterborg_navigation multiple_move_base_outdoor_nav.py`

Once the Monsterborg is done navigating, the terminal running `roslaunch monsterborg_navigation outdoor_nav.launch` should terminate and display a message the Monsterborg has achieved its goals. 

*********************************************************************
This project was conducted on ROS Melodic, Gazebo and Ubuntu 18.04 LTS. When installing everything on Ubuntu install ROS Melodic first, choosing the desktop-full installation. This installation option will install all the important packages to get started (including all packages that connect ROS with Gazebo such as the plug-ins etc...). ALso please refer to the `package.xml` file of each package to install the additional packages to get everything running smoothly. After installing ROS, install Gazebo. 







