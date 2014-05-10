#ifndef __TURNOUT__H__
#define __TURNOUT__H__

#include "solenoid.h"

class Turnout {
  
  public:
    explicit Turnout(Solenoid& left, Solenoid& right);
    
    bool isDirectionLeft();
    void left();
    void right();
    bool update();
  
  private:
    Solenoid& _left;
    Solenoid& _right;
    bool _dirLeft;
};

#endif
