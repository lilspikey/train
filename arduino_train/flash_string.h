#ifndef __FLASH_STRING_H__
#define __FLASH_STRING_H__

#include <Arduino.h>

// small helper class/util to convert from F() objects to String()
// object (this will be in Arduino IDE 1.5) so won't be needed then

#define FS(string_literal) FlashString(F(string_literal))

class FlashString {
  public:
    FlashString(const __FlashStringHelper* pHelper) : _pHelper(pHelper) {}
    
    operator String() const {
      int len = strlen_P((PGM_P)_pHelper);
      char buffer[len + 1];
      strcpy_P(buffer, (PGM_P)_pHelper);
      buffer[len] = '\0';
      return String(buffer);
    }
  
  private:
    const __FlashStringHelper* _pHelper;
};

#endif
