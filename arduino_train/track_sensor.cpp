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

bool TrackSensor::update(void) {
  bool prevTriggered = isTriggered();
  digitalWrite(_irLEDPin, HIGH);
  delayMicroseconds(500 + random(700));
  int readingOn = analogRead(_analogPin);

  digitalWrite(_irLEDPin, LOW);
  delayMicroseconds(500 + random(700));
  int readingOff = analogRead(_analogPin);
  
  int difference = readingOff - readingOn;
  if ( difference > _difference ) {
    if ( _correctCount < CORRECT_THRESHOLD ) {
      _correctCount++;
    }  
  }
  else {
    _correctCount = 0;
  }
  return prevTriggered != isTriggered();
}

bool TrackSensor::isTriggered(void) {
  return _correctCount >= CORRECT_THRESHOLD;
}
