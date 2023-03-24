#!/usr/bin/env python

from __future__ import print_function

import sys
import rospy
from rospy_tutorials.srv import AddTwoInts,AddTwoIntsResponse,AddTwoIntsRequest

def add_two_ints_client(x, y):
    rospy.loginfo("Paso 1")
    rospy.wait_for_service('add_two_ints')
    rospy.loginfo("Paso 2")
    try:
        rospy.loginfo("Paso 3")
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
        rospy.loginfo("Paso 4")
        resp1 = add_two_ints(x, y)
        rospy.loginfo("Paso 5")
        return resp1.sum
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
        print(usage())
        sys.exit(1)
        
    rospy.init_node('client_node')
    print("Requesting %s+%s"%(x, y))
    print("%s + %s = %s"%(x, y, add_two_ints_client(x, y)))