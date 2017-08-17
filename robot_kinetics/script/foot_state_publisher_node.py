#!/usr/bin/env python
from robot_kinetics.msg import FootStateStamped
#import xml parser
import xml.etree.ElementTree as ET
#import ros modules
import rospkg
import rospy
import tf2_ros
import tf2_geometry_msgs
#import ros messages
from geometry_msgs.msg import Point32,PointStamped,PolygonStamped,WrenchStamped
from sensor_msgs.msg import PointCloud

class foot_state_publisher:
    def __init__(self):
        #create tf listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        rospack = rospkg.RosPack()
        #define publisher
        self.corner_points_pub = rospy.Publisher(rospy.get_name()+"/foot_state/corner_points",PointCloud,queue_size=1)
        self.polygon_pub = rospy.Publisher(rospy.get_name()+"/foot_state/polygon",PolygonStamped,queue_size=1)
        self.foot_state_pub = rospy.Publisher(rospy.get_name()+"/foot_state",FootStateStamped,queue_size=1)
        self.foot_state_msg = FootStateStamped()
        #get parameters
        self.foot_state_msg.foot_state.foot_id = rospy.get_param(rospy.get_name()+"/foot_id")
        config_filename = rospy.get_param(rospy.get_name()+"/config_filename")
        self.publish_frame = rospy.get_param(rospy.get_name()+"/publish_frame","base_link")
        #parse config xml files
        tree = ET.parse(rospack.get_path('robot_kinetics')+'/config/'+config_filename)
        root = tree.getroot()
        self.corner_points_raw = []
        self.corner_points_transformed = []
        #parse xml files and input data into self.corner_points_raw list
        for point in root:
            corner_point = PointStamped()
            corner_point.header.frame_id = point.attrib["frame_id"]
            corner_point.header.stamp = rospy.Time.now()
            corner_point.point.x = float(point.attrib["x"])
            corner_point.point.y = float(point.attrib["y"])
            corner_point.point.z = float(point.attrib["z"])
            self.corner_points_raw.append(corner_point)
        self.wrentch_sub = rospy.Subscriber(rospy.get_name()+"/wrench_stamped", WrenchStamped, self.wrentch_callback)
    def wrentch_callback(self,data):
        self.foot_state_msg.foot_state.state = self.foot_state_msg.foot_state.SUPPORT_LEG
        if data.wrench.force.x == 0.0:
            if data.wrench.force.y == 0.0:
                if data.wrench.force.z == 0.0:
                    if data.wrench.torque.x == 0.0:
                        if data.wrench.torque.y == 0.0:
                            if data.wrench.torque.z == 0.0:
                                self.foot_state_msg.foot_state.state = self.foot_state_msg.foot_state.NOT_SUPPORT_LEG
    def transform_to_publish_frame(self):
        self.corner_points_transformed = []
        if self.foot_state_msg.foot_state.state == self.foot_state_msg.foot_state.SUPPORT_LEG:
            num_corner_points = len(self.corner_points_raw)
            for i in range(num_corner_points):
                try:
                    #transform to self.publish_frame
                    transform = self.tf_buffer.lookup_transform(self.publish_frame, self.corner_points_raw[i].header.frame_id, rospy.Time(0))
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
        polygon_msg = PolygonStamped()
        pointcloud_msg = PointCloud()
        pointcloud_msg.header.frame_id = self.publish_frame
        pointcloud_msg.header.stamp = rospy.Time.now()
        pointcloud_msg.points = self.corner_points_transformed
        self.corner_points_pub.publish(pointcloud_msg)
        polygon_msg.header = pointcloud_msg.header;
        polygon_msg.polygon.points = self.corner_points_transformed
        self.foot_state_msg.foot_state.polygon.points = self.corner_points_transformed
        self.polygon_pub.publish(polygon_msg)
        self.foot_state_pub.publish(self.foot_state_msg)

if __name__ == '__main__':
    rospy.init_node("foot_state_publisher",anonymous=True)
    rate = rospy.Rate(50)
    publisher = foot_state_publisher()
    while not rospy.is_shutdown():
        if publisher.transform_to_publish_frame():
            publisher.publish()
        rate.sleep()
