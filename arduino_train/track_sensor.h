#ifndef __TRACK_SENSOR_H__
#define __TRACK_SENSOR_H__

class TrackSensor {
  
  public:
    explicit TrackSensor(int analogPin, int irLEDPin, int difference=50);
    bool update(void);
    bool isTriggered(void);
  
  private:
    int _analogPin;
    int _irLEDPin;
    int _difference;
    int _correctCount;
};

#endif
