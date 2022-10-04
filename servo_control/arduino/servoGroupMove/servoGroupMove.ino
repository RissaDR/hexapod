void setup() {
  Serial.begin(115200);
  clearError();
  disableACK();
  torqueOn();
}

void loop() {
  moveServo(0x04, 0, 0x01);
  moveServo(0x07, 0, 0x01);
  moveServo(0x01, 0, 0x01);
  delay(1000);
  moveServo(0x04, 1023, 0x02);
  moveServo(0x07, 1023, 0x02);
  moveServo(0x01, 1023, 0x02);
  delay(1000);
}

void torqueOn() {
  uint8_t data[10];
  data[0] = 0xFF; // header 1
  data[1] = 0xFF; // header 2
  data[2] = 10; // length
  data[3] = 0xFE; // servo id
  data[4] = 0x03; // CMD id

  data[7] = 0x34; // register
  data[8] = 0x01; // length
  data[9] = 0x60; // value 

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9]) & 0xFE; // checksum1
  data[6] = (~data[5]) & 0xFE; // checksum2

  for (int i = 0; i < 10; i++) {
    Serial.write(data[i]);
  }
  
}

void moveServo(uint8_t servoId, uint16_t pos, uint8_t color) {
  
  uint8_t lo_pos;
  uint8_t hi_pos;
  lo_pos = (uint8_t) pos;
  hi_pos = (uint8_t) (pos >> 8);
  
  uint8_t data[12];
  data[0] = 0xFF; // header 1
  data[1] = 0xFF; // header 2
  data[2] = 12; // length
  data[3] = servoId; // servo id
  data[4] = 0x06; // CMD id

  data[7] = 60; // playtime
  data[8] = lo_pos; // jog lsb
  data[9] = hi_pos; // jog msb
  color = color & 0x03;
  data[10] = (color << 2) & (~0x02); // set
  data[11] = servoId; // id

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9] ^ data[10] ^ data[11]) & 0xFE; // checksum1
  data[6] = (~data[5]) & 0xFE; // checksum2

  for (int i = 0; i < 12; i++) {
    Serial.write(data[i]);
  }

}

void disableACK() {
  uint8_t data[10];
  data[0] = 0xFF; // header 1
  data[1] = 0xFF; // header 2
  data[2] = sizeof(data)/sizeof(data[0]); // length
  data[3] = 0xFE; // servo id
  data[4] = 0x03; // CMD id

  data[7] = 1; // register
  data[8] = 0x01; // length
  data[9] = 1; // value 

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9]) & 0xFE;
  data[6] = (~data[5]) & 0xFE;

//  Serial.println("Hello world");
//  return;
  for (int i = 0; i < 10; i++) {
    Serial.write(data[i]);
  }
  
}

void clearError() {
  uint8_t data[11];
  data[0] = 0xFF; // header 1
  data[1] = 0xFF; // header 2
  data[2] = 11; // length
  data[3] = 0xFE; // servo id
  data[4] = 0x03; // CMD id

  data[7] = 0x30; // register
  data[8] = 0x02; // length
  data[9] = 0x00; // value 
  data[10] = 0x00; // value 

  data[5] = (data[2] ^ data[3] ^ data[4] ^ data[7] ^ data[8] ^ data[9] ^ data[10]) & 0xFE;
  data[6] = (~data[5]) & 0xFE;

//  Serial.println("Hello world");
//  return;
  for (int i = 0; i < 11; i++) {
    Serial.write(data[i]);
  }
  
  delay(10);
}
