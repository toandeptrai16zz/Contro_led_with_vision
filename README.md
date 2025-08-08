# Hand Gesture Controlled LED Simulation with Python and Arduino in Proteus

## Description
This project uses Python (OpenCV + MediaPipe) to detect hand gestures (open or closed hand). When an open hand is detected, Python sends a signal via a virtual COM port to an Arduino (simulated in Proteus) to turn an LED on or off.

## Components
- Python 3
- Libraries: opencv-python, mediapipe, pyserial
- Proteus (simulating Arduino Uno, LED, COMPIM)
- Virtual Serial Port Driver (to create virtual COM port pairs)

## Instructions

### 1. Create a Virtual COM Port Pair
- Use Virtual Serial Port Driver to create a pair, e.g., COM1 ↔ COM2 (or any available names).

### 2. Configure Proteus
- Add Arduino Uno, LED, and COMPIM to your schematic.
- Wiring:
  - Connect the LED to pin 13 of Arduino (with a resistor and GND).
  - COMPIM: TXD (pin 3) to RX (pin 0 Arduino), RXD (pin 2) to TX (pin 1 Arduino), GND to GND.
- COMPIM settings:
  - Select the correct virtual COM port (e.g., COM1 or COM2, opposite to Python).
  - Baud rate: 9600.

### 3. Upload Arduino Code
- Use the sample code below, compile and upload the hex file to Arduino in Proteus:

```cpp
const int ledPin = 13;
void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}
void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();
    if (data == '1') digitalWrite(ledPin, HIGH);
    else if (data == '0') digitalWrite(ledPin, LOW);
  }
}
```

### 4. Install Python Libraries
```bash
pip install opencv-python mediapipe pyserial
```

### 5. Run the Python Program
- Set the `SERIAL_PORT` variable in `hand_control.py` to match your virtual COM port (e.g., 'COM2').
- Start Proteus first, then run the Python script:
```bash
python hand_control.py
```
- Press 'q' or ESC to stop the program.

## Result
- When your hand is open, the LED in Proteus will turn on.
- When your hand is closed, the LED will turn off.

## Notes
- Make sure the baud rate and COM port match between Python, Proteus, and Arduino.
- If the LED does not turn on, check the TX/RX/GND wiring and COM port configuration.
