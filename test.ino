char ch;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {}

void serialEvent() {
  while(Serial.available())
    ch = Serial.read();

  if (ch == '1') digitalWrite(LED_BUILTIN, HIGH);
  else digitalWrite(LED_BUILTIN, LOW);
}
