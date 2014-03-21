#ifndef __TRACK_SENSOR_H__
#define __TRACK_SENSOR_H__

class TrackSensor {
  
  public:
    TrackSensor(int analogPin, int irLEDPin, int threshold);
    bool read(void);
  
  private:
    int _analogPin;
    int _irLEDPin;
    int _threshold;
    int _correctCount;
  
};

#endif
