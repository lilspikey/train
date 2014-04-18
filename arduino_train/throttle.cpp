#include <Arduino.h>
#include <TimerOne.h>
#include "throttle.h"


Throttle::Throttle(int powerPin, int forwardPin, int backwardPin)
 : _powerPin(powerPin),
   _forwardPin(forwardPin),
   _backwardPin(backwardPin),
   _power(0) {
  pinMode(_powerPin, OUTPUT);
  pinMode(_forwardPin, OUTPUT);
  pinMode(_backwardPin, OUTPUT);
  forward();
}

int Throttle::power() {
  return _power; 
}

void Throttle::forward() {
  digitalWrite(_forwardPin, HIGH);
  digitalWrite(_backwardPin, LOW);  
}

void Throttle::reverse() {
  digitalWrite(_forwardPin, LOW);
  digitalWrite(_backwardPin, HIGH); 
}

void Throttle::set_power(int power) {
  Timer1.pwm(_powerPin, power);
}

void Throttle::update() {
  // TODO emulate acceleration
}


