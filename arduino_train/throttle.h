#ifndef __THROTTLE_H__
#define __THROTTLE_H__

typedef enum {
  THROTTLE_RUNNING,
  THROTTLE_STOPPING,
  THROTTLE_STOPPED
} throttle_state;

/**
 * Simple class to handle controlling throttle for train via a h-bridge.
 * Potentially this will also simulate gradual acceleration etc
 **/
class Throttle {
  
  public:
    explicit Throttle(int powerPin, int forwardPin, int backwardPin);
    int getPower();
    void setPower(int power);
    bool isForward();
    void forward();
    void reverse();
    bool update();
  
  private:
    bool updatePower(int targetPower);
  
    throttle_state _state;
    int _powerPin;
    int _forwardPin;
    int _backwardPin;
    bool _forward;
    int _power;
    bool _targetForward;
    int _targetPower;
    int _waitCount;
    long _prevMillis;
};

#endif
