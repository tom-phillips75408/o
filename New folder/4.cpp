String PASSWORD = "1234";   // set your password here 
String inputCode = ""; 
const int buzzer = 7; 
const int greenLED = 8; 
const int redLED = 9; 
void setup() { 
pinMode(greenLED, OUTPUT); 
pinMode(redLED, OUTPUT); 
pinMode(buzzer, OUTPUT); 
digitalWrite(greenLED, LOW); 
digitalWrite(redLED, LOW); 
digitalWrite(buzzer, LOW); 
Serial.begin(9600); 
Serial.println("== Password Authentication with Buzzer =="); 
Serial.println("Enter password:"); 
} 
 
void loop() { 
  if (Serial.available()) { 
    inputCode = Serial.readStringUntil('\n');  // read until Enter 
    inputCode.trim();  // remove spaces/newlines 
 
    Serial.print("Entered: "); 
    Serial.println(inputCode); 
 
    if (inputCode == PASSWORD) { 
      Serial.println("Correct Password!"); 
      digitalWrite(greenLED, HIGH);   // green LED ON 
      delay(5000);                    // keep green LED ON for 5 sec 
      digitalWrite(greenLED, LOW);    // turn OFF green LED after 5 sec 
    }  
    else { 
      Serial.println("Wrong Password!"); 
      // blink red LED + beep 3 times 
      for (int i = 0; i < 3; i++) { 
        digitalWrite(redLED, HIGH); 
        digitalWrite(buzzer, HIGH); 
        delay(300); 
        digitalWrite(redLED, LOW); 
        digitalWrite(buzzer, LOW); 
        tone(buzzer, 1000, 500);  
        delay(300); 
      } 
    } 
     
    Serial.println("Enter password:"); 
    inputCode = "";  // reset 
  } 
} 
 