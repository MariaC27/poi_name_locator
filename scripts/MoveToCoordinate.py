from __future__ import print_function

import sys
import rospy
import actionlib
from geometry_msgs.msg import Point
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from std_msgs.msg import Header

from move_base_msgs.msg import MoveBaseAction
# from move_base_msgs.msg import MoveBaseActionClient
from move_base_msgs.msg import MoveBaseGoal


from poi_name_locator.srv import PoiNameLocator
from poi_name_locator.srv import PoiNameLocatorRequest
from poi_name_locator.srv import PoiNameLocatorResponse

class MoveToCoordinates:

        def __init__(self):
                rospy.init_node('MoveToCoordinates')
                rospy.loginfo('waiting for service poi_name_locator')
                rospy.wait_for_service('poi_name_locator')
                rospy.loginfo('waiting for service poi_name_locator finished')

                self.poi_name_locator_callable = rospy.ServiceProxy(
                'poi_name_locator', PoiNameLocator
                )  # type: callable(PoiNameLocatorRequest) -> PoiNameLocatorResponse

                self.move_base_action_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
                self.move_base_action_client.wait_for_server()
   



        def lookup(self, poi_name):  # type: (str) -> Point
                request = PoiNameLocatorRequest(poi_name)
                #gets coordinates based on poi name - like what the server and the client do 

                # response cannot be None. If server tries to return None, a rospy.ServiceException will raise here.
                response = self.poi_name_locator_callable(request)  # type: PoiNameLocatorResponse

                return response.position


        def move_turtle_bot (self, request):
                poi1 = request.poi_name
                point1 = self.lookup(poi1)

                goal = MoveBaseGoal()
                target_pose = goal.target_pose  # type: PoseStamped

                header = target_pose.header  # type: Header
                header.frame_id = "/map"

                pose = target_pose.pose  # type: Pose

                # pose.orientation  by default is just a bunch of 0's, which is not valid because the length of the
                # vector is 0. Length of vector must be 1, and for map navigation, z-axis must be vertical, so by setting
                # w = 1, it's the same as yaw = 0
                pose.orientation.w = 1

                while not rospy.is_shutdown():
                        ########### Drive to poi1
                        rospy.loginfo('drive to {}'.format(poi1))

                        pose.position = point1
                        header.stamp = rospy.Time.now()

                        self.move_base_action_client.send_goal(goal)
                        self.move_base_action_client.wait_for_result()

                         rospy.loginfo('arrived, now waiting 10 sec')
                        for i in range(100):
                                if rospy.is_shutdown():
                                        return
                                rospy.sleep(0.1)

        if __name__ == "__main__":
                move = MoveToCoordinates()
                move.move_turtle_bot(PoiNameLocatorRequest)
        
