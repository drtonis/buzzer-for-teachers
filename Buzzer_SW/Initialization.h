/*
  Dr. Tõnis
  Pfäffikon 2025
  Switzerland  

  Buzzer

*/

void init_pins() {
  // define output pins
    pinMode(OutPutPins, OUTPUT);
  // define input pins
    for (int i = 0; i < 5; i++) {
      // define all panel control pins at the same time
      pinMode(InPutButtons[i], INPUT);
    }
}

void setup_init() {
  // start the serial
    if (debugModeE || debugModeF || debugModeM || debugModeD) Serial.begin(115200);
  // define the input/output pins
    init_pins();
  // define the screen
    init_screen();
  // define the miniplayer
    init_player();
}