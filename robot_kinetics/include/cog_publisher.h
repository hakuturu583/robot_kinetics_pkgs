#ifndef COG_PUBLISHER_H_INCLUDED
#define COG_PUBLISHER_H_INCLUDED

//headers in this package
#include <joint.h>

//headers for ROS
#include <ros/ros.h>

class cog_publisher
{
public:
  cog_publisher();
  ~cog_publisher();
private:
  ros::NodeHandle nh;
};
#endif
