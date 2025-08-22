/*
  Dr. Tõnis
  Pfäffikon 2025
  Switzerland  

  Buzzer

*/

void init_pins() {
  // define output pins
    pinMode(OutPutPins, OUTPUT);
    pinMode(LedPin, OUTPUT);
  // define input pins
    for (int i = 0; i < 5; i++) {
      // define all panel control pins at the same time
      pinMode(InPutButtons[i], INPUT);
    }
}

void setup_init() {
  wdt_disable();
  // start the serial
    if (debugModeE || debugModeF || debugModeM || debugModeD) Serial.begin(115200);
  // define the input/output pins
    init_pins();
  // define the screen
    init_screen();
  // define the miniplayer
    init_player();
  // Enable watchdog with 2s timeout
    wdt_enable(WDTO_2S); // Timeout values: WDTO_15MS, WDTO_30MS, WDTO_1S, WDTO_2S, WDTO_8S … up to 8 seconds max.
}