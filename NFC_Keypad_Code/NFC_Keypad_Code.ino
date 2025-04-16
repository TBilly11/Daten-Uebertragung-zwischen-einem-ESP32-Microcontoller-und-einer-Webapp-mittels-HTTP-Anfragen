#include <WiFi.h>
#include <HTTPClient.h>
#include <SPI.h>
#include <MFRC522.h>
#include <string.h>
#include <ArduinoJson.h>
#include <ESP32Servo.h> 
 
#define SS_PIN 21
#define RST_PIN 22
MFRC522 mfrc522(SS_PIN, RST_PIN);

#include "FS.h"
#include <TFT_eSPI.h>      // Hardware-specific library
TFT_eSPI tft = TFT_eSPI(); // Invoke custom library
// This is the file name used to store the calibration data
// You can change this to create new calibration files.
// The SPIFFS file name must start with "/".
#define CALIBRATION_FILE "/TouchCalData1"

// Set REPEAT_CAL to true instead of false to run calibration
// again, otherwise it will only be done once.
// Repeat calibration if you change the screen rotation.
#define REPEAT_CAL false

// Keypad start position, key sizes and spacing
#define KEY_X 40 // Centre of key
#define KEY_Y 96
#define KEY_W 62 // Width and height
#define KEY_H 30
#define KEY_SPACING_X 18 // X and Y gap
#define KEY_SPACING_Y 20
#define KEY_TEXTSIZE 1   // Font size multiplier

// Using two fonts since numbers are nice when bold
#define LABEL1_FONT &FreeSansOblique12pt7b // Key label font 1
#define LABEL2_FONT &FreeSansBold12pt7b    // Key label font 2

// Numeric display box size and location
#define DISP_X 1
#define DISP_Y 10
#define DISP_W 238
#define DISP_H 50
#define DISP_TSIZE 3
#define DISP_TCOLOR TFT_CYAN

// Number length, buffer for storing it and character index
#define NUM_LEN 12
char numberBuffer[NUM_LEN + 1] = "";
uint8_t numberIndex = 0;

// We have a status line for messages
#define STATUS_X 120 // Centred on this
#define STATUS_Y 65

// Create 15 keys for the keypad
char keyLabel[15][7] = {"Neu", "X", "Send", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "0", "#" };
uint16_t keyColor[15] = {TFT_RED, TFT_DARKGREY, TFT_DARKGREEN,
                         TFT_BLUE, TFT_BLUE, TFT_BLUE,
                         TFT_BLUE, TFT_BLUE, TFT_BLUE,
                         TFT_BLUE, TFT_BLUE, TFT_BLUE,
                         TFT_BLUE, TFT_BLUE, TFT_BLUE
                        };

// Invoke the TFT_eSPI button class and create all the button objects
TFT_eSPI_Button key[15];

//------------------------------------------------------------------------------------------


const char* ssid = "TP-Link_C2E4";
const char* password = "68365202";

//const char* ssid = "TBILLY11";
//const char* username = "s0572869";
//const char* password = "tnbg1234";


String NFC_Code="";
String payload1;
String payload2;
String payload3;
String response2;
String response1;
bool oneFactor_statut;
char one_factor_code[13];
int password_6;
bool check = 0;
char password_6_str[7];
uint8_t b;
const int gruen_LED = 12;
const int rot_LED = 14;
// Allouez un objet JSON
StaticJsonDocument<200> doc1;
StaticJsonDocument<200> doc2;
Servo meinServo;

void setup() {

  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("Approximate your card to the reader...");
  Serial.println();
 

  WiFi.begin(ssid, password);
  //WiFi.begin(ssid, username, password, 0);
  while (WiFi.status() != WL_CONNECTED) {
  delay(1000);
  Serial.println("Connecting to WiFi...");

  pinMode(gruen_LED, OUTPUT);
  pinMode(rot_LED, OUTPUT);
  // Initialise the TFT screen
  tft.init();

  // Set the rotation before we calibrate
  tft.setRotation(0);

   // Calibrate the touch screen and retrieve the scaling factors
  touch_calibrate();
  
  // Clear the screen
  tft.fillScreen(TFT_BLACK);

  // Draw keypad background
  tft.fillRect(0, 0, 240, 320, TFT_DARKGREY);

  // Draw number display area and frame
  tft.fillRect(DISP_X, DISP_Y, DISP_W, DISP_H, TFT_BLACK);
  tft.drawRect(DISP_X, DISP_Y, DISP_W, DISP_H, TFT_WHITE);

  // Parsez le contenu
  // Draw keypad
  drawKeypad();

  meinServo.attach(13);  // Attache le servomoteur à la broche 15
  meinServo.write(0);    // Initialise le servomoteur à 0 degrés
}
}

