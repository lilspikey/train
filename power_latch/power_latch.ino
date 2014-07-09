#define PIN_POWER_ON 3
#define PIN_BUTTON 4

void setup() {
  pinMode(PIN_POWER_ON, OUTPUT);
  pinMode(PIN_BUTTON, INPUT);
  digitalWrite(PIN_BUTTON, HIGH);
}

void loop() {
  digitalWrite(PIN_POWER_ON, HIGH);
  if ( digitalRead(PIN_BUTTON) == LOW ) {
    delay(500);
    if ( digitalRead(PIN_BUTTON) == LOW ) {
      while( digitalRead(PIN_BUTTON) != HIGH ) {
        delay(10);
      }
      digitalWrite(PIN_POWER_ON, LOW);
      delay(1000);
    }
  }
  delay(50);
}
