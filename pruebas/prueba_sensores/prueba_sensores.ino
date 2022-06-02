const byte pin1 = 7;
const byte pin2 = 6;
const byte pin3 = 5;
const byte pin4 = 4;
const byte pin5 = 3;
const byte pin6 = 2;

int read1 = HIGH;
int read2 = HIGH;
int read3 = HIGH;
int read4 = HIGH;
int read5 = HIGH;
int read6 = HIGH;

void setup(){
  Serial.begin(9600);
}

void loop(){
  read1 = digitalRead(pin1);
  read2 = digitalRead(pin2);
  read3 = digitalRead(pin3);
  read4 = digitalRead(pin4);
  read5 = digitalRead(pin5);
  read6 = digitalRead(pin6);

  Serial.print("Pin 1: ");
  Serial.print(read1);
  Serial.print(" Pin 2: ");
  Serial.print(read2);
  Serial.print(" Pin 3: ");
  Serial.print(read3);
  Serial.print(" Pin 4: ");
  Serial.print(read4);
  Serial.print(" Pin 5: ");
  Serial.print(read5);
  Serial.print(" Pin 6: ");
  Serial.println(read6);
}
