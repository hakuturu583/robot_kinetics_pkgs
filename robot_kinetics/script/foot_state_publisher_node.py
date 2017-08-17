#!/usr/bin/env python
import xml.etree.ElementTree as ET
import rospkg
from geometry_msgs.msg import Point32,PointStamped,PolygonStamped
from sensor_msgs.msg import PointCloud
import rospy
import tf2_ros
import tf2_geometry_msgs

class foot_state_publisher:
    def __init__(self):
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        rospack = rospkg.RosPack()
        #define publisher
        self.foot_state_pub = rospy.Publisher(rospy.get_name()+"/foot_state/corner_points",PointCloud,queue_size=1)
        #parse config xml files
        config_filename = rospy.get_param(rospy.get_name()+"/config_filename")
        tree = ET.parse(rospack.get_path('robot_kinetics')+'/config/'+config_filename)
        root = tree.getroot()
        self.corner_points_raw = []
        self.corner_points_transformed = []
        for point in root:
            corner_point = PointStamped()
            corner_point.header.frame_id = point.attrib["frame_id"]
            corner_point.header.stamp = rospy.Time.now()
            corner_point.point.x = float(point.attrib["x"])
            corner_point.point.y = float(point.attrib["y"])
            corner_point.point.z = float(point.attrib["z"])
            self.corner_points_raw.append(corner_point)
    def transform_to_base_link(self):
        self.corner_points_transformed = []
        num_corner_points = len(self.corner_points_raw)
        for i in range(num_corner_points):
            try:
                transform = self.tf_buffer.lookup_transform("base_link", self.corner_points_raw[i].header.frame_id, rospy.Time(0))
                corner_point_ransformed = tf2_geometry_msgs.do_transform_point(self.corner_points_raw[i], transform)
                corner_point_ransformed_point32 = Point32()
                corner_point_ransformed_point32.x = corner_point_ransformed.point.x
                corner_point_ransformed_point32.y = corner_point_ransformed.point.y
                corner_point_ransformed_point32.z = corner_point_ransformed.point.z
                self.corner_points_transformed.append(corner_point_ransformed_point32)
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                return False
        return True
    def publish(self):
        pointcloud_msg = PointCloud()
        pointcloud_msg.header.frame_id = "base_link"
        pointcloud_msg.header.stamp = rospy.Time.now()
        pointcloud_msg.points = self.corner_points_transformed
        self.foot_state_pub.publish(pointcloud_msg)


if __name__ == '__main__':
    rospy.init_node("foot_state_publisher",anonymous=True)
    rate = rospy.Rate(50)
    publisher = foot_state_publisher()
    while not rospy.is_shutdown():
        if publisher.transform_to_base_link():
            publisher.publish()
        rate.sleep()
