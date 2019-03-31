#include <LiquidCrystal_I2C.h> 
#include <Wire.h>

LiquidCrystal_I2C lcd(0x27,16,2);  //設定LCD位置0x27,設定LCD大小為16*2

const int WaterPin = 2, BlackTeaPin = 3, GreenTeaPin = 4, MilkPin = 5, ledPin = 7;//, SugarPin = 6;
int water_flag = 0, black_flag = 0, green_flag = 0, milk_flag = 0;
void setup() {
  // put your setup code here, to run once:
  lcd.init(); //初始化LCD 
  lcd.backlight(); //開啟背光
  Serial.begin(9600);
  pinMode(WaterPin,  OUTPUT);
  pinMode(BlackTeaPin,  OUTPUT);
  pinMode(GreenTeaPin,  OUTPUT);
  pinMode(MilkPin,  OUTPUT);
  pinMode(ledPin,  OUTPUT);
  
  digitalWrite(WaterPin, HIGH);
  digitalWrite(BlackTeaPin, HIGH);
  digitalWrite(GreenTeaPin, HIGH);
  digitalWrite(MilkPin, HIGH);
  //pinMode(SugarPin,  OUTPUT);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("    Welcome!!");
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()){
    switch(Serial.read()){
      case 'a':
      lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Pouring Water");
        Serial.println("low");
        digitalWrite(WaterPin, LOW);
    digitalWrite(ledPin, HIGH);
        break;
      case 'b':
        Serial.println("high");
        digitalWrite(WaterPin, HIGH);
        break;
       ///////////////////
      case 'c':
      lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Pouring BlackTea");
        Serial.println("low");
    digitalWrite(ledPin, HIGH);
       // if(water_flag == 0)
        //{
          digitalWrite(BlackTeaPin, LOW);
          water_flag = 1;
       // }
        break;
      case 'd':
        Serial.println("high");
        //if(water_flag == 1)
        //{
          digitalWrite(BlackTeaPin, HIGH);
          water_flag = 2;
        //}
        break;
      ///////////////////
      case 'e':
      lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Pouring GreenTea");
        Serial.println("low");
    digitalWrite(ledPin, HIGH);
        digitalWrite(GreenTeaPin, LOW);
        break;
      case 'f':
        Serial.println("high");
        digitalWrite(GreenTeaPin, HIGH);
        break;
      ///////////////////
      case 'g':
      lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Pouring Milk");
        Serial.println("low");
    digitalWrite(ledPin, HIGH);
        digitalWrite(MilkPin, LOW);
        break;
      case 'h':
        Serial.println("high");
        digitalWrite(MilkPin, HIGH);
        break;
    case 'i':
      lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("    ERROR!!!");
    lcd.setCursor(0, 1);
    lcd.print("Please Say Again");
    delay(1000);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("    Welcome!!");
        break;
    case 'j':
        digitalWrite(ledPin, LOW);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Mission");
    lcd.setCursor(0, 1);
    lcd.print("   Complete!!!");
    delay(1000);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("    Welcome!!");
        break;
    case 'k':
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Say something");
    lcd.setCursor(0, 1);
    lcd.print("       to drink");
        break;
    }
    //delay(20);
  }
  /*Serial.println("Hello");
  digitalWrite(ledPin, HIGH);
  delay(1000);
  digitalWrite(ledPin, LOW);
  delay(1000);*/
}