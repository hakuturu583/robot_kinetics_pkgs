# robot_kinetics_pkgs
ROS packages about robot kinetics(get center of gravity etc..)

# packages and nodes
- robot_kinetics  
├ cog_publisher_node  
## cog_publisher_node  
calculate center of gravity from /robot_description parameters and /tf topic  
#### topics and parameters  
##### parameters  
- /robot_description  
type : string     
- /publish_frame  
type : string  
default : base_link   
- /publish_rate  
type : int  
default: 50  
##### subscribe topics  
- /tf  
##### publish topics  
- /cog/links  
message type : [sensor_msgs/PointCloud](http://docs.ros.org/api/sensor_msgs/html/msg/PointCloud.html)  
center of gravity in each link
- /cog/robot  
message type :
[geometry_msgs/PointStamped](http://docs.ros.org/jade/api/geometry_msgs/html/msg/PointStamped.html)  
