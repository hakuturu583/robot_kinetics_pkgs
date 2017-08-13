//headers in this package
#include <joint.h>
joint::joint(std::string name,int joint_type,std::string parent_link,std::string child_link)
{
  this->name = name;
  this->joint_type = joint_type;
  this->parent_link = parent_link;
  this->child_link = child_link;
}

joint::~joint()
{

}
