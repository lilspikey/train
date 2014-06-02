#include <Arduino.h>
#include <TimerOne.h>
#include "throttle.h"


Throttle::Throttle(int powerPin, int forwardPin, int backwardPin)
 : _state(THROTTLE_STOPPED),
   _powerPin(powerPin),
   _forwardPin(forwardPin),
   _backwardPin(backwardPin),
   _forward(true),
   _power(0),
   _targetForward(false),
   _targetPower(0),
   _waitCount(0),
   _prevMillis(0) {
  pinMode(_powerPin, OUTPUT);
  pinMode(_forwardPin, OUTPUT);
  pinMode(_backwardPin, OUTPUT);
}

int Throttle::getPower() {
  return _power; 
}

bool Throttle::isForward() {
  return _forward;
}

void Throttle::forward() {
  _targetForward = true;
}

void Throttle::reverse() {
  _targetForward = false;
}

void Throttle::setPower(int power) {
  _targetPower = power;
}

bool Throttle::updatePower(int targetPower) {
  int prevPower = _power;
  int accel = min(500, abs(_power - targetPower));
  _power += (_power < targetPower)? accel : -accel;
  if ( _power != prevPower ) {
    Timer1.pwm(_powerPin, _power);
    return true;
  }
  return false;
}

bool Throttle::update() {
  bool changed = false;
  unsigned long duration = millis() - _prevMillis;
  if ( duration > 50 ) {
    //bool changed = _prevForward != _forward || _prevPower != _power;
    //_prevForward = _forward;
    //_prevPower = _power;
    switch(_state) {
      case THROTTLE_RUNNING: {
        if ( _forward != _targetForward ) {
          changed = true;
          _state = THROTTLE_STOPPING;
        }
        else {
          changed = updatePower(_targetPower);
        }
      }
      break;
      case THROTTLE_STOPPING: {
        changed = updatePower(0);
        if ( !changed ) {
          _waitCount = 10;
          _state = THROTTLE_STOPPED;
        }
      }
      break;
      case THROTTLE_STOPPED: {
        if ( _waitCount > 0 ) {
          _waitCount--;
        }
        else if ( _forward != _targetForward || _power != _targetPower ) {
          changed = true;
          _forward = _targetForward;
          _power = 0;
          digitalWrite(_forwardPin, _forward? HIGH : LOW);
          digitalWrite(_backwardPin, _forward? LOW : HIGH);
          _state = THROTTLE_RUNNING;
          _waitCount = 0;
        }
      }
      break;
    }
    _prevMillis = millis();
  }
  
  return changed;
}


