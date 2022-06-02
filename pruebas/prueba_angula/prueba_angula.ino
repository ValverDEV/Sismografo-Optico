// Establecemos los pines de los sensores
const byte pin1 = 7;
const byte pin2 = 6;
const byte pin3 = 5;
const byte pin4 = 4;
const byte pin5 = 3;
const byte pin6 = 2;

// Arreglos que guardan el estado actual y el estado previo
int reads[] = {HIGH,HIGH,HIGH,HIGH,HIGH,HIGH};
int prevs[] = {HIGH,HIGH,HIGH,HIGH,HIGH,HIGH};

// Arreglos para guardar los tiemos para ida o regreso en cada sensor
unsigned long tPinsGo[] = {0,0,0,0,0,0};
unsigned long tPinsBack[] = {0,0,0,0,0,0};

// Sensor activo actual y previo para identificar orden
int active = 0;
int pre_active = -1;

// Variables para calculo de semiperiodo
unsigned long t0;
unsigned long tf;
unsigned long prevT0 = 0;

// Declaramos algunas funciones
void in_out(int pin);
void send_serial();
void reset_array(unsigned long arr[]);

void setup() {
  Serial.begin(9600); // Establecemos el baudrate del puerto serial
}

void loop() {
  // Lectura de estado de los sensores
  reads[0] = digitalRead(pin1);
  reads[1] = digitalRead(pin2);
  reads[2] = digitalRead(pin3);
  reads[3] = digitalRead(pin4);
  reads[4] = digitalRead(pin5);
  reads[5] = digitalRead(pin6);

  // Evaluemos el estado de cada sensor
  for (int pin = 0; pin < 6; pin++){
    in_out(pin);
  }
}



void in_out(int pin){
  if (reads[pin] != prevs[pin]){ // Si el estado es diferente al previo (hubo cambio)
    if(prevs[pin] == HIGH){ // Estaba en bajo, pasó a alto
      active = pin; // Establecemos el activo actual
      if (pre_active != active){ // Si es diferente al activo previo
        if(pre_active < active){ // ida
          if (pin == 0){ // Si es el estado base, comienza a tomar al tiempo
            t0 = millis();
          }
          tPinsGo[pin] = millis(); // Registra el tiempo en el que pasa por el sensor
        } else { // regreso
          tPinsBack[pin] = millis(); // Registra el tiempo en el que pasa por el sensor (regreso
          if (pin == 0){ // Si vuelve a ser el 0
            tf = millis(); // Cuenta el tiempo del movimiento
            if (t0 != prevT0 | t0 - prevT0 > 5000){ // Condición para evitar bug
              send_serial(); // manda los datos al serial
              prevT0 = t0;
            }
            // Limpia los tiempos
            reset_array(tPinsGo);
            reset_array(tPinsBack);
          }
        }
      } else { // mismo
          if (pin !=0){
            tPinsBack[pin] = millis(); // Registra el regreso de uno repetido (caso único)
          }
      }
    }
    if (active == 0){ //actualiza los previos a activos actuales
      pre_active = -1; // si el previo fue 0, necesitamos que sea negativo
    } else {
      pre_active = active;
    }
    prevs[pin] = !prevs[pin]; // actualiza el estado previo de cada pin
  }
}

void send_serial(){ // manda la info en el formato t0/tf/ix/rx
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

void reset_array(unsigned long arr[]){ // limpia un arreglo
  for (int i = 0; i<6; i++){
    arr[i] = 0;
  }
}
