#include <Adafruit_NeoPixel.h>
#include <elapsedMillis.h>
#define LEDPIN 2
#define AVG 10
#define SensorInterrupt 3
#define interval 1000  //time interval for interrupt to be sent in ms

elapsedMillis timer;


// defines pins numbers
const int RtrigPin = 9;
const int RechoPin = 10;
const int LtrigPin = 5;
const int LechoPin = 6;

//Values for LED calculation
int counter = 0;
int LdistanceAVG, RdistanceAVG;
int Ldistances[10], Rdistances[10];
int signalOffset = 11;


//Distance Variables for Sonars
long duration;
int Ldistance, Rdistance;

//LED Variables
// small led 73
// large led 116
int ledLenght = 75;
int timeLen = 100;
//LED colors for right sensor
int RightLEDR = 255, RightLEDG = 0, RightLEDB = 0;
//LED colors for left sensor
int LeftLEDR = 255, LeftLEDG = 0, LeftLEDB = 0;
int LStart = 0, LEnd = 5, REnd = 10;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(ledLenght, LEDPIN, NEO_GRB + NEO_KHZ800);


void setup() {
  pinMode(RtrigPin, OUTPUT); // Sets the RtrigPin as an Output
  pinMode(RechoPin, INPUT); // Sets the RechoPin as an Input
  pinMode(LtrigPin, OUTPUT); // Sets the RtrigPin as an Output
  pinMode(LechoPin, INPUT); // Sets the RechoPin as an Input

  Serial.begin(9600); // Starts the serial communication
  pinMode(SensorInterrupt, OUTPUT);

  strip.begin();
  strip.show(); // Initialize all pixels to 'off'

  timer = 0; //Initialize timer
}

void loop() {
  RightSensor();
  LeftSensor();

  getAvg();

  rightLEDs(strip.Color(RightLEDR, RightLEDG, RightLEDB), timeLen); //red (R, G, B)
  leftLEDs(strip.Color(LeftLEDR, LeftLEDG, LeftLEDB), timeLen);
  //delay(500);

  if (timer > interval) {
    if (LdistanceAVG < 12 && RdistanceAVG > 12) {
      digitalWrite(SensorInterrupt, HIGH);
      Serial.println("L");
      digitalWrite(SensorInterrupt, LOW);
    }
    else if (LdistanceAVG > 12 && RdistanceAVG < 12) {
      digitalWrite(SensorInterrupt, HIGH);
      Serial.println("R");
      digitalWrite(SensorInterrupt, LOW);
    }
    timer -= interval;
  }
}



void RightSensor() {
  // Clears the RtrigPin
  digitalWrite(RtrigPin, LOW);
  delayMicroseconds(2);
  // Sets the RtrigPin on HIGH state for 10 micro seconds
  digitalWrite(RtrigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(RtrigPin, LOW);
  // Reads the RechoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(RechoPin, HIGH);
  // Calculating the distance
  Rdistance = duration * 0.034 / 2;
  // Prints the distance on the Serial Monitor
}

void LeftSensor() {
  // Clears the LtrigPin
  digitalWrite(LtrigPin, LOW);
  delayMicroseconds(2);
  // Sets the LtrigPin on HIGH state for 10 micro seconds
  digitalWrite(LtrigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(LtrigPin, LOW);
  // Reads the LechoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(LechoPin, HIGH);
  // Calculating the distance
  Ldistance = duration * 0.034 / 2;
  // Prints the distance on the Serial Monitor
}


void getAvg()
{
  LdistanceAVG = 0;
  RdistanceAVG = 0;
  Ldistances[counter % 10] = Ldistance;
  Rdistances[counter % 10] = Rdistance;

  for (int i = 0; i < AVG; i++)
  {
    LdistanceAVG = Ldistances[i] + LdistanceAVG;
    RdistanceAVG = Rdistances[i] + RdistanceAVG;
  }

  LdistanceAVG /= AVG;
  RdistanceAVG /= AVG;
  counter++;
}

//LED settings for left side
void leftLEDs(uint32_t c, uint8_t wait) {
  //Left LEDS
  if (LdistanceAVG < 30)
  {
    if (LdistanceAVG > 12) {
      LeftLEDR = 0;
      LeftLEDB = 255;
    }
    else {
      LeftLEDR = 255;
      LeftLEDB = 0;
    }
    //Turns LEDs on if within 100cm
    for (int i = LStart; i < LEnd; i++)
    {
      strip.setPixelColor(i, c);
      strip.show();
    }

  }
  else
  {
    //Turns LEDs off
    for (int i = LStart; i < LEnd; i++)
    {
      strip.setPixelColor(i, 0);
      strip.show();
    }
  }
}

//LED settings for right side
void rightLEDs(uint32_t c, uint8_t wait) {
  //Right LEDS
  if (RdistanceAVG < 30)
  {
    if (RdistanceAVG > 12) {
      RightLEDR = 0;
      RightLEDB = 255;
    }
    else {
      RightLEDR = 255;
      RightLEDB = 0;
      //rightSignal();
    }

    //Turns LEDs on if within 100cm
    for (int i = LEnd; i < REnd; i++)
    {
      strip.setPixelColor(i, c);
      strip.show();
    }
  }

  else
  {
    //Turns LEDs off
    for (int i = LEnd; i < REnd; i++)
    {
      strip.setPixelColor(i, 0);
      strip.show();
    }
  }
}

/*void rightSignal() {
  for (int i = 0; i < 3; i++) {
    if (i == 0)
      strip.setPixelColor(13, strip.Color(0, 0, 0));
    else
      strip.setPixelColor(i + signalOffset - 1, strip.Color(0, 0, 0));
    strip.setPixelColor(i + signalOffset, strip.Color(138, 43, 226));
    strip.show();
    delay(100);
    if (i == 2) {
      strip.setPixelColor(i + signalOffset, strip.Color(0, 0, 0));
      strip.show();
    }
  }
  }*/

