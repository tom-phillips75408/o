const int tempPin = A0;      // Temperature sensor (TMP36) connected to Analog Pin 
A0 
const int motorPin = 9;      // Transistor base connected to PWM Pin 9 to control 
motor 
const int ledPin = 10;       // Status LED connected to Digital Pin 10 
 
// Safety threshold. If the motor's temperature exceeds this, it shuts down. 
const float overheatThreshold = 50.0;  
 
// The normal operating speed for the motor 
const int normalMotorSpeed = 200; // A value between 0 (off) and 255 (max) 
 
void setup() { 
  // Initialize Serial communication for monitoring 
  Serial.begin(9600); 
   
  // Set the pin modes 
  pinMode(motorPin, OUTPUT); 
  pinMode(ledPin, OUTPUT); 
} 
 
void loop() { 
  // 1. SENSE: Read the raw value from the temperature sensor 
  int sensorVal = analogRead(tempPin); 
 
  // 2. PROCESS: Convert the raw sensor reading to a temperature in Celsius 
  float voltage = (sensorVal / 1023.0) * 5.0; 
  float temperatureC = (voltage - 0.5) * 100; 
 
  // 3. MONITOR: Print the data to the Serial Monitor (our simple dashboard) 
  Serial.print("Motor Temperature: "); 
  Serial.print(temperatureC); 
  Serial.print(" C | "); 
 
  // 4. ACTUATE based on the new PROTECTIVE logic 
  if (temperatureC >= overheatThreshold) { 
    // Condition: OVERHEATED! Take protective action. 
     
    // Shut down the motor completely 
    analogWrite(motorPin, 0);  
     
    // Blink the LED to signal a critical alert 
    digitalWrite(ledPin, HIGH); 
    delay(250); 
    digitalWrite(ledPin, LOW); 
    delay(250); 
     
    Serial.println("Status: DANGER - OVERHEATED! Motor has been shut down."); 
     
  } else { 
    // Condition: Normal. Temperature is within safe limits. 
     
    // Run the motor at its normal speed 
    analogWrite(motorPin, normalMotorSpeed);  
     
    // Ensure the alert LED is off 
    digitalWrite(ledPin, LOW);  
     
    Serial.println("Status: Normal Operation. Motor ON."); 
  } 
} 