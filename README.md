# robot_kinetics_pkgs
ROS packages about robot kinetics(get center of gravity etc..)

# packages and nodes
- robot_kinetics  
├ cog_publisher_node  
├ foot_publisher_node  
- gazebo_robot_kinetics  
├ from_contact_state_to_wrench_stamped_node    
## cog_publisher_node  
calculate center of gravity from /robot_description parameters and /tf topic  

#### topics and parameters  

##### parameters  
- /robot_description  
type : string     
- ~publish_frame  
type : string  
default : base_link   
- ~publish_rate  
type : int  
default: 50  

##### subscribe topics  
- /tf  
message_type :
[tf2_msgs/TFMessage](http://docs.ros.org/jade/api/tf2_msgs/html/msg/TFMessage.html)  

##### publish topics  
- /cog/links  
message type : [sensor_msgs/PointCloud](http://docs.ros.org/api/sensor_msgs/html/msg/PointCloud.html)  
center of gravity in each link
- /cog/robot  
message type :
[geometry_msgs/PointStamped](http://docs.ros.org/jade/api/geometry_msgs/html/msg/PointStamped.html)  
center of gravity in whole robot  

## foot_state_publisher_node  
A ROS node for publishing foot state.  

#### topics and parameters  
##### parameters  
- config_filename  
type:string  
- foot_id  
type:int (if LEFT=0,RIGHT=1)  
- ~publish_frame  
type : string  
default : base_link   

##### subscribe topics  
- /tf  
message_type :
[tf2_msgs/TFMessage](http://docs.ros.org/jade/api/tf2_msgs/html/msg/TFMessage.html)  

##### publish topics  
- ~/foot_state/corner_points  
message type : [sensor_msgs/PointCloud](http://docs.ros.org/api/sensor_msgs/html/msg/PointCloud.html)  
corner points of support area   
- ~/foot_state/polygon  
publish support area foot polygon    
message_type : [geometry_msgs/PolygonStamped](http://docs.ros.org/api/geometry_msgs/html/msg/PolygonStamped.html)  
- ~/foot_state  
message_type : robot_kinetics/FootState  
publish foot_state

## from_contact_state_to_wrench_stamped_node  
A ROS node for converting gazebo/ContactsState message to geometry_msgs/WrenchStamped message  
#### topics and parameters  

##### parameters  
##### subscribe topics  
-  /robot/contact_states  
message_type : [gazebo_msgs/ContactsState](http://docs.ros.org/jade/api/gazebo_msgs/html/msg/ContactsState.html)
##### publish topics  
- ~/wrentch_stamped  
message_type : [geometry_msgs/WrenchStamped](http://docs.ros.org/jade/api/geometry_msgs/html/msg/WrenchStamped.html)  
