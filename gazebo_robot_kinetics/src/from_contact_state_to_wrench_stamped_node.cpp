//headers for ROS
#include <ros/ros.h>
#include <wrench_stamped_converter.h>
#include <gazebo_msgs/ContactsState.h>
#include <geometry_msgs/WrenchStamped.h>

int main(int argc, char *argv[])
{
  ros::init(argc, argv, "from_contact_state_to_wrench_stamped_node");
  wrench_stamped_converter converter;
  ros::spin();
  return 0;
}