void keypad_pin(){
  
  uint16_t t_x = 0, t_y = 0; // To store the touch coordinates

  // Pressed will be set true is there is a valid touch on the screen
  bool pressed = tft.getTouch(&t_x, &t_y);

  // / Check if any key coordinate boxes contain the touch coordinates
  for ( b = 0; b < 15; b++) {               //uint8_t 
    if (pressed && key[b].contains(t_x, t_y)) {
      key[b].press(true);  // tell the button it is pressed
    } else {
      key[b].press(false);  // tell the button it is NOT pressed
    }
  }

  // Check if any key has changed state
  for (b = 0; b < 15; b++) {

    if (b < 3) tft.setFreeFont(LABEL1_FONT);
    else tft.setFreeFont(LABEL2_FONT);

    if (key[b].justReleased()) key[b].drawButton();     // draw normal

    if (key[b].justPressed()) {
      key[b].drawButton(true);  // draw invert

      // if a numberpad button, append the relevant # to the numberBuffer
      if (b >= 3) {
        if (numberIndex < NUM_LEN) {
          numberBuffer[numberIndex] = keyLabel[b][0];
          numberIndex++;
          numberBuffer[numberIndex] = 0; // zero terminate
        }
        status(""); // Clear the old status
      }

      // Del button, so delete last char
      if (b == 1) {
        numberBuffer[numberIndex] = 0;
        if (numberIndex > 0) {
          numberIndex--;
          numberBuffer[numberIndex] = 0;//' ';
        }
        status(""); // Clear the old status
      }

      if (b == 2) {
        status("Sent value to serial port");
        Serial.println(numberBuffer);  
        if(strlen(numberBuffer)==8){
         HTTPClient http;
         http.begin("http://192.168.0.101:8000/api/one_factor_auth"); // 192.168.0.101
         http.addHeader("Content-Type", "application/x-www-form-urlencoded");
         String payload1 = "one_factor_code=" + String (numberBuffer);
         numberIndex = 0; // Reset index to 0
         numberBuffer[numberIndex] = 0; // Place null in buffer
         Serial.println(payload1);
         int httpCode = http.POST(payload1);
         response1 = http.getString();
         Serial.println("Response code: " + String(httpCode));
         Serial.println("Response body: " + response1);
         const char* json1 = response1.c_str();
         DeserializationError error1 = deserializeJson(doc1, json1);
              if (error1) {
                   Serial.print(F("deserializeJson() ist fehlgeschlagen mit dem Fehlercode: "));
                   Serial.println(error1.c_str());
                   return;
            }
        oneFactor_statut = doc1["one_factor"];
        String code = doc1["one_factor_code"].as<String>();
        strncpy(one_factor_code, code.c_str(), sizeof(one_factor_code));
         
        http.end();}

      if(strlen(numberBuffer)==6){
        const char* json2 = response2.c_str();
        DeserializationError error2 = deserializeJson(doc2, json2);
        if (error2) {
        Serial.print(F("deserializeJson() a échoué avec le code : "));
        Serial.println(error2.c_str());
        return;
                } 
        const char* password_str = doc2["password"];
        password_6 = strtol(password_str, NULL, 10);
        sprintf(password_6_str, "%06d", password_6);
        Serial.println(numberBuffer);Serial.print(password_6_str);
        if(strcmp(numberBuffer, password_6_str) == 0){
            check = true;
               Serial.println(check);
        }
        numberIndex = 0; // Reset index to 0
        numberBuffer[numberIndex] = 0; // Place null in buffer
        
       }

       if((check!=1 && oneFactor_statut!=1)){  //||strlen(numberBuffer)==6 && check!=1){
           
             digitalWrite(rot_LED, HIGH); 
             delay(2000);
             digitalWrite(rot_LED, LOW);
        }
       numberIndex = 0; // Reset index to 0
        numberBuffer[numberIndex] = 0; // Place null in buffer 
      }
      
       
      // we dont really check that the text field makes sense
      // just try to call
      if (b == 0) {
        status("Value cleared");
        numberIndex = 0; // Reset index to 0
        numberBuffer[numberIndex] = 0; // Place null in buffer
      }

      // Update the number display field
      tft.setTextDatum(TL_DATUM);        // Use top left corner as text coord datum
      tft.setFreeFont(&FreeSans18pt7b);  // Choose a nicefont that fits box
      tft.setTextColor(DISP_TCOLOR);     // Set the font colour

      // Draw the string, the value returned is the width in pixels
      int xwidth = tft.drawString(numberBuffer, DISP_X + 4, DISP_Y + 12);

      // Now cover up the rest of the line up by drawing a black rectangle.  No flicker this way
      // but it will not work with italic or oblique fonts due to character overlap.
      tft.fillRect(DISP_X + 4 + xwidth, DISP_Y + 1, DISP_W - xwidth - 5, DISP_H - 2, TFT_BLACK);

      delay(10); // UI debouncing
    }
  }
}

void NFC_Reader(){
    NFC_Code="";
    byte letter;
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      NFC_Code.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : ""));
      NFC_Code.concat(String(mfrc522.uid.uidByte[i], HEX));
      NFC_Code.toUpperCase();
    }
    }
    
