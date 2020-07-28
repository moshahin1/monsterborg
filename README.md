# Monsterborg
So far this repository contains 2 ROS packages: 
* `monsterborg_description` 
* `monsterborg_control`

**IMPORTANT**: Before starting anything it is important to open (and do not close the tab) the terminal and run the command: `roscore`

The `monsterborg_description` package contains the launch file (`spawn_in_gazebo.launch`) that spawns the model into Gazebo and most importantly loads the robot description into
the parameter server under the variable `robot_description`. The `monsterborg_control` package contains the launch file (`monsterborg_control.launch`) 
that loads the controllers required to control the monsterborg. To get everything running: 

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






