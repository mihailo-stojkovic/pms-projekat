#include <TimerOne.h>

const int pin1 = 2;
const int pin2 = 3;
const int pin3 = 4;
const int edgePin = 5;

// 7-segment display pins (a-g)
const int segPins[7] = {6, 7, 8, 9, 10, 11, 12};

// Segment patterns for digits 0-9 (common cathode)
const byte digitPatterns[10] = {
    0b00111111, // 0
    0b00000110, // 1
    0b01011011, // 2
    0b01001111, // 3
    0b01100110, // 4
    0b01101101, // 5
    0b01111101, // 6
    0b00000111, // 7
    0b01111111, // 8
    0b01101111  // 9
};

volatile bool sendDataFlag = false;
volatile bool edgeFlag = false;
volatile int displayDigitValue = 0;

void timerISR() {
    sendDataFlag = true;
}

void edgeISR() {
    edgeFlag = true;
}

void setup() {
    Serial.begin(9600);

    pinMode(pin1, INPUT);
    pinMode(pin2, INPUT);
    pinMode(pin3, INPUT);
    pinMode(edgePin, INPUT);

    for (int i = 0; i < 7; i++) {
        pinMode(segPins[i], OUTPUT);
        digitalWrite(segPins[i], LOW);
    }

    Timer1.initialize(100000); // 100ms
    Timer1.attachInterrupt(timerISR);

    attachInterrupt(digitalPinToInterrupt(edgePin), edgeISR, RISING);
}

void displayDigit(int digit) {
    if (digit < 0 || digit > 9) return;
    byte pattern = digitPatterns[digit];
    for (int i = 0; i < 7; i++) {
        digitalWrite(segPins[i], (pattern >> i) & 0x01);
    }
}

void loop() {
    // Timer-based data send
    if (sendDataFlag) {
        sendDataFlag = false;

        int val1 = digitalRead(pin1);
        int val2 = digitalRead(pin2);
        int val3 = digitalRead(pin3);

        Serial.print("Pin1: ");
        Serial.print(val1);
        Serial.print(", Pin2: ");
        Serial.print(val2);
        Serial.print(", Pin3: ");
        Serial.println(val3);
    }

    // Rising edge detection (interrupt)
    if (edgeFlag) {
        edgeFlag = false;
        Serial.println("Rising edge detected!");
        // You can send another value here if needed
    }

    // Receive digit from Serial and display (handled in loop, but value stored for ISR-safe access)
    if (Serial.available()) {
        char ch = Serial.read();
        if (ch >= '0' && ch <= '9') {
            displayDigitValue = ch - '0';
        }
    }

    // Display digit (handled in loop for safe access to hardware)
    displayDigit(displayDigitValue);
}