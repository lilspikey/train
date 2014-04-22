#include <TimerOne.h>
#include "track_sensor.h"
#include "throttle.h"
#include "solenoid.h"
#include "protocol.h"

#define ANALOG_0 0
#define PIN_7 7

#define THROTTLE_POWER 9
#define THROTTLE_FWD 8
#define THROTTLE_BCK 7

#define TURNOUT_LEFT 2
#define TURNOUT_RIGHT 4

#define DECOUPLER 12


#define PWM_HZ 32000

Throttle throttle(THROTTLE_POWER, THROTTLE_FWD, THROTTLE_BCK);
Solenoid turnoutLeft(TURNOUT_LEFT);
Solenoid turnoutRight(TURNOUT_RIGHT);
Solenoid decoupler(DECOUPLER);

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
  for ( int i = 0; i < 16 && Serial.available() > 0; i++ ) {
    protocol.receive();
  }
  throttle.update();
  turnoutLeft.update();
  turnoutRight.update();
  decoupler.update();
}
