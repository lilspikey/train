#include <Arduino.h>
#include <TimerOne.h>
#include "throttle.h"


Throttle::Throttle(int powerPin, int forwardPin, int backwardPin)
 : _powerPin(powerPin),
   _forwardPin(forwardPin),
   _backwardPin(backwardPin),
   _forward(true),
   _power(0),
   _prevForward(false),
   _prevPower(0) {
  pinMode(_powerPin, OUTPUT);
  pinMode(_forwardPin, OUTPUT);
  pinMode(_backwardPin, OUTPUT);
  forward();
}

int Throttle::getPower() {
  return _power; 
}

bool Throttle::isForward() {
  return _forward;
}

void Throttle::forward() {
  _forward = true;
  digitalWrite(_forwardPin, HIGH);
  digitalWrite(_backwardPin, LOW);  
}

void Throttle::reverse() {
  _forward = false;
  digitalWrite(_forwardPin, LOW);
  digitalWrite(_backwardPin, HIGH); 
}

void Throttle::setPower(int power) {
  _power = power;
  Timer1.pwm(_powerPin, power);
}

bool Throttle::update() {
  // TODO emulate acceleration
  bool changed = _prevForward != _forward || _prevPower != _power;
  _prevForward = _forward;
  _prevPower = _power;
  
  return changed;
}


