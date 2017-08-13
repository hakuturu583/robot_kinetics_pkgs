#ifndef JOINT_H_INCLUDED
#define JOINT_H_INCLUDED

//define joint types
#define JOINT_REVOLUTE 0
#define JOINT_CONTINOUS 1
#define JOINT_FIXED 2
#define JOINT_FLOATING 3
#define JOINT_PLANAR 4

//headers for std library
#include <string>

class joint
{
public:
  joint(std::string name,int joint_type,std::string parent_link,std::string child_link);
  ~joint();
private:
  std::string name;
  int joint_type;
  std::string parent_link,child_link;
};
#endif
