#include <Arduino.h>
#include <FastLED.h>
#include <BLE_Uart.h>

const int packSize = 4;
char laptop_packetBuffer[packSize] = {'0', '0', '0', '0'};
BLE_Uart CubbyLED = BLE_Uart(laptop_packetBuffer, packSize);

// Off / Highlight / Object just detected and trying to figure out what the hell it is
CRGB ModeToColor[] = {CRGB::Black, CRGB::White, CRGB::Purple};

#define NUM_LEDS 7 // LEDs per strip

CRGB cub1[NUM_LEDS];
CRGB cub2[NUM_LEDS];
CRGB cub3[NUM_LEDS];
CRGB cub4[NUM_LEDS];

const int cub1_pin = 1;
const int cub2_pin = 2;
const int cub3_pin = 3;
const int cub4_pin = 4;

void setLeds(CRGB color) {
  fill_solid(cub1, NUM_LEDS, color);
  fill_solid(cub2, NUM_LEDS, color);
  fill_solid(cub3, NUM_LEDS, color);
  fill_solid(cub4, NUM_LEDS, color);
  FastLED.show();
}

void setup() {
  USBSerial.begin(115200);

  CubbyLED.init_ble("Cubby_Sense");

  FastLED.addLeds<WS2812B, cub1_pin, GRB>(cub1, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.addLeds<WS2812B, cub2_pin, GRB>(cub2, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.addLeds<WS2812B, cub3_pin, GRB>(cub3, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.addLeds<WS2812B, cub4_pin, GRB>(cub4, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.setBrightness( 100 );
  FastLED.show();

  setLeds(CRGB::Green);
  delay(500);
  setLeds(CRGB::Black);
}

void loop() {

  if (CubbyLED.isConnected()) {
    fill_solid(cub1, NUM_LEDS, ModeToColor[(int)laptop_packetBuffer[1] - '0']);
    fill_solid(cub2, NUM_LEDS, ModeToColor[(int)laptop_packetBuffer[0] - '0']);
    fill_solid(cub3, NUM_LEDS, ModeToColor[(int)laptop_packetBuffer[3] - '0']);
    fill_solid(cub4, NUM_LEDS, ModeToColor[(int)laptop_packetBuffer[2] - '0']);

  } else { // Handle not connected case
    setLeds(CRGB::Black);

    static bool tog = false;
    EVERY_N_MILLIS(750)
      tog = !tog;
    
    if (tog)
      cub1[6] = CRGB::Blue;
    else 
      cub1[6] = CRGB::Black;
  }

  FastLED.show();
  delay(10);
}
