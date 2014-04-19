#include "protocol.h"


FrameEvent::FrameEvent(frame_event e, char b) 
  : event(e), data(b) {}


FrameParser::FrameParser()
  : _state(READY) {}


FrameEvent FrameParser::processByte(char b) {
  char data;
  frame_event event = NO_DATA;
  switch(_state) {
    case READY: {
      if ( b == START_BYTE ) {
        _state = IN_FRAME;
        event = FRAME_START;
      }
    }
    break;
    case IN_FRAME: {
      if ( b == ESCAPE_BYTE ) {
        _state = IN_ESCAPE;
      }
      else if ( b == END_BYTE ) {
        _state = READY;
        event = FRAME_END;
      }
      else {
        event = DATA;
        data = b;
      }
    }
    break;
    case IN_ESCAPE: {
      _state = IN_FRAME;
      event = DATA;
      data = b ^ ESCAPE_MASK;
    }
    break;
  }
  return FrameEvent(event, data);
}

