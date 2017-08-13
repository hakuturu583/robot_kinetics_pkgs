//headers in this package
#include <cog_publisher.h>

//headers for standard library
#include<iostream>
#include<fstream>

//headers for ROS
#include <ros/ros.h>
#include <ros/package.h>

//headers for urdf parser
#include <kdl_parser/kdl_parser.hpp>

cog_publisher::cog_publisher()
{
  std::string robot_description_text;
  //get robot_description parameter
  nh.getParam("/robot_description", robot_description_text);
  KDL::Tree robot_tree;
  //parse urdf by using kdl_parser
  kdl_parser::treeFromString(robot_description_text, robot_tree);
  std::map<std::string,KDL::TreeElement> robot_segment = robot_tree.getSegments();
  for(auto itr = robot_segment.begin(); itr != robot_segment.end(); ++itr)
  {
    //get link name from std::map
    std::string link_name = itr->first;
    //get link parameters
    KDL::RigidBodyInertia rigid_body_inertia = itr->second.segment.getInertia();
    //get Mass of link
    double mass = rigid_body_inertia.getMass();
    //get Center of Gravity parameters
    KDL::Vector cog_point = rigid_body_inertia.getCOG();
    double cog_point_x = cog_point.x();
    double cog_point_y = cog_point.y();
    double cog_point_z = cog_point.z();
  }
}

cog_publisher::~cog_publisher()
{

}
