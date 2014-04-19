#ifndef __PROTOCOL_H__
#define __PROTOCOL_H__

// use PPP frame format
static const int START_BYTE = 0x7E;
static const int ESCAPE_BYTE = 0x7D;
static const int ESCAPE_MASK = 0x20;
static const int END_BYTE = 0x7E;


typedef enum {
  READY, IN_FRAME, IN_ESCAPE
} frame_state;


typedef enum {
  FRAME_START, DATA, NO_DATA, FRAME_END
} frame_event;


class FrameEvent {
  public:
    explicit FrameEvent(frame_event e, char b);
    frame_event event; 
    char data;
};


class FrameParser {
  public:
    explicit FrameParser();
    FrameEvent processByte(char b);
    
  private:
    frame_state _state;
};


#endif
