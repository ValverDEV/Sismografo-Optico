const byte pin1 = 7;
const byte pin2 = 6;
const byte pin3 = 5;
const byte pin4 = 4;
const byte pin5 = 3;
const byte pin6 = 2;

int reads[] = {HIGH,HIGH,HIGH,HIGH,HIGH,HIGH};
int prevs[] = {HIGH,HIGH,HIGH,HIGH,HIGH,HIGH};

//int tPinsIn[] = {0,0,0,0,0,0};
//int tPinsOut[] = {0,0,0,0,0,0};

unsigned long tPinsGo[] = {0,0,0,0,0,0};
unsigned long tPinsBack[] = {0,0,0,0,0,0};

int active = 0;
int pre_active = -1;

unsigned long t0;
unsigned long tf;
unsigned long prevT0 = 0;

//int left = false;

void in_out(int pin);
void send_serial();
void reset_array(unsigned long arr[]);

void setup() {
  Serial.begin(9600);
}

void loop() {
  reads[0] = digitalRead(pin1);
  reads[1] = digitalRead(pin2);
  reads[2] = digitalRead(pin3);
  reads[3] = digitalRead(pin4);
  reads[4] = digitalRead(pin5);
  reads[5] = digitalRead(pin6);

  for (int pin = 0; pin < 6; pin++){
    in_out(pin);
  }
}



void in_out(int pin){
  if (reads[pin] != prevs[pin]){
    if(prevs[pin] == HIGH){
      active = pin;
      if (pre_active != active){
        if(pre_active < active){ // ida
          if (pin == 0){
            t0 = millis();
          }
          tPinsGo[pin] = millis();
        } else { // regreso
          tPinsBack[pin] = millis();
          if (pin == 0){
            tf = millis();
            if (t0 != prevT0 | t0 - prevT0 > 5000){
              send_serial();
              prevT0 = t0;
            }
            reset_array(tPinsGo);
            reset_array(tPinsBack);
          }
        }
      } else { // mismo
//        Serial.print(pin);
//        Serial.println("Mismo");
          if (pin == 0) {
//            t0 = millis();
//            tPinsGo[pin] = t0;
          }
          if (pin !=0){
            tPinsBack[pin] = millis();
          }
      }
    }
    if (active == 0){
      pre_active = -1;
    } else {
      pre_active = active;
    }
    prevs[pin] = !prevs[pin];
  }
}

void send_serial(){
  Serial.print(t0);
  Serial.print("/");
  Serial.print(tf);
  Serial.print("/");
  for (int pin = 0; pin < 6; pin++){
    Serial.print(tPinsGo[pin]);
    Serial.print(",");
  }
  Serial.print("/");
  for (int pin = 0; pin < 6; pin++){
    Serial.print(tPinsBack[pin]);
    Serial.print(",");
  }
  Serial.println();
}

void reset_array(unsigned long arr[]){
  for (int i = 0; i<6; i++){
    arr[i] = 0;
  }
}
