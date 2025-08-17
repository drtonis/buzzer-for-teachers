/*
  Dr. Tõnis
  Pfäffikon 2025
  Switzerland  

  Buzzer

*/

void printDetail(uint8_t type, int value){
  switch (type) {
    case TimeOut:
      Serial.println("Time Out!");
      break;
    // case WrongStack:
    //   Serial.println("Stack Wrong!");
    //   break;
    case DFPlayerCardInserted:
      Serial.println("Card Inserted!");
      break;
    case DFPlayerCardRemoved:
      Serial.println("Card Removed!");
      break;
    case DFPlayerCardOnline:
      Serial.println("Card Online!");
      break;
    // case DFPlayerUSBInserted:
    //   Serial.println("USB Inserted!");
    //   break;
    // case DFPlayerUSBRemoved:
    //   Serial.println("USB Removed!");
    //   break;
    // case DFPlayerPlayFinished:
    //   Serial.print("Number:");
    //   Serial.print(value);
    //   Serial.println(" Play Finished!");
    //   break;
    case DFPlayerError:
      Serial.print("DFPlayerError:");
      switch (value) {
        case Busy:
          Serial.println("Card not found");
          break;
        // case Sleeping:
        //   Serial.println("Sleeping");
        //   break;
        // case SerialWrongStack:
        //   Serial.println("Get Wrong Stack");
        //   break;
        // case CheckSumNotMatch:
        //   Serial.println("Check Sum Not Match");
        //   break;
        // case FileIndexOut:
        //   Serial.println("File Index Out of Bound");
        //   break;
        case FileMismatch:
          Serial.println("Cannot Find File");
          break;
        // case Advertise:
        //   Serial.println("In Advertise");
        //   break;
        default:
          break;
      }
      break;
    default:
      break;
  } 
}

void playerSerialDetails() {
  if (myDFPlayer.available()) {
    printDetail(myDFPlayer.readType(), myDFPlayer.read()); //Print the detail message from DFPlayer to handle different errors and states.
  }
}

void playerSetVolume() {
  // set the new volume level. eepromVolume can be between 1 and 5
  int value = 6 * eepromVolume;
  // write info to serial
  if (debugModeM) {
    Serial.print("eepromVolume = "); Serial.println(eepromVolume);
    Serial.print("Volume = "); Serial.println(value);
  }
  myDFPlayer.volume(value); // Set volume value (0~30).
  // write info to serial
  if (debugModeM) Serial.println("Volume adjusted");
}

void CheckIfVolumeChanged() {
  if (volumeAdjusted) { // we do something only if the volume has been adjusted
    if (millis() - previousMillisVolume >= intervalVolumeChange) {
      // only after intervalVolumeChange we make the Eeprom update
      EepromUpdateVolumeTrack();
      volumeAdjusted = false;
    }
  }
}

void playerAdjustVolume(int addVolume) {
  switch (addVolume) {
    case 0: eepromVolume += 1; break; // increase volume
    case 1: eepromVolume -= 1; break; // reduce volume
    default: break; // do nothing
  }

  // eepromVolume can be between 1 and 5
  if (eepromVolume > 5) eepromVolume = 1;
  if (eepromVolume < 1) eepromVolume = 5;
}

void init_player() {
  // turn the Miniplayer power ON
    digitalWrite(OutPutPins, HIGH);
  // some delay
    delay(1000);
  // start the software serial
    FPSerial.begin(9600);
  // start the player  
    // write info to serial
    if (debugModeM) Serial.println(F("Initializing DFPlayer ... (May take 3~5 seconds)"));
  
    if (!myDFPlayer.begin(FPSerial, /*isACK = */true, /*doReset = */true)) {  //Use serial to communicate with mp3.
      // if the first try doesn't work, then try again and start the software serial
      FPSerial.begin(9600);
      if (!myDFPlayer.begin(FPSerial, /*isACK = */true, /*doReset = */true)) {  //Use serial to communicate with mp3.
        // write info to serial
        if (debugModeM) Serial.println(F("Unable to begin:"));
        if (ScreenOK) {
          drawLabel("SD card!",  0, 5, 20);
          display.display();
        }
        while(true){
          delay(100); // Code to compatible with ESP8266 watch dog.
        }
      }
    }
    // write info to serial
    if (debugModeM) Serial.println(F("DFPlayer Mini online."));
  // define volume
    myDFPlayer.volume(10);  //Set volume value. From 0 to 30
}