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
Solenoid decoupler(DECOUPLER, 750);

//TrackSensor sensor1(ANALOG_0, PIN_7, 30);

Protocol protocol(Serial);


void handle_command(protocol_cmd cmd, int arg) {
  switch(cmd) {
    case PROTOCOL_CMD_THROTTLE_FWD: {
      throttle.forward();
      throttle.set_power(arg);
      protocol.log("throttle fwd");
    }
    break;
    case PROTOCOL_CMD_THROTTLE_REV: {
      throttle.reverse();
      throttle.set_power(arg);
      protocol.log("throttle bck");
    }
    break;
    case PROTOCOL_CMD_TURNOUT_LEFT: {
      turnoutLeft.activate();
      protocol.log("turnout left");
    }
    break;
    case PROTOCOL_CMD_TURNOUT_RIGHT: {
      turnoutRight.activate();
      protocol.log("turnout right");
    }
    break;
    case PROTOCOL_CMD_DECOUPLER: {
      decoupler.activate();
      protocol.log("decoupler");
    }
    break;
  }
}

void setup() {
  Serial.begin(9600);
  protocol.log("Setup started");
  Timer1.initialize(1e6/PWM_HZ);
  protocol.set_cmd_handler(handle_command);
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
