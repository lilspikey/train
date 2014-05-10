#include "turnout.h"


Turnout::Turnout(Solenoid& left, Solenoid& right)
 : _left(left), _right(right), _dirLeft(false) {

}

bool Turnout::isDirectionLeft() {
  return _dirLeft; 
}

void Turnout::left() {
  _dirLeft = true;
  _left.activate(); 
}

void Turnout::right() {
  _dirLeft = false;
  _right.activate(); 
}

bool Turnout::update() {
  bool left = _left.update();
  bool right = _right.update();
  return left || right; 
}
