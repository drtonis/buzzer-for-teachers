/*
  Dr. Tõnis
  Pfäffikon 2025
  Switzerland  

  Buzzer

*/

void TrackChangeButtons() {
  // go through all the buttons and check if one of them has been pressed
  for (int button_index = 0; button_index < 5; button_index++) {
    // HIGH means pressed button 
    if (digitalRead(InPutButtons[button_index])) {
      // stop the current sound
      myDFPlayer.stop(); 
      if (debugModeF) Serial.print("you have pressed Button "); Serial.println(button_index);
      // if the new track number differs from the current one then we change it
      if (eepromTrack != button_index + 1) {
        // adjust the track number
        eepromTrack = button_index + 1;
        if (debugModeF) Serial.print("Track number is "); Serial.println(eepromTrack);
        // adjust Eeprom
        EepromUpdateVolumeTrack();
        // adjust the screen
        somethingNew = true;
        // in order to prevent delays after changing the track 
        previousMillisBuzzer = 0; // the last time instance the buzzer was pressed
        // adjust the Eeprom
        volumeAdjusted = true;
        // adjust time for the eeprom saving
        previousMillisVolume = millis();
      }
    }
  }
}

void BuzzerButtons() {
  if (digitalRead(buzzerPin) && !buzzerPressed && millis() - previousMillisBuzzer > intervalBuzzer) {
    if (debugModeF) Serial.println("Buzzer Button");
    myDFPlayer.play(eepromTrack);  // Play the corresponding mp3
    //myDFPlayer.playMp3Folder(eepromTrack);  // play specific mp3 in SD:/MP3/0004.mp3; File Name(0~65535)
    //myDFPlayer.playFolder(1, eepromTrack);  // play specific mp3 in SD:/15/004.mp3; Folder Name(1~99); File Name(1~255)
    //myDFPlayer.advertise(eepromTrack); // advertise specific mp3 in SD:/ADVERT/0003.mp3; File Name(0~65535)
    // small delay
    delay(1);
    // adjust the help paramters accordingly
    buzzerPressed = true;
    previousMillisBuzzer = millis(); // the last time instance the buzzer was pressed
  }
  else buzzerPressed = false;
}

void VolumeChangeButtons() {
  if (volumeAdjusted && millis() - previousMillisVolume < 150) {
    return; // skip if not enough time has passed
  }
  // here we chack what the volume change buttons are doing
  bool LocalVolumeAdjusted = false; // local help parameter
  // volume + button
  if (analogRead(volumePin[0]) > 500) {
    if (debugModeF) Serial.println("Volume + Button");
    // adjust the volume level
    playerAdjustVolume(0);
    // local help parameter 
    LocalVolumeAdjusted = true;
  }
  // volume - button
  if (analogRead(volumePin[1]) > 500) {
    if (debugModeF) Serial.println("Volume - Button");
    // adjust the volume level
    playerAdjustVolume(1);
    // local help parameter 
    LocalVolumeAdjusted = true;
  }
  // aditional parameters that change only if the button is pressed
  if (LocalVolumeAdjusted) {
    // stop the current sound
    myDFPlayer.stop(); 
    // send it to the MiniPlayer
    playerSetVolume();
    // adjust the screen
    somethingNew = true;
    // adjust the Eeprom
    volumeAdjusted = true;
    // adjust time for the eeprom saving
    previousMillisVolume = millis();
  }
}