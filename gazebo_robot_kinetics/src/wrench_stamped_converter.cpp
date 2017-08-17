#include <wrench_stamped_converter.h>

wrench_stamped_converter::wrench_stamped_converter()
{
  ros::NodeHandle nh;
  wrench_stamped_pub = nh.advertise<geometry_msgs::WrenchStamped>(ros::this_node::getName()+"/wrentch_stamped", 1);
  contact_states_sub = nh.subscribe("/robot/contact_states", 1, &wrench_stamped_converter::publish_wrench_stamped, this);
}

wrench_stamped_converter::~wrench_stamped_converter()
{

}

void wrench_stamped_converter::publish_wrench_stamped(const gazebo_msgs::ContactsState& contact_states)
{
  geometry_msgs::WrenchStamped wrench_stamped_msg;
  //update header
  wrench_stamped_msg.header.frame_id = contact_states.header.frame_id;
  wrench_stamped_msg.header.stamp = ros::Time::now();
  double num_states = (double)contact_states.states.size();
  //iterate each state
  for(auto state = contact_states.states.begin(); state != contact_states.states.end(); ++state)
  {
    wrench_stamped_msg.wrench.force.x = state->total_wrench.force.x + wrench_stamped_msg.wrench.force.x/num_states;
    wrench_stamped_msg.wrench.force.y = state->total_wrench.force.y + wrench_stamped_msg.wrench.force.y/num_states;
    wrench_stamped_msg.wrench.force.z = state->total_wrench.force.z + wrench_stamped_msg.wrench.force.z/num_states;
    wrench_stamped_msg.wrench.torque.x = state->total_wrench.torque.x + wrench_stamped_msg.wrench.torque.x/num_states;
    wrench_stamped_msg.wrench.torque.y = state->total_wrench.torque.y + wrench_stamped_msg.wrench.torque.y/num_states;
    wrench_stamped_msg.wrench.torque.z = state->total_wrench.torque.z + wrench_stamped_msg.wrench.torque.z/num_states;
  }
  wrench_stamped_pub.publish(wrench_stamped_msg);
}
