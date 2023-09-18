#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Int32
import subprocess
import os


class MoveBaseClient:

    def __init__(self):
        self.estacion = 0
        self.subscriber = rospy.Subscriber("dato", Int32, self.callback)
        rospy.init_node('movebase_client_py')

    def callback(self, msg):
        self.estacion = msg.data
        rospy.loginfo("Estacion: %d", msg.data)

    def check(self):
        if self.estacion == 0:
            rospy.loginfo("No es la estacion")
        elif self.estacion == 1:
            rospy.loginfo("Si es la estacion")
            rospy.sleep(10)
            self.movebase_client(6)
            rospy.loginfo("6 Goal execution done!")
            self.shutdown()

    def movebase_client(self, x):
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        client.wait_for_server()

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()

        # Assigning pose values same as in your code
        if x == 1:
            goal.target_pose.pose.position.x = 2.846
            goal.target_pose.pose.position.y = 0.000
            goal.target_pose.pose.orientation.z = 0.705
            goal.target_pose.pose.orientation.w = 0.709
        elif x == 2:
            goal.target_pose.pose.position.x = 2.846
            goal.target_pose.pose.position.y = 3.556
            goal.target_pose.pose.orientation.z = 0.000
            goal.target_pose.pose.orientation.w = 1.000
        elif x == 3:  # primera estacion
            goal.target_pose.pose.position.x = 3.890
            goal.target_pose.pose.position.y = 3.556
            goal.target_pose.pose.orientation.z = 0.000
            goal.target_pose.pose.orientation.w = 1.000
        elif x == 4:  # segunda estacion
            goal.target_pose.pose.position.x = 4.914
            goal.target_pose.pose.position.y = 3.556
            goal.target_pose.pose.orientation.z = 0.000
            goal.target_pose.pose.orientation.w = 1.000
        elif x == 5:  # tercera estacion
            goal.target_pose.pose.position.x = 6.011
            goal.target_pose.pose.position.y = 3.556
            goal.target_pose.pose.orientation.z = 0.000
            goal.target_pose.pose.orientation.w = 1.000
        else:
            goal.target_pose.pose.position.x = 7.634
            goal.target_pose.pose.position.y = 3.556
            goal.target_pose.pose.orientation.z = 0.0
            goal.target_pose.pose.orientation.w = 1.000

        client.send_goal(goal)
        wait = client.wait_for_result()

        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        else:
            return client.get_result()

    def open_teleop(self):
        rospy.loginfo("Opening teleop_twist_keyboard...")
        subprocess.Popen(["rosrun", "teleop_twist_keyboard", "teleop_twist_keyboard.py"])

    def shutdown(self):
        os.system('rosnode kill -a')
        os.system('pkill -f rosmaster')

    def execute(self):
        try:
            result = self.movebase_client(1)
            rospy.loginfo("1 Goal execution done!")
            rospy.sleep(7)

            result = self.movebase_client(2)
            rospy.loginfo("2 Goal execution done!")
            rospy.sleep(7)

            result = self.movebase_client(3)
            rospy.loginfo("3 Goal execution done!")
            rospy.sleep(7)
            self.open_teleop()
            rospy.sleep(50)
            subprocess.Popen(["pkill", "-f", "teleop_twist_keyboard"])
            self.check()

            result = self.movebase_client(4)
            rospy.loginfo("4 Goal execution done!")
            rospy.sleep(7)
            self.open_teleop()
            rospy.sleep(50)
            subprocess.Popen(["pkill", "-f", "teleop_twist_keyboard"])
            self.check()

            result = self.movebase_client(5)
            rospy.loginfo("5 Goal execution done!")
            rospy.sleep(7)
            self.open_teleop()
            rospy.sleep(50)
            subprocess.Popen(["pkill", "-f", "teleop_twist_keyboard"])
            self.check()

            if result:
                rospy.loginfo("Goal execution done!" + str(result))
        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")

    def spin(self):
        rospy.spin()

if __name__ == '__main__':
    client = MoveBaseClient()
    client.execute()
    client.spin()