#define PIN_POWER_ON 3
#define PIN_BUTTON 4
#define PIN_SHUTDOWN 1
#define PIN_SHUTDOWN_ACKNOWLEDGED 2
#define PIN_LED 0

typedef enum {
  INIT,
  POWER_ON,
  POWER,
  POWER_BUTTON_PRESSED,
  SEND_SHUTDOWN,
  SHUTDOWN
} STATE;

STATE state = INIT;

void setup() {
  pinMode(PIN_POWER_ON, OUTPUT);
  pinMode(PIN_SHUTDOWN, OUTPUT);
  pinMode(PIN_LED, OUTPUT);
  
  pinMode(PIN_BUTTON, INPUT);
  digitalWrite(PIN_BUTTON, HIGH);
  
  pinMode(PIN_SHUTDOWN_ACKNOWLEDGED, INPUT);
  digitalWrite(PIN_SHUTDOWN_ACKNOWLEDGED, HIGH);
  
  digitalWrite(PIN_POWER_ON, LOW);
  digitalWrite(PIN_SHUTDOWN, HIGH);
}

bool isPinStateMatching(int pin, int state) {
  if ( digitalRead(pin) == state ) {
    delay(50);
    if ( digitalRead(pin) == state ) {
      return true;
    }
  }
  return false;
}

bool isButtonDown() {
  return isPinStateMatching(PIN_BUTTON, LOW);
}

bool isButtonUp() {
  return isPinStateMatching(PIN_BUTTON, HIGH);
}

bool isAcknowledgeHigh() {
  return isPinStateMatching(PIN_SHUTDOWN_ACKNOWLEDGED, HIGH);
}

bool isAcknowledgeLow() {
  return isPinStateMatching(PIN_SHUTDOWN_ACKNOWLEDGED, LOW);
}

void flashLED() {
  digitalWrite(PIN_LED, HIGH);
  delay(500);
  digitalWrite(PIN_LED, LOW);
  delay(500);
}

void loop() {
  switch(state) {
    case INIT: {
      // confirm that button pressed before
      // we actually power on
      if ( isButtonDown() ) {
        state = POWER_ON;
      }
    }
    break;
    case POWER_ON: {
      // once we've applied power we need to make sure 
      // that button goes up again before we listen out
      // for button press again
      digitalWrite(PIN_POWER_ON, HIGH);
      if ( isButtonUp() ) {
        // until we get acknowledgement
        // that RPi is up we'll flash LED
        if ( !isAcknowledgeHigh() ) {
          flashLED();
        }
        else {
          state = POWER;
        }
      }
    }
    break;
    case POWER: {
      // fully powered on, so turn on LED
      // and wait for button to be pressed
      digitalWrite(PIN_LED, HIGH);
      if ( isButtonDown() ) {
        state = POWER_BUTTON_PRESSED;
      }
    }
    break;
    case POWER_BUTTON_PRESSED: {
      // now that button is pressed we'll
      // wait till it's released again
      if ( isButtonUp() ) {
        state = SEND_SHUTDOWN;
      }
    }
    break;
    case SEND_SHUTDOWN: {
      // now wait for RPi to signal it has shutdown
      digitalWrite(PIN_SHUTDOWN, LOW);
      if ( !isAcknowledgeLow() ) {
        flashLED();
      }
      else {
        state = SHUTDOWN;
      }
    }
    break;
    case SHUTDOWN: {
      digitalWrite(PIN_LED, LOW);
      digitalWrite(PIN_POWER_ON, LOW);
    }
    break;
  }
  delay(10);
}
