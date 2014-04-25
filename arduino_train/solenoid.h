#ifndef __SOLENOID__H__
#define __SOLENOID__H__


class Solenoid {
  
  public:
    explicit Solenoid(int pin, int durationMillis=250);
    
    void activate();
    void deactivate();
    void update();
  
  private:
    int _pin;
    bool _active;
    int _durationMillis;
    long _prevMillis;
};

#endif
