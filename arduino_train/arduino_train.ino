#include <TimerOne.h>
#include "track_sensor.h"
#include "throttle.h"
#include "solenoid.h"
#include "turnout.h"
#include "protocol.h"
#include "flash_string.h"

#define SENSOR_ON1 2
#define SENSOR_ON2 3

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

// sensors are turned on and off by a pair of transistors
// so share pins for output, but each has own pin for input (obviously)
TrackSensor sensor1(0, SENSOR_ON1);
TrackSensor sensor2(1, SENSOR_ON2);
TrackSensor sensor3(2, SENSOR_ON1);
TrackSensor sensor4(3, SENSOR_ON2);
TrackSensor sensor5(4, SENSOR_ON1);
TrackSensor sensor6(5, SENSOR_ON2);

Protocol protocol(Serial);

int free_ram () {
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}

void handle_command(protocol_cmd cmd, unsigned int arg) {
  protocol.log(FS("handle_command"));
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
  protocol.log(FS("Setup started"));
  Timer1.initialize(1e6/PWM_HZ);
  protocol.set_cmd_handler(handle_command);
  protocol.log(FS("Setup complete"));
  turnout.left();
}

void checkSensor(TrackSensor& sensor, const FlashString& name) {
  if ( sensor.update() ) {
    protocol.status(name, sensor.isTriggered());  
  }
}

void loop() {
  for ( int i = 0; i < 16 && Serial.available() > 0; i++ ) {
    protocol.receive();
  }
  if ( throttle.update() ) {
    protocol.status(FS("forward"), throttle.isForward());
    protocol.status(FS("power"), throttle.getPower());
  }
  if ( turnout.update() ) {
    protocol.status(FS("turnout"), turnout.isDirectionLeft());
  }
  if ( decoupler.update() ) {
    protocol.status(FS("decoupler"), decoupler.isActive());
  }
  checkSensor(sensor1, FS("sensor1"));
  checkSensor(sensor2, FS("sensor2"));
  checkSensor(sensor3, FS("sensor3"));
  checkSensor(sensor4, FS("sensor4"));
  checkSensor(sensor5, FS("sensor5"));
  checkSensor(sensor6, FS("sensor6"));
  //Serial.println(free_ram());
}