// Funktion send_PIN_to_User definiert
void send_PIN_to_User(){
  NFC_Reader();
// HTTPClient-Instanz erstellen  
  HTTPClient http;
// HTTP-Anfrage an URL senden
  http.begin("http://192.168.0.101:8000/api/send_mail");  // 192.168.137.1//192.168.0.101
// HTTP-Header hinzufügen
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
// HTTP-Body (Anfrageparameter) erstellen
  payload2 ="nfc="+NFC_Code;
  Serial.println(payload2);
// HTTP-Anfrage mit dem gegebenen HTTP-Body senden und den HTTP-Statuscode erhalten
  int httpCode = http.POST(payload2);
// HTTP-Antwort (Response) als String abrufen
  response2 = http.getString();
  Serial.println("Response code: " + String(httpCode));
  Serial.println("Response body: " + response2);
  http.end();
  delay(1000);
 
  }

  //------------------------------------------------------------------------------------------

void drawKeypad()
{
  // Draw the keys
  for (uint8_t row = 0; row < 5; row++) {
    for (uint8_t col = 0; col < 3; col++) {
      uint8_t b = col + row * 3;

      if (b < 3) tft.setFreeFont(LABEL1_FONT);
      else tft.setFreeFont(LABEL2_FONT);

      key[b].initButton(&tft, KEY_X + col * (KEY_W + KEY_SPACING_X),
                        KEY_Y + row * (KEY_H + KEY_SPACING_Y), // x, y, w, h, outline, fill, text
                        KEY_W, KEY_H, TFT_WHITE, keyColor[b], TFT_WHITE,
                        keyLabel[b], KEY_TEXTSIZE);
      key[b].drawButton();
    }
  }
}

//------------------------------------------------------------------------------------------

void touch_calibrate()
{
  uint16_t calData[5];
  uint8_t calDataOK = 0;

  // check file system exists
  if (!SPIFFS.begin()) {
    Serial.println("Formating file system");
    SPIFFS.format();
    SPIFFS.begin();
  }

  // check if calibration file exists and size is correct
  if (SPIFFS.exists(CALIBRATION_FILE)) {
    if (REPEAT_CAL)
    {
      // Delete if we want to re-calibrate
      SPIFFS.remove(CALIBRATION_FILE);
    }
    else
    {
      File f = SPIFFS.open(CALIBRATION_FILE, "r");
      if (f) {
        if (f.readBytes((char *)calData, 14) == 14)
          calDataOK = 1;
        f.close();
      }
    }
  }

  if (calDataOK && !REPEAT_CAL) {
    // calibration data valid
    tft.setTouch(calData);
  } else {
    // data not valid so recalibrate
    tft.fillScreen(TFT_BLACK);
    tft.setCursor(20, 0);
    tft.setTextFont(2);
    tft.setTextSize(1);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);

    tft.println("Touch corners as indicated");

    tft.setTextFont(1);
    tft.println();

    if (REPEAT_CAL) {
      tft.setTextColor(TFT_RED, TFT_BLACK);
      tft.println("Set REPEAT_CAL to false to stop this running again!");
    }

    tft.calibrateTouch(calData, TFT_MAGENTA, TFT_BLACK, 15);

    tft.setTextColor(TFT_GREEN, TFT_BLACK);
    tft.println("Calibration complete!");

    // store data
    File f = SPIFFS.open(CALIBRATION_FILE, "w");
    if (f) {
      f.write((const unsigned char *)calData, 14);
      f.close();
    }
  }
}

//------------------------------------------------------------------------------------------

// Print something in the mini status bar
void status(const char *msg) {
  tft.setTextPadding(240);
  //tft.setCursor(STATUS_X, STATUS_Y);
  tft.setTextColor(TFT_WHITE, TFT_DARKGREY);
  tft.setTextFont(0);
  tft.setTextDatum(TC_DATUM);
  tft.setTextSize(1);
  tft.drawString(msg, STATUS_X, STATUS_Y);
}

//------------------------------------------------------------------------------------------

void record_login_entry(){
  
  HTTPClient http;

  http.begin("http://192.168.0.101:8000/api/login_entry");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  if(check==1){
     payload3 = "code=" + NFC_Code + "&auth_type=Zwei Faktor-Authentifizierung";
  }
  if(oneFactor_statut==1){ 
     payload3 = "code="+ String(one_factor_code) + "&auth_type=Ein Faktor-Authentifizierung";
  }
  Serial.println(payload3);
  int httpCode = http.POST(payload3);
 
  String response3 = http.getString();
 
  Serial.println("Response code: " + String(httpCode));
  Serial.println("Response body: " + response3);
  http.end();
  delay(1000);
  }

void mein_Servo_Motor(){
    digitalWrite(gruen_LED, HIGH);
    for (int i = 90; i >= 0; i -= 10) {
    meinServo.write(i);    
    delay(100);         
  }
   delay(4000);
   digitalWrite(gruen_LED, LOW);
  delay(4000);           
  for (int i = 0; i <= 90; i += 10) {
    meinServo.write(i);    
    delay(100);          
  }
  delay(100);            
 
    }

void loop() {
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
  //NFC_Reader();
  send_PIN_to_User();
   }
   
keypad_pin();
//Serial.println(check);

if(check==1 || oneFactor_statut== 1){    
mein_Servo_Motor();
Serial.println(NFC_Code);
Serial.println(one_factor_code);
record_login_entry();
} 
oneFactor_statut = 0;
check=0;
}
