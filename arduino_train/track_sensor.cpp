#include <Arduino.h>
#include "track_sensor.h"

#define CORRECT_THRESHOLD 10

TrackSensor::TrackSensor(int analogPin, int irLEDPin, int difference)
 : _analogPin(analogPin),
   _irLEDPin(irLEDPin),
   _difference(difference),
   _correctCount(0) {
  pinMode(irLEDPin, OUTPUT);
}

bool TrackSensor::read(void) {
  digitalWrite(_irLEDPin, HIGH);
  delayMicroseconds(500 + random(700));
  int readingHigh = analogRead(_analogPin);
  digitalWrite(_irLEDPin, LOW);
  delayMicroseconds(500 + random(700));
  int readingLow = analogRead(_analogPin);
  
  int difference = readingLow - readingHigh;
  
  if ( difference > _difference ) {
    if ( _correctCount < CORRECT_THRESHOLD ) {
      _correctCount++;
    }  
  }
  else {
    _correctCount = 0;
  }  
  return _correctCount >= CORRECT_THRESHOLD;
}
