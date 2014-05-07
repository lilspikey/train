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

#define TURNOUT_LEFT 6
#define TURNOUT_RIGHT 5

#define DECOUPLER 4


//#define PWM_HZ 32000
#define PWM_HZ 60

Throttle throttle(THROTTLE_POWER, THROTTLE_FWD, THROTTLE_BCK);
Solenoid turnoutLeft(TURNOUT_LEFT);
Solenoid turnoutRight(TURNOUT_RIGHT);
Solenoid decoupler(DECOUPLER, 1000);

//TrackSensor sensor1(ANALOG_0, PIN_7, 30);

Protocol protocol(Serial);


void handle_command(protocol_cmd cmd, unsigned int arg) {
  protocol.log("handle_command");
  switch(cmd) {
    case PROTOCOL_CMD_THROTTLE_FWD: {
      throttle.forward();
      throttle.setPower(arg);
    }
    break;
    case PROTOCOL_CMD_THROTTLE_REV: {
      throttle.reverse();
      throttle.setPower(arg);
    }
    break;
    case PROTOCOL_CMD_TURNOUT_LEFT: {
      turnoutLeft.activate();
      turnoutRight.deactivate();
    }
    break;
    case PROTOCOL_CMD_TURNOUT_RIGHT: {
      turnoutRight.activate();
      turnoutLeft.deactivate();
    }
    break;
    case PROTOCOL_CMD_DECOUPLER_UP: {
      decoupler.activate();
    }
    break;
    case PROTOCOL_CMD_DECOUPLER_DOWN: {
      decoupler.deactivate();
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
  if ( throttle.update() ) {
    protocol.status("forward", throttle.isForward());
    protocol.status("power", throttle.getPower());
  }
  if ( turnoutLeft.update() ) {
    protocol.status("turnoutLeft", turnoutLeft.isActive());
  }
  if ( turnoutRight.update() ) {
    protocol.status("turnoutRight", turnoutRight.isActive());
  }
  if ( decoupler.update() ) {
    protocol.status("decoupler", decoupler.isActive());
  }
}
