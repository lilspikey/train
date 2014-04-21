#include <TimerOne.h>
#include "track_sensor.h"
#include "throttle.h"
#include "protocol.h"

#define ANALOG_0 0
#define PIN_7 7

#define THROTTLE_POWER 9
#define THROTTLE_FWD 8
#define THROTTLE_BCK 7


#define PWM_HZ 32000

Throttle throttle(THROTTLE_POWER, THROTTLE_FWD, THROTTLE_BCK);
//TrackSensor sensor1(ANALOG_0, PIN_7, 30);

Protocol protocol(Serial);

void throttle_fwd(int power) {
  throttle.forward();
  throttle.set_power(power);
  protocol.log("throttle fwd");
}

void throttle_rev(int power) {
  throttle.reverse();
  throttle.set_power(power);
  protocol.log("throttle bck");
}

void setup() {
  Serial.begin(9600);
  protocol.log("Setup started");
  Timer1.initialize(1e6/PWM_HZ);
  protocol.set_throttle_fwd(throttle_fwd);
  protocol.set_throttle_rev(throttle_rev);
  protocol.log("Setup complete");
} 

void loop() {
  while ( Serial.available() > 0 ) {
    protocol.receive();
  }
  throttle.update();
}
