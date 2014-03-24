#include "track_sensor.h"

#define ANALOG_0 0
#define PIN_7 7

TrackSensor sensor1(ANALOG_0, PIN_7, 30);
 
void setup() {
  Serial.begin(9600);
} 
 
void loop() {
  digitalWrite(9, sensor1.read()? HIGH : LOW);
  delay(1);
} 
