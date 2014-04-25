#include "solenoid.h"
#include <Arduino.h>


Solenoid::Solenoid(int pin, int durationMillis)
  : _pin(pin), _active(false), _durationMillis(durationMillis), _prevMillis(0) {
  pinMode(_pin, OUTPUT);  
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

void Solenoid::update() {
  if ( _active ) {
    unsigned long duration = millis() - _prevMillis;
    if (duration >= _durationMillis) {
      deactivate();
    }
  }
}

