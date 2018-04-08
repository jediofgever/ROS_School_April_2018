#!/usr/bin/env python

import rospy
import math
import tf
import tf2_ros
import tf_conversions
import geometry_msgs

br = tf2_ros.TransformBroadcaster()  
cnt = 0  
position_odom = [0.,0.]

def calculate_position():
    global cnt
    if cnt > 300:
        cnt = 0
    cnt = cnt+1
    x = 3* math.cos(cnt*0.02)
    y = math.sin(2*cnt*0.02)

    position = (x,y)
    return position

def calculate_tf():
    t = geometry_msgs.msg.TransformStamped()
    #getting actual position
    position_odom = calculate_position()
    #calculating transform
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "map"
    t.child_frame_id = "odom"
    t.transform.translation.x = position_odom[0]
    t.transform.translation.y = position_odom[1]
    t.transform.translation.z = 0
    q = tf.transformations.quaternion_from_euler(0,0,0)
    t.transform.rotation.x = q[0]
    t.transform.rotation.y = q[1]
    t.transform.rotation.z = q[2]
    t.transform.rotation.w = q[3]
    return t

if __name__ == '__main__':
    rospy.init_node("dynamic_tf_broadcaster")
    rate = rospy.Rate(100)

    while not rospy.is_shutdown():
        odom_to_base_footprint = calculate_tf()
        #broadcasting transform
        br.sendTransform(odom_to_base_footprint)
        rate.sleep()
