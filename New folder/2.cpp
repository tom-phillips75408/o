const int pirPin    = 2;   // PIR sensor output pin 
const int ledPin    = 3;   // LED pin 
const int buzzerPin = 4;   // Buzzer pin 
 
int pirState = LOW;        // Tracks previous motion state 
 
void setup() { 
  pinMode(pirPin, INPUT); 
  pinMode(ledPin, OUTPUT); 
  pinMode(buzzerPin, OUTPUT); 
 
  Serial.begin(9600); 
  Serial.println("PIR Motion Detector Ready."); 
} 
 
void loop() { 
  int motion = digitalRead(pirPin); 
 
  if (motion == HIGH) { 
    digitalWrite(ledPin, HIGH); 
    playPoojaTone();                // Play three-note chime 
 
    if (pirState == LOW) {          // Only print once when motion starts 
      Serial.println("Motion Detected!"); 
      pirState = HIGH; 
    } 
  } else { 
    digitalWrite(ledPin, LOW); 
    noTone(buzzerPin);              // Stop buzzer tone 
 
if (pirState == HIGH) {         
// Only print once when motion ends 
Serial.println("Motion Ended."); 
pirState = LOW; 
} 
} 
} 
void playTone() { 
// Three quick ascending notes like a small bell 
tone(buzzerPin, 800);   delay(200); 
tone(buzzerPin, 1000);  delay(200); 
tone(buzzerPin, 1200);  delay(200); 
noTone(buzzerPin);  delay(200);     
} 