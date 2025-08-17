/*
  Dr. Tõnis
  Pfäffikon 2025
  Switzerland  

  Buzzer
  Arduino Nano
*/

// add the required libraries
  #include "Wire.h"
  #include "Adafruit_GFX.h"
  #include "Adafruit_SSD1306.h"
  #include "Arduino.h"
  #include "DFRobotDFPlayerMini.h"
  #include <SoftwareSerial.h>
  #include <EEPROM.h>
  #include "Fonts/FreeSans9pt7b.h"
  #include "Fonts/FreeSansBold18pt7b.h"
// debugging mode
  bool debugModeE = false; // parameter to activate the serial communication
  bool debugModeF = false; // parameter to activate the serial communication
  bool debugModeM = false; // parameter to activate the serial communication
  bool debugModeD = false; // parameter to activate the serial communication
// screen parameters
  #define SCREEN_WIDTH 128 // OLED display width, in pixels
  #define SCREEN_HEIGHT 64 // OLED display height, in pixels
  #define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
  #define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
  Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
  bool ScreenOK = true;
// // define MiniPlayer serial pins
  SoftwareSerial softSerial(/*rx =*/10, /*tx =*/11);
  #define FPSerial softSerial
  DFRobotDFPlayerMini myDFPlayer;

// define input/output pins
  //                    index  0  1  2   3   4
  //                    button 1  2  3   4   5
  const int InPutButtons[5] = {2, 3, A3, A2, A1};
  const int volumePin[2] = {A7, A6}; // A6 and A7 are analog read only! 
  const int buzzerPin = 5;
  const int OutPutPins = 9;

// parameters
  const int maxEepromAdress = 100;
  int eepromVolume = 3; // volume level
  int eepromTrack = 1; // track number
  const int eepromAddress = 0; // current eeprom address
  char buf[4];  // enough for 0–999 - help parameter for displaying the track number 
  bool somethingNew = true; // a help parameter to deterrmine if we have something new to display
  bool volumeAdjusted = true; // a help parameter to determine if we have changed the volume level
  bool buzzerPressed = false;
  unsigned long previousMillisVolume = 0; // will store the last time the Volume button was pressed
  unsigned long previousMillisBuzzer = 0; // will store the last time the Buzzer button was pressed
  const int intervalVolumeChange = 2000; // interval at which to adjust the volume level in Eeporm
  const int intervalBuzzer = 5000; // interval at which the buzzer can be used

// include other functions
  #include "EEPROM_UTILS.h"
  #include "Display.h"
  #include "MiniPlayer.h"
  #include "Functions.h"
  #include "Initialization.h"

void setup() {
  // initiate everything
  setup_init();
  // get the volume and track number from eeprom
  EepromGetVolumeTrack();
}

void loop() {
  screenDrawEverything();
  TrackChangeButtons();
  BuzzerButtons();
  VolumeChangeButtons();
  CheckIfVolumeChanged();
  //playerSerialDetails(); // somehow crashes the I2C communication
  delay(100);
}