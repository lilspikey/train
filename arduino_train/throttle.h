#ifndef __THROTTLE_H__
#define __THROTTLE_H__

/**
 * Simple class to handle controlling throttle for train via a h-bridge.
 * Potentially this will also simulate gradual acceleration etc
 **/
class Throttle {
  
  public:
    explicit Throttle(int powerPin, int forwardPin, int backwardPin);
    int power();
    void set_power(int power);
    void forward();
    void reverse();
    void update();
  
  private:
    int _powerPin;
    int _forwardPin;
    int _backwardPin;
    int _power;
  
};

#endif
