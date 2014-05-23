#include "protocol.h"


FrameEvent::FrameEvent(frame_event e, char b) 
  : event(e), data(b) {}


Frame::Frame(Stream& stream)
  : _stream(stream), _state(FRAME_READY) {}


void Frame::begin() {
  _stream.write(FRAME_START_BYTE);
}

void Frame::write(char b) {
  switch(b) {
    case FRAME_START_BYTE:
    case FRAME_ESCAPE_BYTE: {
      b ^= FRAME_ESCAPE_MASK;
      _stream.write(FRAME_ESCAPE_BYTE);
    }
    break;
  }
  _stream.write(b);
}

void Frame::end() {
  _stream.write(FRAME_END_BYTE);
}

FrameEvent Frame::receive() {
  char b = _stream.read();
  char data;
  frame_event event = FRAME_NO_DATA;
  switch(_state) {
    case FRAME_READY: {
      if ( b == FRAME_START_BYTE ) {
        _state = FRAME_STARTED;
        event = FRAME_BEGIN;
      }
    }
    break;
    case FRAME_STARTED: {
      if ( b == FRAME_ESCAPE_BYTE ) {
        _state = FRAME_ESCAPING;
      }
      else if ( b == FRAME_END_BYTE ) {
        _state = FRAME_READY;
        event = FRAME_END;
      }
      else {
        event = FRAME_DATA;
        data = b;
      }
    }
    break;
    case FRAME_ESCAPING: {
      _state = FRAME_STARTED;
      event = FRAME_DATA;
      data = b ^ FRAME_ESCAPE_MASK;
    }
    break;
  }
  return FrameEvent(event, data);
}


Protocol::Protocol(Stream& stream)
  : _frame(stream), _state(PROTOCOL_READY), _cmd_handler(NULL) {}


void Protocol::receive() {
  FrameEvent event = _frame.receive();
  switch(_state) {
    case PROTOCOL_READY: {
      if ( event.event == FRAME_BEGIN ) {
        _state = PROTOCOL_READ_CMD;
      }
    }
    break;
    case PROTOCOL_READ_CMD: {
      if ( event.event == FRAME_DATA ) {
        _state = PROTOCOL_READ_ARG;
        _cmd = (protocol_cmd)event.data;
        _arg = 0;
      }
    }
    break;
    case PROTOCOL_READ_ARG: {
      // read arg in big endian order
      if ( event.event == FRAME_DATA ) {
        _arg = (_arg << 8) | (0xFF & event.data);
      }
    }
    break;
  }
  if ( event.event == FRAME_END ) {
    if ( _state == PROTOCOL_READ_ARG ) {
      received(_cmd, _arg);
    }
    _state = PROTOCOL_READY;
  }
}


void Protocol::log(const String& msg) {
  _frame.begin();
  _frame.write(PROTOCOL_CMD_LOG);
  write(msg);
  _frame.end();
}

void Protocol::status(const String& key, unsigned int value) {
  _frame.begin();
  _frame.write(PROTOCOL_CMD_STATUS);
  write(key);
  write(value);
  _frame.end();
}

void Protocol::write(const String& msg) {
  // only send up to 255 chars
  byte len = msg.length();
  _frame.write(len);
  for ( int i = 0; i < len; i++ ) {
    _frame.write(msg[i]);
  }
}

void Protocol::write(unsigned int value) {
  _frame.write((value >> 8) & 0xFF);
  _frame.write((value) & 0xFF);
}

void Protocol::received(protocol_cmd cmd, unsigned int arg) {
  if ( _cmd_handler ) {
    _cmd_handler(cmd, arg);
  }
}
