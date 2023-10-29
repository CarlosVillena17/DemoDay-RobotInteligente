#include <SoftwareSerial.h>

SoftwareSerial sw(2, 3); // 2 es rx y 3 es tx

int EnA = 10;
int int1 = 7;
int int2 = 6;
int int3 = 5;
int int4 = 4;

String receivedData = ""; // Para almacenar los datos recibos

void setup() {
  Serial.begin(9600);
  sw.begin(9600);
  pinMode(EnA, OUTPUT);
  pinMode(int1, OUTPUT);
  pinMode(int2, OUTPUT);
  pinMode(int3, OUTPUT);
  pinMode(int4, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char c = Serial.read();
    receivedData += c;
    Serial.print(c); // Imprime el carácter recibido
    checkCommands(receivedData);
  }

  if (sw.available() > 0) {
    char c = sw.read();
    receivedData += c;
    Serial.print(c); // Imprime el carácter recibido
    Serial.print(c); // Imprime el carácter recibido
    checkCommands(receivedData);
  }
}

void setMotorSpeed(int speed) {
  analogWrite(EnA, speed);
}

void moveMotors(int m1, int m2, int m3, int m4) {
  digitalWrite(int1, m1);
  digitalWrite(int2, m2);
  digitalWrite(int3, m3);
  digitalWrite(int4, m4);
}

void checkCommands(String data) {
  if (data.endsWith("arriba")) {
    setMotorSpeed(100);
    moveMotors(LOW, HIGH, LOW, HIGH);
  } else if (data.endsWith("abajo")) {
    setMotorSpeed(100);
    moveMotors(HIGH, LOW, HIGH, LOW);
  } else if (data.endsWith("derecha")) {
    setMotorSpeed(50);
    moveMotors(LOW, HIGH, HIGH, LOW);
    setMotorSpeed(70);
    delay(500);
    moveMotors(LOW, HIGH, LOW, HIGH);
    setMotorSpeed(100);
  } else if (data.endsWith("izquierda")) {
    setMotorSpeed(70);
    moveMotors(HIGH, LOW, LOW, HIGH);
    delay(500);
    moveMotors(LOW, HIGH, LOW, HIGH);
    setMotorSpeed(100);
  }else if (data.endsWith("stop")) {
    setMotorSpeed(100);
    moveMotors(LOW, LOW, LOW, LOW);
  }
}