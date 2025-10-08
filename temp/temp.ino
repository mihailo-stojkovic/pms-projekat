#include <Arduino.h>
#include <TM1637Display.h>
#include <TimerOne.h>

#define CLK 9
#define DIO 8
#define TOUCH_PIN 2
#define AX_PIN A0
#define AY_PIN A1
#define AZ_PIN A2
#define TEST_PIN 13

volatile bool sendTick = false;  // Timer1 flag
volatile bool touched = false;
volatile int steps = 0;          // step count updated from PC

TM1637Display display(CLK, DIO);
String serialBuffer = "";         // accumulate incoming serial data

// --- Interrupts ---
void touchISR() { touched = true; }
void timerISR() { sendTick = true; }

void setup() {
  Serial.begin(9600);
  
  display.setBrightness(0x0f);
  display.showNumberDec(0);

  attachInterrupt(digitalPinToInterrupt(TOUCH_PIN), touchISR, RISING);
  pinMode(AX_PIN, INPUT);
  pinMode(AY_PIN, INPUT);
  pinMode(AZ_PIN, INPUT);
  pinMode(TEST_PIN, OUTPUT);

  // Start Timer1 for 100ms interval
  Timer1.initialize(100000);  // 100 ms
  Timer1.attachInterrupt(timerISR);
  Timer1.start();
  digitalWrite(TEST_PIN, HIGH);
}

// --- Main loop ---
void loop() {
  // Update display with current steps
  display.showNumberDec(steps);

  // --- Send data every 100ms ---
  if (sendTick) {
    sendTick = false;

    int aX = analogRead(AX_PIN);
    int aY = analogRead(AY_PIN);
    int aZ = analogRead(AZ_PIN);

    Serial.print(aX);
    Serial.print(" ");
    Serial.print(aY);
    Serial.print(" ");
    Serial.print(aZ);
    Serial.print(" ");
    Serial.println((int)touched);

    touched = false;
  }

  // --- Handle incoming serial data ---
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      // End of command — parse step count
      int newSteps = serialBuffer.toInt();
      steps = newSteps;
      serialBuffer = ""; // reset buffer
    } else {
      serialBuffer += c; // accumulate digits
    }
  }
}
