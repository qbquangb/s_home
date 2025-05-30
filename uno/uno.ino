#include <string.h>
String data;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(13, OUTPUT);
digitalWrite(13, 0);
}

void loop() {
  // put your main code here, to run repeatedly:
if (Serial.available())
  {
  data=Serial.readStringUntil('\r');
  if (data == "bat")
    {
    digitalWrite(13, 1);
    Serial.println("Dabatcoi");
    delay(25000);
    digitalWrite(13, 0);
    Serial.println("Datatcoi");
    delay(10000);
    }
  }
}