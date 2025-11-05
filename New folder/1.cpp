const int sensorPin = A0;   // Vout of the temperature sensor 
const int ledPin    = 7;    // LED anode (+) directly (Tinkercad OK) 
const int buzzerPin = 8;    // Optional buzzer + 
const float limitC  = 30.0; // Alert threshold in °C 
void setup() { 
Serial.begin(9600);            
// Open Serial Monitor at 9600 baud 
pinMode(ledPin, OUTPUT); 
pinMode(buzzerPin, OUTPUT); 
} 
void loop() { 
// 1. Read analog value and convert to volts 
int raw = analogRead(sensorPin); 
float voltage = (raw * 5.0) / 1023.0; 
// 2. Convert voltage to temperature (LM35 = 10 mV per °C) 
float tempC = voltage * 100.0; 
// 3. Display temperature in °C 
Serial.print("Temperature: "); 
Serial.print(tempC); 
Serial.println(" C"); 
// 4. Alert if temperature is above limit 
if (tempC > limitC) { 
Serial.println("ALERT: High Temperature!"); 
digitalWrite(ledPin, HIGH); 
digitalWrite(buzzerPin, HIGH); 
} else { 
digitalWrite(ledPin, LOW); 
digitalWrite(buzzerPin, LOW); 
} 
delay(1000); // Update once per second 
}