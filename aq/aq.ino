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


volatile int aX, aY, aZ;
volatile bool touched = false;
volatile int steps = 0;
volatile byte comCode = 0x01;
volatile int calibrationCounter = 0;
volatile bool newCommand = false;
volatile bool calibrationDone = false;
volatile bool sendCalibrationFlag = false;
void touchISR() {
  touched = true;
}

TM1637Display display(CLK, DIO);

void setup() {
  Serial.begin(9600);
  display.setBrightness(0x0f);  // Set brightness to maximum
  display.showNumberDec(steps);  // Display the number 1234
  attachInterrupt(digitalPinToInterrupt(TOUCH_PIN), touchISR, RISING);
  pinMode(AX_PIN, INPUT);
  pinMode(AY_PIN, INPUT);
  pinMode(AZ_PIN, INPUT);
  pinMode(TEST_PIN, OUTPUT);


}

void loop() {
  display.showNumberDec(steps);
  aX = analogRead(AX_PIN);
  aY = analogRead(AY_PIN);
  aZ = analogRead(AZ_PIN);

  if (newCommand) {
    newCommand = false;
    switch (comCode) {
      case 0x01: // ComCode za standardna merenja
        // pokreni mjerenje
        return;
      case 0x02: // ComCode za pocetak kalibracije
        Timer1.initialize(100000);
        Timer1.attachInterrupt(sendCalibrationData);
        Timer1.start();
        digitalWrite(TEST_PIN, HIGH);
        return;
      case 0x03: //ComCode za primanje broja koraka
        steps = Serial.parseInt();
        comCode = 0x01; // vrati se na standardna merenja
        return;
    }
  }
  if (calibrationDone) {
    Timer1.stop();
    calibrationDone = false;
    return;
  }

  if (comCode == 0x01) {
    sendData();
  }

  if(sendCalibrationFlag) {
    Serial.print(0x03); // ComCode za kalibracione podatke 
    Serial.print(" ");
    Serial.print(aX);
    Serial.print(" ");
    Serial.print(aY);
    Serial.print(" ");
    Serial.println(aZ);
    calibrationCounter++;
    if (calibrationCounter >= 100) {
      calibrationCounter = 0;
      comCode = 0x01;
      calibrationDone = true;
    }

  }

}


void sendCalibrationData() {
  sendCalibrationFlag = true;
}

void sendData() {
  Serial.print(0x01); // ComCode za kalibracione podatke 
  Serial.print(" ");
  Serial.print(aX);
  Serial.print(" ");
  Serial.print(aY);
  Serial.print(" ");
  Serial.print(aZ);
  Serial.print(" ");
  Serial.println((int)touched);
  touched = false;
}


void serialEvent() {
  if (Serial.available()) {
    comCode = Serial.read();  // cita se samo jedan bajt - Predstavlja ComCode pd racunara ka arudinu
    newCommand = true;        // sta treba dalje da se radi se izvrsava u loop
  }
}