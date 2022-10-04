void setup() {
  Serial.begin(115200);
}

void loop() {;
  if (Serial.available() > 0) {
    char ser = Serial.read();
    Serial.print("I heard: ");
    Serial.println(ser);
  }
}
