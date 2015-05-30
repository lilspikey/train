#ifndef __LIGHT_H__
#define __LIGHT_H__

class Light {
  
  public:
    explicit Light(int pin);
    void on();
    void off();
    bool isOn();
    bool update();
  
  private:
    int _pin;
    bool _on;
    bool _prevOn;
};

#endif
