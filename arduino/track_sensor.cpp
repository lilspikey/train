#include <Arduino.h>
#include "track_sensor.h"

#define CORRECT_THRESHOLD 10

TrackSensor::TrackSensor(int analogPin, int irLEDPin, int threshold)
 : _analogPin(analogPin),
   _irLEDPin(irLEDPin),
   _threshold(threshold),
   _correctCount(0) {
  pinMode(irLEDPin, OUTPUT);
}

bool TrackSensor::read(void) {
  digitalWrite(_irLEDPin, HIGH);
  delay(1 + random(4));
  bool onCorrect = analogRead(_analogPin) <= _threshold;
  digitalWrite(_irLEDPin, LOW);
  delay(1);
  bool offCorrect = analogRead(_analogPin) > _threshold;
  
  if ( onCorrect && offCorrect ) {
    if ( _correctCount < CORRECT_THRESHOLD ) {
      _correctCount++;
    }  
  }
  else {
    _correctCount = 0;
  }  
  return _correctCount >= CORRECT_THRESHOLD;
}
