#include "solenoid.h"
#include <Arduino.h>


Solenoid::Solenoid(int pin)
  : _pin(pin), _active(false), _prevMillis(0) {
  pinMode(_pin, OUTPUT);  
}


void Solenoid::activate() {
  _active = true;
  digitalWrite(_pin, HIGH);
  _prevMillis = millis();
}


void Solenoid::update() {
  if ( _active ) {
    unsigned long duration = millis() - _prevMillis;
    if (duration >= 250) {
      digitalWrite(_pin, LOW);
      _active = false;
    }
  }
}

