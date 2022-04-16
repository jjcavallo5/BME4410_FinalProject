#include <LiquidCrystal.h>

char ch;
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);

  lcd.begin(16, 2);
}

void loop() {}

void serialEvent() {
  String str = "";
  
  while(Serial.available()){
    delay(10);
    str += (char)Serial.read();
  }

  lcd.clear();
  lcd.print(str);
  

  if (str.toInt() > 100){ 
    digitalWrite(LED_BUILTIN, HIGH);
  }
  else {
    digitalWrite(LED_BUILTIN, LOW);
  }
}
