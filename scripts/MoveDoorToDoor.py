#!/usr/bin/env python
from __future__ import print_function

import sys
import rospy
import actionlib
from geometry_msgs.msg import Point
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from std_msgs.msg import Header
from std_msgs.msg import String

from move_base_msgs.msg import MoveBaseAction
# from move_base_msgs.msg import MoveBaseActionClient
from move_base_msgs.msg import MoveBaseGoal

from poi_name_locator.srv import PoiNameLocator
from poi_name_locator.srv import PoiNameLocatorRequest
from poi_name_locator.srv import PoiNameLocatorResponse
from poi_name_locator.srv import PoiNames
from poi_name_locator.srv import PoiNamesRequest
from poi_name_locator.srv import PoiNamesResponse


# A simple demonstration of using poi_name_locator to move from door to door throughout the second floor of Halligan, 
#and stop at each one before moving on to the next
#To be used as a test/example program to make sure the robot is working correctly  
class Patrol:
    def __init__(self):
        rospy.init_node('doors_patrol')

        rospy.loginfo('waiting for service poi_names')
        rospy.wait_for_service('poi_names')
        rospy.loginfo('waiting for service poi_names finished')

        self.poi_name_locator_callable = rospy.ServiceProxy(
            'poi_name_locator', PoiNameLocator
        )  # type: callable(PoiNamesRequest) -> PoiNamesResponse
	
	self.poi_names_callable = rospy.ServiceProxy('poi_names', PoiNames)

        self.move_base_action_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.move_base_action_client.wait_for_server()
	#self.retlist = []

    def lookup(self, poi_name):  # type: (str) -> Point
        request = PoiNameLocatorRequest(poi_name)

	rospy.loginfo('Going to requested position %s'%(poi_name))

        # response cannot be None. If server tries to return None, a rospy.ServiceException will raise here.
        response = self.poi_name_locator_callable(request)  # type: PoiNameLocatorResponse

        return response.position


    def getList(self):
	
	#trying to get response from server commented out for now, 
	#as it keeps returning an empty list 

	#response = PoiNamesResponse()
	#if not response.locations:
		#rospy.loginfo('list is empty')	
	#return response.locations 


	#HARD CODING:

	locList = ['Door_202_Graduate_Offices', 'Door_204_Kitchenette','Door_205_Scheutz_Ruiter', 'Door_206_Akitaya', 'Door_207_Vu', 'Door_208_Koomson', 'Door_209_Conference_Right', 'Door_210_Hughes', 'Door_211_Foster', 'Door_212_Collab_Right', 'Door_213_Sinapov', 'Door_214_Mendelsohn', 'Door_215_Jacob', 'Door_212_Collab_Left', 'Door_Mens_Bathroom','Door_217_Janitor_Closet',  'Door_Womens_Bathroom', 'Door_220_Afsar', 'Door_221_Edwards', 'Door_222_Ramsey', 'Door_224_Sheldon', 'Door_209_Conference_Left', 'Door_226_Graduate_Offices', 'Door_228_SinapovLab_ProfKorman', 'Door_235B_Offices', 'Door_250_Graduate_Offices', 'Door_233_Closet', 'Door_235A_Hempstead', 'Door_219_Wellness_Room', 'Door_237_Guyer', 'Door_239_Souvaine', 'Door_241_Landau', 'Door_245_Main_Office', 'Door_245_Sitting_Area']

	length = len(locList)
	rospy.loginfo('print length %s'%(length))

	return locList

	
    def getItem(self, index):
	retlist = self.getList()
	rospy.sleep(0.1) 
	temp = retlist[index]
	rospy.loginfo('reached here')
	return temp
	

    def patrol(self): #moves from door to door in ascending order of door number  

	for x in range(34): 

	
		point1 = self.lookup(self.getItem(x))  # type: Point

	       	goal = MoveBaseGoal()
		target_pose = goal.target_pose  # type: PoseStamped

		header = target_pose.header  # type: Header
		header.frame_id = "/map"

		pose = target_pose.pose  # type: Pose

		# pose.orientation  by default is just a bunch of 0's, which is not valid because the length of the
		# vector is 0. Length of vector must be 1, and for map navigation, z-axis must be vertical, so by setting
		# w = 1, it's the same as yaw = 0
		pose.orientation.w = 1

			########### Drive to poi1
			#rospy.loginfo('drive to {}'.format(response[x]))

		pose.position = point1
		header.stamp = rospy.Time.now()

		self.move_base_action_client.send_goal(goal)
		self.move_base_action_client.wait_for_result()

		rospy.loginfo('arrived, now waiting 5 sec')
		for i in range(50):
			if rospy.is_shutdown():
				return
			rospy.sleep(0.1)


	rospy.loginfo('finished door to door patrol program')

		




if __name__ == "__main__":
    patrol = Patrol()
    patrol.patrol()
