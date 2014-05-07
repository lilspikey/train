#ifndef __SOLENOID__H__
#define __SOLENOID__H__


class Solenoid {
  
  public:
    explicit Solenoid(int pin, int durationMillis=250);
    
    bool isActive();
    void activate();
    void deactivate();
    bool update();
  
  private:
    int _pin;
    bool _active;
    bool _prevActive;
    int _durationMillis;
    long _prevMillis;
};

#endif
