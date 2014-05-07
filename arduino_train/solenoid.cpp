#include "solenoid.h"
#include <Arduino.h>


Solenoid::Solenoid(int pin, int durationMillis)
  : _pin(pin), _active(false), _prevActive(true), _durationMillis(durationMillis), _prevMillis(0) {
  pinMode(_pin, OUTPUT);  
}

bool Solenoid::isActive() {
  return _active;
}

void Solenoid::activate() {
  _active = true;
  digitalWrite(_pin, HIGH);
  _prevMillis = millis();
}

void Solenoid::deactivate() {
  digitalWrite(_pin, LOW);
  _active = false;
}

bool Solenoid::update() {
  if ( _active ) {
    unsigned long duration = millis() - _prevMillis;
    if (duration >= _durationMillis) {
      deactivate();
    }
  }
  
  bool changed = _prevActive != _active;
  _prevActive = _active;
  return changed;
}

