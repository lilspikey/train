#include <TimerOne.h>
#include "track_sensor.h"
#include "throttle.h"
#include "solenoid.h"
#include "turnout.h"
#include "protocol.h"

// TODO perhaps try running all sensors from couple of pins
// probably need to use a transistor, to avoid pulling too
// much current on each pin
#define SENSOR_1 2
#define SENSOR_2 3
#define SENSOR_3 10
#define SENSOR_4 11
#define SENSOR_5 12
#define SENSOR_6 13

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
Turnout turnout(turnoutLeft, turnoutRight);
Solenoid decoupler(DECOUPLER, 1000);

TrackSensor sensor1(0, SENSOR_1);
TrackSensor sensor2(1, SENSOR_2);
TrackSensor sensor3(2, SENSOR_3);
TrackSensor sensor4(3, SENSOR_4);
TrackSensor sensor5(4, SENSOR_5);
TrackSensor sensor6(5, SENSOR_6);

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
      turnout.left();
    }
    break;
    case PROTOCOL_CMD_TURNOUT_RIGHT: {
      turnout.right();
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
  turnout.left();
}

void checkSensor(TrackSensor& sensor, const char* name) {
  if ( sensor.update() ) {
    protocol.status(name, sensor.isTriggered());  
  }
}

void loop() {
  for ( int i = 0; i < 16 && Serial.available() > 0; i++ ) {
    protocol.receive();
  }
  if ( throttle.update() ) {
    protocol.status("forward", throttle.isForward());
    protocol.status("power", throttle.getPower());
  }
  if ( turnout.update() ) {
    protocol.status("turnout", turnout.isDirectionLeft());
  }
  if ( decoupler.update() ) {
    protocol.status("decoupler", decoupler.isActive());
  }
  checkSensor(sensor1, "sensor1");
  checkSensor(sensor2, "sensor2");
  checkSensor(sensor3, "sensor3");
  checkSensor(sensor4, "sensor4");
  checkSensor(sensor5, "sensor5");
  checkSensor(sensor6, "sensor6");  
}
