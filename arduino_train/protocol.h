#ifndef __PROTOCOL_H__
#define __PROTOCOL_H__

#include <Arduino.h>

// use PPP frame format
static const int FRAME_START_BYTE = 0x7E;
static const int FRAME_ESCAPE_BYTE = 0x7D;
static const int FRAME_ESCAPE_MASK = 0x20;
static const int FRAME_END_BYTE = 0x7E;


typedef enum {
  FRAME_READY, FRAME_STARTED, FRAME_ESCAPING
} frame_state;


typedef enum {
  FRAME_BEGIN, FRAME_DATA, FRAME_NO_DATA, FRAME_END
} frame_event;


class FrameEvent {
  public:
    explicit FrameEvent(frame_event e, char b);
    frame_event event; 
    char data;
};


class Frame {
  public:
    explicit Frame(Stream& stream);
    FrameEvent receive();
    void begin();
    void write(char c);
    void end();
    
  private:
    Stream& _stream;
    frame_state _state;
};


typedef enum {
  PROTOCOL_READY, PROTOCOL_READ_CMD, PROTOCOL_READ_ARG
} protocol_state;


typedef enum {
  PROTOCOL_CMD_LOG = 1,
  PROTOCOL_CMD_STATUS = 2,
  PROTOCOL_CMD_THROTTLE_FWD = 3,
  PROTOCOL_CMD_THROTTLE_REV = 4,
  PROTOCOL_CMD_TURNOUT_LEFT = 5,
  PROTOCOL_CMD_TURNOUT_RIGHT = 6,
  PROTOCOL_CMD_DECOUPLER_UP = 7,
  PROTOCOL_CMD_DECOUPLER_DOWN = 8
} protocol_cmd;


class Protocol {
  public:
    explicit Protocol(Stream& stream);
    void receive();
    void log(const String& msg);
    void status(const String& key, unsigned int value);
    void set_cmd_handler(void (*cmd_handler)(protocol_cmd, unsigned int)) { _cmd_handler = cmd_handler; };
  
  protected:
    void received(protocol_cmd cmd, unsigned int arg);
    void write(const String& msg);
    void write(unsigned int value);
  
  private:
    Frame _frame;
    protocol_state _state;
    protocol_cmd _cmd;
    int _arg;
    void (*_cmd_handler)(protocol_cmd, unsigned int);
};

#endif
