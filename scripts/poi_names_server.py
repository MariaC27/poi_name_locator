from __future__ import print_function

from std_msgs.msg import String

import rospy
import rospkg
import yaml
import os

from poi_names.srv import poi_names
from poi_names.srv import poi_namesRequest
from poi_names.srv import poi_namesResponse

class PoiNamesServer:


	 def __init__(self):
	 	self.poi = None



	 def load(self, locations_from_package=None, locations_from_file=None):  # type: (str, str) -> None
        rospack = rospkg.RosPack()

        if locations_from_package is None or locations_from_file is None:
            pkg_path = rospack.get_path('poi_name_locator')
            locations_yml_path = os.path.join(pkg_path, 'share', 'config.yaml')

            try:
                with open(locations_yml_path, "r") as f:
                    yaml_load = yaml.load(f.read())
                    try:
                        locations_from_package = yaml_load['locations_from_package']
                        locations_from_file = yaml_load['locations_from_file']
                    except KeyError:
                        rospy.logwarn("PoiNameLocatorServer share/config.yaml does not contain locations keys. " +
                                      "PoiNameLocatorServer not initialized. Name locator requests will fail until " +
                                      "locations file is loaded")
                        return
            except IOError:
                rospy.logwarn("PoiNameLocatorServer share/config.yaml does not exist. PoiNameLocatorServer not " +
                              "initialized. Name locator requests will fail until locations file is loaded")
                return

        pkg_path = rospack.get_path(locations_from_package)
        locations_yml_path = os.path.join(pkg_path, locations_from_file)

        with open(locations_yml_path, "r") as f:
            self.poi = yaml.load(f.read())
            #reads/loads the yaml file 

    def handle_poi_response():

    	#for loop that gets all the values and stories them in an array
    	#then the array is returned 

    	retval = Point()
    	String[] locations 

    	for x in range (0, 34):
    	 	retval.x = self.poi["Door_"]['x']
        	retval.y = self.poi["Door_"]['y']
    		locations[x] = "x: " + retval.x + "y: " + retval.y + "z: 0.0"
    	

        return poi_namesResponse(locations)



     def spin(self):
        rospy.init_node('poi_names_server')
        self.load()
        s = rospy.Service('poi_names', poi_names, self.handle_poi_response)
        #call the method from above that loops through and gives esponse coordinates 
        rospy.loginfo("Ready print out coordinates of all locations.")
        rospy.spin()

