void setup() {
  Serial.begin(9600);
  
}

void loop() {
  int sensorValue = analogRead(TEMP_SENSOR);

    Serial.print("Raw Value: ");
    Serial.print(sensorValue);
    delay(1000);
}