/*
  Dr. Tõnis
  Pfäffikon 2025
  Switzerland  

  Buzzer

*/

void fillrect() {
  // depending on the ledState blink on the screen differently 
    if (ledState) display.fillRect(120, 50, 10, 10, WHITE); // (x_pos, y_pos, width, height, color)
    else          display.fillRect(120, 50, 10, 10, SSD1306_INVERSE);
  // show everything on the screen
    display.display();
}

void drawVolumeBars(int level, int x, int y) {
  for (int i = 0; i < 5; i++) {
    int height = 4 + 3 * i; // progressively taller bars
    int xpos = x + i * 10;
    if (i < level) {
      display.fillRect(xpos, y - height, 8, height, WHITE);
    } else {
      display.drawRect(xpos, y - height, 8, height, WHITE);
    }
  }
}

// Draw label text with Sans font
void drawLabel(const char* text, int FontSizeIndex, int16_t x, int16_t y) {
  // set the font
  switch (FontSizeIndex) {
    case 0: display.setFont(&FreeSans9pt7b); break;
    case 1: display.setFont(&FreeSansBold18pt7b); break;
    default: display.setFont(); break; // fallback to default font
  }
  // set the text location
  display.setCursor(x, y);
  // write it to the screen
  display.print(text);
}

void screenDrawStandard() {
  // Clear the buffer
  display.clearDisplay();
  // Draw "Volume" label
  drawLabel("Volume", 0, 5, 20);
  drawVolumeBars(eepromVolume, 80, 20);
  // Draw Track Number
  drawLabel("Track #", 0, 5, 55);
  // convert int to char
  itoa(eepromTrack, buf, 10);
  drawLabel(buf, 1, 80, 55); //drawLabel("3", 1, 80, 55);
  // update the display
  display.display();
  // adjust the help parameter
  somethingNew = false; 
}

void screenDrawEverything() {
  if (ScreenOK && somethingNew) {
    // update the screen only if something is new
    screenDrawStandard();
  }

}

void init_screen() {
  Wire.begin();
  // define the screen
    if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) { // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
      if (debugModeE || debugModeF || debugModeM || debugModeD) Serial.println(F("SSD1306 allocation failed"));
      ScreenOK = false;
    }
  // rotate the display 180 deg
    display.setRotation(2);
  // Clear the buffer
    display.clearDisplay();
  // set the text color
    display.setTextColor(WHITE);
  // write booting for the next
    drawLabel("Starting", 0, 5, 20);
  // show everything on the screen
    display.display();
}
