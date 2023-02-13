/*
  WiFi UDP Send and Receive String

 This sketch waits for a UDP packet on localPort using the WiFi module.
 When a packet is received an Acknowledge packet is sent to the client on port remotePort

 created 30 December 2012
 by dlf (Metodo2 srl)

 */
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define OLED_RESET     4 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#include <SPI.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>
#include <IRremote.h>

IRsend irsend(8);

int RECV_PIN = 11;

IRrecv irrecv(RECV_PIN);

decode_results results;

String playerHit = "";


int status = WL_IDLE_STATUS;

///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = "Bonfield 3502";        // your network SSID (name)
char pass[] = "Amber123";    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;            // your network key index number (needed only for WEP)

unsigned int localPort = 2390; 
unsigned int localPort2 = 2380;
unsigned int localPort3 = 2370;// local port to listen on

char packetBuffer[256];
char packetBuffer2[256];
char packetBuffer3[256];//buffer to hold incoming packet
char  ReplyBuffer[] = "acknowledged";       // a string to send back

WiFiUDP Udp;
WiFiUDP Udp2;
WiFiUDP Udp3;
IPAddress remoteIp = (192,168,4,128);
unsigned long starttime = 0;
unsigned long old = 0;
unsigned long buttonDelay = 0;
unsigned long buttonOld = 0;
int triggerState = 0;
int LEDState=0;
const int buttonPin = 2;
int buttonState = 0;         // variable for reading the pushbutton status

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(12, OUTPUT);
  pinMode(12, HIGH);
  pinMode(9, OUTPUT);
  digitalWrite(9, HIGH);

  pinMode(7, OUTPUT);
  digitalWrite(7, HIGH);
  pinMode(6, OUTPUT);
  digitalWrite(6, HIGH);
  
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }


  display.clearDisplay();

  display.setTextSize(1);      // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE); // Draw white text
  display.setCursor(0, 0);     // Start at top-left corner
  display.cp437(true);         // Use full 256 char 'Code Page 437' font

  // Not all the characters will fit on the display. This is normal.
  // Library will draw what it can and the rest will be clipped.
 display.write("Connecting");

  display.display();

  
  


  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true);
  }

  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }

  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(1000);
  }
  Serial.println("Connected to WiFi");
  printWifiStatus();

  Serial.println("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  Udp.begin(localPort);
  Udp2.begin(localPort2);
  Udp3.begin(localPort3);
  display.clearDisplay();
   
}

void loop() {

  buttonState = digitalRead(buttonPin);
  
  if (buttonState == LOW) {
   buttonDelay = millis();
    if (buttonDelay-buttonOld > 1000){
      buttonOld=buttonDelay;

    irsend.sendSony(0xa70, 12);
      Udp2.beginPacket(Udp2.remoteIP(), Udp2.remotePort());
      Udp2.write("fire");
      Udp2.endPacket();
      digitalWrite(13, HIGH);
      delay(100);
      digitalWrite(13, LOW);
      
    }
  } else {
    // turn LED off:
    digitalWrite(13, LOW);
  }

  starttime = millis();
  if (starttime-old> 1000){
    old = starttime;
    if (LEDState == 0){
      LEDState = 1; 
      display.clearDisplay();
      display.setTextSize(2);    
      display.setCursor(0, 0);     // Start at top-left corner
      display.print(packetBuffer);
      display.display();
      }else {
        LEDState = 0; 
        display.clearDisplay();
        display.setTextSize(2);    
        display.setCursor(0, 0);     // Start at top-left corner
        display.print(packetBuffer3);
        display.display();
        }
    }

   

  if(irrecv.decode(&results)){
    playerHit = String(results.value, HEX);
    Serial.println(playerHit);
    char message[50];
    playerHit.toCharArray(message, 50);
    Udp2.beginPacket(Udp2.remoteIP(), Udp2.remotePort());
      Udp2.write("a70");
      Udp2.endPacket();
    irrecv.resume(); 
    }


    
  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    Serial.print("Received packet of size ");
    Serial.println(packetSize);
    Serial.print("From ");
    Serial.print(remoteIp);
    Serial.print(", port ");
    Serial.println(Udp.remotePort());

    // read the packet into packetBufffer
    int len = Udp.read(packetBuffer, 255);
    if (len > 0) {
      packetBuffer[len] = 0;
    }
    Serial.println("Contents:");
    Serial.println(packetBuffer);
    
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write(ReplyBuffer);
    Udp.endPacket();
  }
   int packetSize3 = Udp3.parsePacket();
  if (packetSize3) {
    Serial.print("Received packet of size ");
    Serial.println(packetSize3);
    Serial.print("From ");
    Serial.print(remoteIp);
    Serial.print(", port ");
    Serial.println(Udp3.remotePort());

    // read the packet into packetBufffer
    int len = Udp3.read(packetBuffer3, 255);
    if (len > 0) {
      packetBuffer3[len] = 0;
    }
    Serial.println("Contents:");
    Serial.println(packetBuffer3);

    Udp3.beginPacket(Udp3.remoteIP(), Udp3.remotePort());
    Udp3.write(ReplyBuffer);
    Udp3.endPacket();
  }


   int packetSize2 = Udp2.parsePacket();
  if (packetSize2) {
    Serial.print("Received packet of size ");
    Serial.println(packetSize2);
    Serial.print("From ");

    Serial.print(remoteIp);
    Serial.print(", port ");
    Serial.println(Udp2.remotePort());

    // read the packet into packetBufffer
    int len = Udp2.read(packetBuffer2, 255);
    if (len > 0) {
      packetBuffer2[len] = 0;
    }
    Serial.println("Contents:");
    Serial.println(packetBuffer2);
    if (strcmp(packetBuffer,"1") == 0){
      Serial.print("Activate");
      }

    // send a reply, to the IP address and port that sent us the packet we received
    Udp2.beginPacket(Udp2.remoteIP(), Udp2.remotePort());
    Udp2.write(ReplyBuffer);
    Udp2.endPacket();
  }
}


void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
