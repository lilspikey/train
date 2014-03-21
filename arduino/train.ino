#include "track_sensor.h"

#define ANALOG_0 0
#define PIN_7 7

TrackSensor sensor1(ANALOG_0, PIN_7, 920);
 
void setup() {
  Serial.begin(9600);
} 
 
void loop() {
  for ( int i = 0; i < 10; i++ ) {
    sensor1.read();
  }
  if ( sensor1.read() ) {
    Serial.println("ON");
  }
  else {
    Serial.println("");
  }
  delay(250);
} 
