#define dirPin1 3 
#define stepPin1 4

#define dirPin2 5 
#define stepPin2 6

void setup() {
  // put your setup code here, to run once:
    pinMode(stepPin1,OUTPUT); 
    pinMode(dirPin1,OUTPUT);

    pinMode(stepPin2,OUTPUT); 
    pinMode(dirPin2,OUTPUT);
    Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  // Serial.println("Hello World!");
  // delay(1000);
  digitalWrite(dirPin1,HIGH); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
  for(int x = 0; x < 1600; x++) {
    digitalWrite(stepPin1,HIGH); 
    delayMicroseconds(500);    // by changing this time delay between the steps we can change the rotation speed
    digitalWrite(stepPin1,LOW); 
    delayMicroseconds(500); 
  }
  delay(1000); // One second delay
  Serial.println("testing 3\n");
  digitalWrite(dirPin1,LOW); //Changes the rotations direction
  // Makes 400 pulses for making two full cycle rotation
  for(int x = 0; x < 1600; x++) {
    digitalWrite(stepPin1,HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin1,LOW);
    delayMicroseconds(500);
  }
  delay(1000);

  digitalWrite(dirPin2,HIGH); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
  for(int x = 0; x < 1600; x++) {
    digitalWrite(stepPin2,HIGH); 
    delayMicroseconds(500);    // by changing this time delay between the steps we can change the rotation speed
    digitalWrite(stepPin2,LOW); 
    delayMicroseconds(500); 
  }
  delay(1000); // One second delay
  Serial.println("testing 3\n");
  digitalWrite(dirPin2,LOW); //Changes the rotations direction
  // Makes 400 pulses for making two full cycle rotation
  for(int x = 0; x < 1600; x++) {
    digitalWrite(stepPin2,HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin2,LOW);
    delayMicroseconds(500);
  }
  delay(1000);
}
