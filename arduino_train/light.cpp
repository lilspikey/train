#include <Arduino.h>
#include "light.h"

Light::Light(int pin)
  : _pin(pin), _on(false), _prevOn(true) {
  pinMode(_pin, OUTPUT);
}

void Light::on() {
  _on = true;
}

void Light::off() {
  _on = false;
}

bool Light::isOn() {
  return _on;
}

bool Light::update() {
  if ( _on != _prevOn ) {
    digitalWrite(_pin, _on? HIGH : LOW);
    _on = _prevOn;
    return true;
  }
  return false;
}


