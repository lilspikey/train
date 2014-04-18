#include <TimerOne.h>
#include "track_sensor.h"
#include "throttle.h"

#define ANALOG_0 0
#define PIN_7 7

#define THROTTLE_POWER 9
#define THROTTLE_FWD 8
#define THROTTLE_BCK 7


#define PWM_HZ 32000

Throttle throttle(THROTTLE_POWER, THROTTLE_FWD, THROTTLE_BCK);
//TrackSensor sensor1(ANALOG_0, PIN_7, 30);
 
void setup() {
  Serial.begin(9600);
  Timer1.initialize(1e6/PWM_HZ);
} 
 
void loop() {
  for ( int i = 0; i < 1024; i++ ) {
    throttle.set_power(i);
    delay(10);
  }
  delay(250);
} 
