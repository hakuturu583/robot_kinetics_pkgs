#ifndef WRENCH_STAMPED_CONVERTER_H_INCLUDED
#define WRENCH_STAMPED_CONVERTER_H_INCLUDED
//headers for ROS
#include <ros/ros.h>
#include <wrench_stamped_converter.h>
#include <gazebo_msgs/ContactsState.h>
#include <geometry_msgs/WrenchStamped.h>

class wrench_stamped_converter
{
public:
  wrench_stamped_converter();
  ~wrench_stamped_converter();
private:
  void publish_wrench_stamped(const gazebo_msgs::ContactsState& contact_states);
  ros::Publisher wrench_stamped_pub;
  ros::Subscriber contact_states_sub;
};
#endif
