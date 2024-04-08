#a = right, c = left, b = front, d = back

#!/usr/bin/env python3
import rospy
import time
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class robot():
    def __init__(self):

        self.robot_sub = rospy.Subscriber("/scan", LaserScan,self.scan_callback)
        self.a = 0.0
        self.b = 0.0
        self.c = 0.0
        self.d = 0.0

        self.ctrl_c =False

        self.rate = rospy.Rate(100)
        rospy.on_shutdown(self.shutdownhook)

    def scan_callback(self,msg):
       # print(len(msg.ranges))
        self.a = min(msg.ranges[180],5)
        self.b = min(msg.ranges[360],5)
        self.c = min( msg.ranges[540],5)
        self.d = min(msg.ranges[1],5)
            
    def read_laser(self):
        while not self.ctrl_c:
            if self.a>5:
                self.a =5
            if self.b>5:
                self.b =5
            if self.c>5:
                self.c =5
            if self.d>5:
                self.d =5

            print("a= " + str(self.a) + " b= " + str(self.b) + " c= " + str(self.c) + " d " + str(self.d))
            self.rate.sleep()
       
            rospy.loginfo("node has been started")

            rate = rospy.Rate(100)

            pub = rospy.Publisher("/cmd_vel",Twist,queue_size =10)

            maxi = max(self.a,self.b,self.c)
            msg = Twist()
            if self.b >= 0.5:
                msg.linear.x = -0.5
                msg.angular.z = 0.0
                
            elif self.c == maxi:
                msg.linear.x = 0.0
                msg.angular.z = -1.0
                time.sleep(3.10)

            else:
                msg.linear.x =0.0
                msg.angular.z = 1.0
                time.sleep(3.10)
            
            pub.publish(msg)
            rate.sleep()

    def shutdownhook(self):
        self.ctrl_c = True

if __name__ =='__main__':
    rospy.init_node('rosbot_test',anonymous=True)
    robot_object = robot()
    try:

        robot_object.read_laser()
                        
    except rospy.ROSInterruptException:
        pass  