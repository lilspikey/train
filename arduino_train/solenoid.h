#ifndef __SOLENOID__H__
#define __SOLENOID__H__


class Solenoid {
  
  public:
    explicit Solenoid(int pin);
    
    void activate();
    void update();
  
  private:
    int _pin;
    bool _active;
    long _prevMillis;
};

#endif
