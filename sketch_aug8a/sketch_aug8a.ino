// Kết nối chân LED (ví dụ chân 13)
const int ledPin = 13;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();
    if (data == '1') {
      digitalWrite(ledPin, HIGH); // Bật đèn
    } else if (data == '0') {
      digitalWrite(ledPin, LOW);  // Tắt đèn
    }
  }
}