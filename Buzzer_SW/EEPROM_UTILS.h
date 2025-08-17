/*
  Dr. Tõnis
  Pfäffikon 2025
  Switzerland  

  Buzzer

*/

// in the eeprom we write the data with the following structure
// eepromValue = abc where (max value is 255)
// a - no function
// b - eepromVolume - volume level (between 0 and 9)
// c - eepromTrack - track number (between 0 and 9)

// get the volume level and track number from eeprom
void EepromGetVolumeTrack() {
  int eepromValue = 0; // local help parameter - value stored in the current Eemprom address
  // read the Eeprom value
  eepromValue = EEPROM.read(eepromAddress);
  // write info to serial
  if (debugModeE) Serial.print("eepromValue = "); Serial.println(eepromValue);
  // get the volume level from eepromValue
  eepromVolume = eepromValue / 10; // after dividing with 10 we have ab "abc/10=ab"
  eepromVolume = eepromVolume % 10; // get the part b
  // write info to serial
  if (debugModeE) Serial.print("Volume value is "); Serial.println(eepromVolume);
  // get the track number from eepromValue
  eepromTrack = eepromValue % 10; // we need the part c
  // write info to serial
  if (debugModeE)  Serial.print("Track number is "); Serial.println(eepromTrack);
}

void EepromUpdateVolumeTrack() {
  // prepare the new eeprom data package
  int value = 10* eepromVolume + eepromTrack; // value = abc a = 100*0 
  // write info to serial
  if (debugModeE) Serial.print("EepromUpdateVolumeTrack = "); Serial.println(value);
  // update the eeprom
  EEPROM.update(eepromAddress, value);
}