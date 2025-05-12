#include <FastLED.h>
#include <CuBeX.h>
#include <WiFi.h>

//definisco i pin I2C
#define SDA 21      //pin
#define SCL 22      //pin

//definisco velocità, lunghezza mosse e ritardi
#define vel     120 //rpm
#define step90  50  //passi
#define step180 100 //passi
#define pausaM  30  //millisecondi
#define velCUS  50  //rpm
#define stepCUS 200 //passi

//definisco i led usati dal programma
#define pinled  32  //pin
#define NLED    48  //numero led
CRGB leds[NLED];

//definisco pin pulsanti/led vari
#define rele    23  //pin enable motori
#define servo1  13  //pin servomotori
#define servo2  12
#define servo3  14
#define servo4  27
#define lverde  33  //pin luci
#define lrosso  25
#define lbianco 26
#define pverde  39  //pin pulsanti
#define prosso  34
#define pbianco 35
#define led     19  //pin led sulla scheda
#define P1      18  //pin pulsanti sulla scheda
#define P2      17

//mosse randomizzate
#define randomizzazione 30

//informazioni della rete per la connessione (inserisci ssid e password della rete alla quale vuoi collegare la macchina)
const char* ssid = " ";
const char* password = " ";

//vettori dove salvare i colori del cubo
int fW[9] = { 0, 0, 0, 0, 1, 0, 0, 0, 0 };
int fY[9] = { 0, 0, 0, 0, 2, 0, 0, 0, 0 };
int fG[9] = { 0, 0, 0, 0, 3, 0, 0, 0, 0 };
int fB[9] = { 0, 0, 0, 0, 4, 0, 0, 0, 0 };
int fR[9] = { 0, 0, 0, 0, 5, 0, 0, 0, 0 };
int fO[9] = { 0, 0, 0, 0, 6, 0, 0, 0, 0 };

//altre variabili che servono al programma
int i=0, j=0, y=0, lum=0, luce=0, fatto=0, statotasti=1, color=0, mtt=0, tgs=0, err=0, timeout = 0, messaggio = 0, colore = 1, scramble=0, ser=1, percentuale=0;
int algoritmo[250];
int stringa[48];
unsigned long mill=0;
unsigned long tempointernet=0;
unsigned long tbuf=0;

//inizializzazione del server
WiFiServer server(80);  // creo il server e lo setto sulla porta 80
String header;          //variabile per salvare la richiesta del client

void setup() {
  pinMode(rele,    OUTPUT);
  digitalWrite(rele,  LOW);
  pinMode(lverde,  OUTPUT);
  pinMode(lrosso,  OUTPUT);
  pinMode(lbianco, OUTPUT);
  pinMode(pverde,   INPUT);
  pinMode(prosso,   INPUT);
  pinMode(pbianco,  INPUT);
  pinMode(P1,       INPUT);
  pinMode(P2,       INPUT);
  pinMode(led,     OUTPUT);
  stepper_init(SDA, SCL, 0x21, 0x20, 0x22);   //inizializzo i motori
  FastLED.addLeds<WS2812, pinled, GRB>(leds,NLED);  //inizializzo i led
  for(i=0;i<NLED;i++){
    leds[i]=CRGB(0,0,0);
  }
  FastLED.show();
  Serial.begin(115200);
  if(digitalRead(P2) == 1){
    ser=0;
    digitalWrite(led, HIGH);
  }else{
    digitalWrite(led, LOW);
  }
  servo_1(servo1,58,145);           //funzione per creare i servomotori servo*(pin, angolo da chiuso, angolo da aperto);
  servo_2(servo2,65,151);
  servo_3(servo3,60,144);
  servo_4(servo4,62,147);
  servo_op();
  digitalWrite(rele,HIGH);
  //connessione alla rete
  Serial.print("\nConnessione a: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  i=0;
  Serial.print(".");
  while (WiFi.status() != WL_CONNECTED && i<=20) {
    i++;
    delay(300);
    Serial.print(".");
  }
  //scrivi l'ip e inizializza il server
  if(i<=20){
    Serial.println("\nCONNESSO");
    Serial.print("indirizzo IP: ");
    Serial.println(WiFi.localIP());
    server.begin();
  }else{
    Serial.println("\nUSCITO");
  }
  i=0;
  for(i=0;i<NLED;i++){
    leds[i]=CRGB(0,0,0);
  }
  FastLED.show();
  delay(500);
  animazioneavvio();
}

void loop() {
  if(digitalRead(P2) == 1){
    ser=0;
    digitalWrite(led, HIGH);
  }
  if(digitalRead(P1) == 1){
    ser=1;
    digitalWrite(led, LOW);
  }
  if(ser == 0){
    internet();
  }else{
    seriale();
  }
  if(digitalRead(pbianco)==1&&scramble==0&&lum>0){
    scramble=2;
    if(statotasti==2){
      statotasti=1;
    }
    if(luce>10){
      while(luce>0){
        luci();
        delay(3);
        if(millis()-mill>100&&lum>0){
          refresh();
        }
      }
    }
    randomSeed(millis());
    for(i=1;i<=250;i++){
      algoritmo[i-1] = 0;
    }
    for(i=1;i<=randomizzazione;i++){
      algoritmo[i-1] = random(1,19);
    }
    mtt=randomizzazione;
    statotasti=3;
  }
  if(scramble > 0&&lum>0){
    if(digitalRead(pverde)==1){
      if(luce>10){
         while(luce>0){
          luci();
          delay(3);
          if(millis()-mill>100&&lum>0){
            refresh();
          }
        }
      }
      statotasti=5;
      if(lum>0){
        for(lum=100;lum>=0;lum=lum-5){
          for(i=0;i<10;i++){
            delay(10);
            luci();
          }
          refresh();
        }
        lum=0;
      }
      while(digitalRead(pverde)==1){
        delay(10);
        luci();
      }
      delay(10);
      step();
    }
  }
  if(millis()-tempointernet>10000&&lum==0){
    if(scramble==0){
      statotasti=1;
    }else{
      statotasti=3;
    }
    for(lum=0;lum<=100;lum=lum+5){
      for(i=0;i<10;i++){
        delay(10);
        luci();
      }
      refresh();
    }
  }
  if(lum==0&&luce>0){
    while(luce>0){
      luci();
      delay(10);
    }    
  }
  if((millis()-mill>10&&lum>0)&&fatto==0){
    luci();
    fatto++;
  }
  if((millis()-mill>20&&lum>0)&&fatto==1){
    luci();
    fatto++;
  }
  if((millis()-mill>30&&lum>0)&&fatto==2){
    luci();
    fatto++;
  }
  if((millis()-mill>40&&lum>0)&&fatto==3){
    luci();
    fatto++;
  }
  if((millis()-mill>50&&lum>0)&&fatto==4){
    luci();
    fatto++;
  }
  if((millis()-mill>60&&lum>0)&&fatto==5){
    luci();
    fatto++;
  }
  if((millis()-mill>70&&lum>0)&&fatto==6){
    luci();
    fatto++;
  }
  if((millis()-mill>80&&lum>0)&&fatto==7){
    luci();
    fatto++;
  }
  if((millis()-mill>90&&lum>0)&&fatto==8){
    fatto++;
    luci();
  }
  if(millis()-mill>100&&lum>0){
    fatto=0;
    luci();
    refresh();
  }
}

void step(){
  servo_cl();
  //eseguo le mosse
  mill=millis();
  while(scramble!=10){
    if(millis()-mill>10){
      luci();
      mill=millis();
    }
    if(digitalRead(prosso)==1&&(statotasti==5||statotasti==6||statotasti==9||statotasti==10)){
      if(statotasti<=6){
        statotasti=6;
      }else{
        statotasti=10;
      }
      if(luce>10){
        while(luce>0){
          luci();
          delay(3);
        }
      }
      statotasti=1;
      servo_op();
      scramble=10;
      while(digitalRead(prosso)==1){
        delay(10);
        luci();
      }
      delay(10);
    }
    if(digitalRead(pverde)==1&&(statotasti==5||statotasti==6)){
      statotasti=6;
      if(luce>10){
        while(luce>0){
          luci();
          delay(3);
        }
      }
      statotasti=7;
      while(digitalRead(pverde)==1){
        delay(10);
        luci();
      }
      delay(10);
    }
    if(digitalRead(pbianco)==1&&(statotasti==5||statotasti==6)){
      statotasti=6;
      if(luce>10){
        while(luce>0){
          luci();
          delay(3);
        }
      }
      statotasti=9;
      servo_op();
      while(digitalRead(pbianco)==1){
        delay(10);
        luci();
      }
      delay(10);
    }
    if(digitalRead(pbianco)==1&&(statotasti==9||statotasti==10)){
      statotasti=10;
      if(luce>10){
        while(luce>0){
          luci();
          delay(3);
        }
      }
      statotasti=5;
      servo_cl();
      while(digitalRead(pbianco)==1){
        delay(10);
        luci();
      }
      delay(10);
    }
    if(luce>=250&&statotasti==7){
      scramble=10;
    }
  }
  if(statotasti!=1&&statotasti!=2){
    for(j=0;j<=100;j++){
      for(i=24;i<NLED;i++){
        leds[i]=CRGB(j,j,j);
      }
      FastLED.show();
      delay(8);
    }
    delay(500);
    stepper_RPM(vel);
    for(i=1; i<=mtt; i++){
        percentuale = map(i,0,mtt,0,6);
        for(j=0;j<=percentuale;j++){
          leds[j+0]=CRGB(0,33,33);
          leds[j+6]=CRGB(0,33,33);
          leds[j+12]=CRGB(0,33,33);
          leds[j+18]=CRGB(0,33,33);
        }
        FastLED.show();
      if(algoritmo[i-1]== 0){
        mtt = 251;
      }
      if(algoritmo[i-1]== 1){    //U
        stepper_LUN(step90);
        step_U();
      }
      if(algoritmo[i-1]== 2){    //U'
        stepper_LUN(-step90);
        step_U();
      }
      if(algoritmo[i-1]== 3){    //D
        stepper_LUN(step90);
        step_D();
      }
      if(algoritmo[i-1]== 4){    //D'
        stepper_LUN(-step90);
        step_D();
      }
      if(algoritmo[i-1]== 5){    //R
        stepper_LUN(step90);
        step_R();
      }
      if(algoritmo[i-1]== 6){    //R'
        stepper_LUN(-step90);
        step_R();
      }
      if(algoritmo[i-1]== 7){    //L
        stepper_LUN(step90);
        step_L();
      }
      if(algoritmo[i-1]== 8){    //L'
        stepper_LUN(-step90);
        step_L();
      }
      if(algoritmo[i-1]== 9){    //F
        stepper_LUN(step90);
        step_F();
      }
      if(algoritmo[i-1]==10){    //F'
        stepper_LUN(-step90);
        step_F();
      }
      if(algoritmo[i-1]==11){    //B
        stepper_LUN(step90);
        step_B();
      }
      if(algoritmo[i-1]==12){    //B'
        stepper_LUN(-step90);
        step_B();
      }
      if(algoritmo[i-1]==13){    //U2
        stepper_LUN(step180);
        step_U();
      }
      if(algoritmo[i-1]==14){    //D2
        stepper_LUN(step180);
        step_D();
      }
      if(algoritmo[i-1]==15){    //R2
        stepper_LUN(step180);
        step_R();
      }
      if(algoritmo[i-1]==16){    //L2
        stepper_LUN(step180);
        step_L();
      }
      if(algoritmo[i-1]==17){    //F2
        stepper_LUN(step180);
        step_F();
      }
      if(algoritmo[i-1]==18){    //B2
        stepper_LUN(step180);
        step_B();
      }
      mill=millis();
      while(millis()-mill<pausaM){
        if(digitalRead(prosso)==1){
          stop();
        }
      }
    }
    servo_op();
    y=i;
    mill=millis();
    while(millis()-mill<500){
      delay(5);
      if(digitalRead(prosso)==1){
        stop();
      }
      delay(5);
      if(digitalRead(prosso)==1){
        stop();
      }
      if(y==260){
        luci();
      }
    }
    if(y<=259){
      stepper_RPM(velCUS);
      stepper_LUN(stepCUS);
      step_CUS();
    }
    for(j=100;j>=0;j--){
      for(i=24;i<NLED;i++){
        leds[i]=CRGB(j,j,j);
      }
      for(i=0;i<=percentuale;i++){
        leds[i]=CRGB(0,j/3,j/3);
        leds[i+6]=CRGB(0,j/3,j/3);
        leds[i+12]=CRGB(0,j/3,j/3);
        leds[i+18]=CRGB(0,j/3,j/3);
      }
      FastLED.show();
      delay(8);
      if(y>=260){
        luci();
      }
    }
  }
  while(luce>10){
    delay(10);
    luci();
  }
  delay(10);
  scramble=0;
  statotasti=1;
  y=0;
}

void stop(){
  scramble=0;
  while(digitalRead(prosso)==1){
    delay(10);
    luci();
  }
  if(luce>10){
    while(luce>0){
      luci();
      delay(3);
    }
  }
  statotasti=5;
  while(scramble!=10){
    if(millis()-mill>10){
      luci();
      mill=millis();
    }
    if(digitalRead(prosso)==1&&(statotasti==5||statotasti==6||statotasti==9||statotasti==10)){
      if(statotasti<=6){
        statotasti=6;
      }else{
        statotasti=10;
      }
      if(luce>10){
        while(luce>0){
          luci();
          delay(3);
        }
      }
      statotasti=1;
      servo_op();
      scramble=10;
      i=260;
      while(digitalRead(prosso)==1){
        delay(10);
        luci();
      }
      delay(10);
    }
    if(digitalRead(pverde)==1&&(statotasti==5||statotasti==6)){
      statotasti=6;
      if(luce>10){
        while(luce>0){
          luci();
          delay(3);
        }
      }
      statotasti=7;
      scramble=10;
      while(digitalRead(pverde)==1||statotasti!=7||luce<250){
        delay(10);
        luci();
      }
      delay(10);
    }
    if(digitalRead(pbianco)==1&&(statotasti==5||statotasti==6)){
      statotasti=6;
      if(luce>10){
        while(luce>0){
          luci();
          delay(3);
        }
      }
      statotasti=9;
      servo_op();
      while(digitalRead(pbianco)==1){
        delay(10);
        luci();
      }
      delay(10);
    }
    if(digitalRead(pbianco)==1&&(statotasti==9||statotasti==10)){
      statotasti=10;
      if(luce>10){
        while(luce>0){
          luci();
          delay(3);
        }
      }
      statotasti=5;
      servo_cl();
      while(digitalRead(pbianco)==1){
        delay(10);
        luci();
      }
      delay(10);
    }
  }
}

void animazioneavvio(){
  for(j=0;j<6;j++){
    for(i=0;i<100;i++){
      leds[j+0 ]=CRGB(i,i,i);
      leds[j+6 ]=CRGB(i,i,i);
      leds[j+12]=CRGB(i,i,i);
      leds[j+18]=CRGB(i,i,i);
      FastLED.show();
    }
    delay(5);
  }
  for(i=0;i<100;i++){
    for(j=0;j<24;j++){
      leds[j]=CRGB(100,100+i,100+i);
    }
    FastLED.show();
    delay(8);
  }
  delay(50);
  for(i=100;i>=0;i--){
    for(j=0;j<24;j++){
      leds[j]=CRGB(100,100+i,100+i);
    }
    FastLED.show();
    delay(8);
  }
  delay(50);
  for(i=0;i<100;i++){
    for(j=0;j<24;j++){
      leds[j]=CRGB(100,100+i,100+i);
    }
    FastLED.show();
    delay(8);
  }
  delay(50);
  for(i=100;i>=0;i--){
    for(j=0;j<24;j++){
      leds[j]=CRGB(100,100+i,100+i);
    }
    FastLED.show();
    delay(8);
  }
  for(j=0;j<6;j++){
    for(i=100;i>=0;i--){
      leds[j+0 ]=CRGB(i,i,i);
      leds[j+6 ]=CRGB(i,i,i);
      leds[j+12]=CRGB(i,i,i);
      leds[j+18]=CRGB(i,i,i);
      FastLED.show();
    }
  }
  for(i=0;i<=255;i++){
    analogWrite(lbianco,i);
    delay(2);
  }
  for(i=0;i<=255;i++){
    analogWrite(lrosso,i);
    delay(2);
  }
  for(i=0;i<=255;i++){
    analogWrite(lverde,i);
    delay(2);
  }
  for(i=255;i>=0;i--){
    analogWrite(lbianco,i);
    delay(2);
  }
  for(i=255;i>=0;i--){
    analogWrite(lrosso,i);
    delay(2);
  }
  for(i=255;i>=0;i--){
    analogWrite(lverde,i);
    delay(2);
  }
  for(lum=0;lum<=100;lum=lum+5){
    for(i=0;i<10;i++){
      delay(10);
      luci();
    }
    refresh();
  }
}

void luci(){
  if(statotasti==1){
    luce=luce+4;
    if(luce>=255){
      luce=255;
      statotasti=2;
    }
    analogWrite(lbianco,luce);
    analogWrite(lverde,0);
    analogWrite(lrosso,0);
  }
  if(statotasti==2){
    luce=luce-4;
    if(luce<=0){
      luce=0;
      statotasti=1;
    }
    analogWrite(lbianco,luce);
    analogWrite(lverde,0);
    analogWrite(lrosso,0);
  }
  if(statotasti==3){
    luce=luce+7;
    if(luce>=255){
      luce=255;
      statotasti=4;
    }
    analogWrite(lbianco,0);
    analogWrite(lverde,luce);
    analogWrite(lrosso,0);
  }
  if(statotasti==4){
    luce=luce-7;
    if(luce<=0){
      luce=0;
      statotasti=3;
    }
    analogWrite(lbianco,0);
    analogWrite(lverde,luce);
    analogWrite(lrosso,0);
  }
  if(statotasti==5){
    luce=luce+7;
    if(luce>=255){
      luce=255;
      statotasti=6;
    }
    analogWrite(lbianco,luce);
    analogWrite(lverde,luce);
    analogWrite(lrosso,luce);
  }
  if(statotasti==6){
    luce=luce-7;
    if(luce<=0){
      luce=0;
      statotasti=5;
    }
    analogWrite(lbianco,luce);
    analogWrite(lverde,luce);
    analogWrite(lrosso,luce);
  }
  if(statotasti==7){
    luce=luce+4;
    if(luce>=255){
      luce=255;
      statotasti=8;
    }
    analogWrite(lbianco,0);
    analogWrite(lverde,0);
    analogWrite(lrosso,luce);
  }
  if(statotasti==8){
    luce=luce-4;
    if(luce<=0){
      luce=0;
      statotasti=7;
    }
    analogWrite(lbianco,0);
    analogWrite(lverde,0);
    analogWrite(lrosso,luce);
  }
  if(statotasti==9){
    luce=luce+7;
    if(luce>=255){
      luce=255;
      statotasti=10;
    }
    analogWrite(lbianco,luce);
    analogWrite(lverde,0);
    analogWrite(lrosso,luce);
  }
  if(statotasti==10){
    luce=luce-7;
    if(luce<=0){
      luce=0;
      statotasti=9;
    }
    analogWrite(lbianco,luce);
    analogWrite(lverde,0);
    analogWrite(lrosso,luce);
  }
}

void refresh(){
  color++;
  if(color>=30){
    color=0;
  }
  for(i=0;i<=3;i++){
    if(color==0){  //ciano
      leds[(i*6)+0 ]=CRGB(0*lum,1*lum,1*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==1){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,1*lum,1*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==2){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,1*lum,1*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==3){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,1*lum,1*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==4){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,1*lum,1*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==5){  //blu
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,2*lum);
    }
    if(color==6){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,2*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==7){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,2*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==8){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,2*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==9){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,2*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==10){  //viola
      leds[(i*6)+0 ]=CRGB(1*lum,0*lum,1*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==11){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(1*lum,0*lum,1*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==12){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(1*lum,0*lum,1*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==13){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(1*lum,0*lum,1*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==14){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(1*lum,0*lum,1*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==15){  //rosso
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(2*lum,0*lum,0*lum);
    }
    if(color==16){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(2*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==17){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(2*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==18){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(2*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==19){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(2*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==20){  //giallo
      leds[(i*6)+0 ]=CRGB(1*lum,1*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==21){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(1*lum,1*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==22){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(1*lum,1*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==23){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(1*lum,1*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==24){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(1*lum,1*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==25){  //verde
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,2*lum,0*lum);
    }
    if(color==26){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,2*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==27){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,2*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==28){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,2*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
    if(color==29){
      leds[(i*6)+0 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+1 ]=CRGB(0*lum,2*lum,0*lum);
      leds[(i*6)+2 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+3 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+4 ]=CRGB(0*lum,0*lum,0*lum);
      leds[(i*6)+5 ]=CRGB(0*lum,0*lum,0*lum);
    }
  }
  FastLED.show();
  mill=millis();
}

void internet() {
  WiFiClient client = server.available();            //controlla per eventuali client
  if (client) {                                 //se si collega un nuovo client
    String lineacorrente = "";                       //stringa per i dati che arrivano dal client
    tbuf=millis();
    while (client.connected() && timeout <= 2000) {  //loop che aspetta il client
      timeout = timeout + 1;
      delay(1);
      if(millis()-tbuf>10){
        luci();
        tbuf=millis();
      }
      if (client.available()) {  //se il client scrive qualcosa
        char c = client.read();  //salva il carattere
        header += c;
        if(luce>10){
          while(luce>0){
            luci();
            delay(3);
            if(millis()-mill>100&&lum>0){
              refresh();
            }
          }
        }
        statotasti=0;
        if(lum>0){
          for(lum=100;lum>=0;lum=lum-5){
            delay(100);
            refresh();
          }
          lum=0;
        }
        if (c == '\n') {                              //se il carrattere è un invio possiamo inviargli la paginaweb
          if (lineacorrente.length() == 0) {          //se la linea corrente è vuota, inviamo la pagina
            client.println("HTTP/1.1 200 OK\nContent-type:text/html\nConnection: close\n");
            if (header.indexOf("GET /reset") >= 0) {  //controllo se è stato premuto qualcosa
              Serial.println("RESET");
              scramble = 0;
              colore = 1;
              messaggio = 0;
              for (i = 0; i <= 8; i++) {
                fW[i] = 0;
                fY[i] = 0;
                fG[i] = 0;
                fB[i] = 0;
                fR[i] = 0;
                fO[i] = 0;
              }
              fW[4] = 1;
              fY[4] = 2;
              fG[4] = 3;
              fB[4] = 4;
              fR[4] = 5;
              fO[4] = 6;
            }
            if (header.indexOf("GET /risoluzione") >= 0) {
              Serial.println("START");
              scramble = 0;
              for(i=1;i<=250;i++){
                algoritmo[i-1] = 0;
              }
              colore = 1;
              af_W(fW[0],fW[1],fW[2],fW[3],fW[5],fW[6],fW[7],fW[8]);
              af_Y(fY[0],fY[1],fY[2],fY[3],fY[5],fY[6],fY[7],fY[8]);
              af_G(fG[0],fG[1],fG[2],fG[3],fG[5],fG[6],fG[7],fG[8]);
              af_B(fB[0],fB[1],fB[2],fB[3],fB[5],fB[6],fB[7],fB[8]);
              af_R(fR[0],fR[1],fR[2],fR[3],fR[5],fR[6],fR[7],fR[8]);
              af_O(fO[0],fO[1],fO[2],fO[3],fO[5],fO[6],fO[7],fO[8]);
              start();
              mtt = mosse();
              tgs = tempo();
              err = errori();
              if(err > 0){
                messaggio = 2;
                scramble = 0;
              }else{
                messaggio = 1;
                scramble = 1;
                statotasti = 3;
                for(i=1;i<=mtt;i++){
                  algoritmo[i-1]=mossa(i);
                }
                for(i=1;i<=mtt;i++){
                  Serial.print(algoritmo[i-1]);
                  Serial.print(" ");
                }
                Serial.print("\n");
              }
            }
            if (header.indexOf("GET /bianco") >= 0) {
              Serial.println("BIANCO SELEZIONATO");
              colore = 1;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /giallo") >= 0) {
              Serial.println("GIALLO SELEZIONATO");
              colore = 2;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /verde") >= 0) {
              Serial.println("VERDE SELEZIONATO");
              colore = 3;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /blu") >= 0) {
              Serial.println("BLU SELEZIONATO");
              colore = 4;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /rosso") >= 0) {
              Serial.println("ROSSO SELEZIONATO");
              colore = 5;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /arancione") >= 0) {
              Serial.println("ARANCIONE SELEZIONATO");
              colore = 6;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciabianca/1") >= 0) {
              fW[0] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciabianca/2") >= 0) {
              fW[1] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciabianca/3") >= 0) {
              fW[2] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciabianca/4") >= 0) {
              fW[3] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciabianca/6") >= 0) {
              fW[5] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciabianca/7") >= 0) {
              fW[6] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciabianca/8") >= 0) {
              fW[7] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciabianca/9") >= 0) {
              fW[8] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciagialla/1") >= 0) {
              fY[0] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciagialla/2") >= 0) {
              fY[1] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciagialla/3") >= 0) {
              fY[2] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciagialla/4") >= 0) {
              fY[3] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciagialla/6") >= 0) {
              fY[5] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciagialla/7") >= 0) {
              fY[6] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciagialla/8") >= 0) {
              fY[7] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciagialla/9") >= 0) {
              fY[8] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaverde/1") >= 0) {
              fG[0] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaverde/2") >= 0) {
              fG[1] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaverde/3") >= 0) {
              fG[2] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaverde/4") >= 0) {
              fG[3] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaverde/6") >= 0) {
              fG[5] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaverde/7") >= 0) {
              fG[6] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaverde/8") >= 0) {
              fG[7] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaverde/9") >= 0) {
              fG[8] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciablu/1") >= 0) {
              fB[0] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciablu/2") >= 0) {
              fB[1] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciablu/3") >= 0) {
              fB[2] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciablu/4") >= 0) {
              fB[3] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciablu/6") >= 0) {
              fB[5] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciablu/7") >= 0) {
              fB[6] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciablu/8") >= 0) {
              fB[7] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciablu/9") >= 0) {
              fB[8] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciarossa/1") >= 0) {
              fR[0] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciarossa/2") >= 0) {
              fR[1] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciarossa/3") >= 0) {
              fR[2] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciarossa/4") >= 0) {
              fR[3] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciarossa/6") >= 0) {
              fR[5] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciarossa/7") >= 0) {
              fR[6] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciarossa/8") >= 0) {
              fR[7] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciarossa/9") >= 0) {
              fR[8] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaarancione/1") >= 0) {
              fO[0] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaarancione/2") >= 0) {
              fO[1] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaarancione/3") >= 0) {
              fO[2] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaarancione/4") >= 0) {
              fO[3] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaarancione/6") >= 0) {
              fO[5] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaarancione/7") >= 0) {
              fO[6] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaarancione/8") >= 0) {
              fO[7] = colore;
              scramble = 0;
              messaggio = 0;
            }
            if (header.indexOf("GET /facciaarancione/9") >= 0) {
              fO[8] = colore;
              scramble = 0;
              messaggio = 0;
            }
            client.print("<!DOCTYPE html><html><head><title>Rubo di Cubik</title><style>");  //inviamo la pagina web
            client.print("body     {background-color:#9EFCFC;}");
            client.print("hr       {background-color:black;height:2px;justify-content: center;display:flex;}");
            client.print("h1       {font-family:'roboto',sans-serif;color:black;font-size:40px;height:25px;text-align:center;display:flex;justify-content: center;}");
            client.print("h2       {font-family:'roboto',sans-serif;color:black;font-size:20px;height:15px;text-align:center;display:flex;justify-content: center;}");
            client.print("h3       {font-family:'roboto',sans-serif;color:#FF5050;font-size:10px;height:15px;text-align:center;display:flex;justify-content: center;}");
            client.print(".button0 {border-radius:8px;border:none;color:black;padding:30px 30px;background-color:grey;}");
            client.print(".button1 {border-radius:8px;border:none;color:black;padding:30px 30px;background-color:white;}");
            client.print(".button2 {border-radius:8px;border:none;color:black;padding:30px 30px;background-color:yellow;}");
            client.print(".button3 {border-radius:8px;border:none;color:black;padding:30px 30px;background-color:green;}");
            client.print(".button4 {border-radius:8px;border:none;color:black;padding:30px 30px;background-color:blue;}");
            client.print(".button5 {border-radius:8px;border:none;color:black;padding:30px 30px;background-color:red;}");
            client.print(".button6 {border-radius:8px;border:none;color:black;padding:30px 30px;background-color:orange;}");
            client.print(".button7 {border-radius:8px;border:none;color:black;padding:0px 25px; background-color:black;}");
            client.print(".button8 {border:none;color:black;padding:30px 30px;background-color:#9EFCFC;}");
            client.print(".button9 {border:none;color:black;padding:1px 25px;background-color:#9EFCFC;}");
            client.print(".button10{border-radius:8px;border:none;color:black;padding:6px 10px;background-color:lightgrey;}");
            client.print(".button11{border:none;color:black;padding:2px 153px;font-size:0px;background-color:#9EFCFC;}");
            client.print("spessore {width:0px;height:2px;background-color:red;display:inline-block;margin:3px;}");
            client.print("spessore2{width:0px;height:2px;background-color:red;display:inline-block;margin:8px;}");
            client.print("spessore1{width:45px;height:5px;background-color:#9EFCFC;}");
            client.print("p        {color: red;text-align:center;height:50px;display:flex;justify-content: center;}");
            client.print("p1       {color: red;text-align:center;height:5px;display:flex;justify-content: center;}");
            client.print("</style></head><body><h1>Risolutore di Cubo di Rubik</h1><hr><h2>Messaggio dalla macchina:</h2><h3>");
            if (messaggio == 0) {
              client.print("Nessun errore, macchina pronta all uso");
            } else if (messaggio == 1) {
              client.print("Scramble generato con successo (tempo impiegato: ");
              client.print(tgs);
              client.print(" ms, mosse totali: ");
              client.print(mtt);
              client.print(")");
            } else if (messaggio == 2) {
              client.print("Generazione scramble fallita, errore: ");
              client.print(err);
              client.print(" (per ritornare indietro premere reset)");
            }
            client.print("</h3><hr><h2>Comandi</h2><p><a href='http://");
            client.print(WiFi.localIP());
            client.print("/bianco'><button class='button1'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/giallo'><button class='button2'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/verde'><button class='button3'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/blu'><button class='button4'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/rosso'><button class='button5'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/arancione'><button class='button6'></button></a><spessore></spessore><button class='button8'></button><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/reset'><button class='button10'><h2>RESET</h2></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/risoluzione'><button class='button10'><h2>RISOLUZIONE</h2></button></a></p><p1><button class='button");
            if (colore == 1) {
              client.print("7");
            } else {
              client.print("9");
            }
            client.print("'></button><spessore2></spessore2><button class='button");
            if (colore == 2) {
              client.print("7");
            } else {
              client.print("9");
            }
            client.print("'></button><spessore2></spessore2><button class='button");
            if (colore == 3) {
              client.print("7");
            } else {
              client.print("9");
            }
            client.print("'></button><spessore2></spessore2><button class='button");
            if (colore == 4) {
              client.print("7");
            } else {
              client.print("9");
            }
            client.print("'></button><spessore2></spessore2><button class='button");
            if (colore == 5) {
              client.print("7");
            } else {
              client.print("9");
            }
            client.print("'></button><spessore2></spessore2><button class='button");
            if (colore == 6) {
              client.print("7");
            } else {
              client.print("9");
            }
            client.print("'></button><spessore2></spessore2><button class='button11'></button></p1><hr><h2>Cubo da risolvere</h2><p><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciabianca/1'><button class='button");
            client.print(fW[0]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciabianca/2'><button class='button");
            client.print(fW[1]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciabianca/3'><button class='button");
            client.print(fW[2]);
            client.print("'></button></a><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'>");
            client.print("</button><spessore></spessore><button class='button8'></button></p><spessore1></spessore1><p><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciabianca/4'><button class='button");
            client.print(fW[3]);
            client.print("'></button></a><spessore></spessore><button class='button1'></button><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciabianca/6'><button class='button");
            client.print(fW[5]);
            client.print("'></button></a><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore>");
            client.print("<button class='button8'></button><spessore></spessore><button class='button8'></button></p><spessore1></spessore1><p><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciabianca/7'><button class='button");
            client.print(fW[6]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciabianca/8'><button class='button");
            client.print(fW[7]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciabianca/9'><button class='button");
            client.print(fW[8]);
            client.print("'></button></a><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button></p><spessore1></spessore1><p><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaarancione/1'><button class='button");
            client.print(fO[0]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaarancione/2'><button class='button");
            client.print(fO[1]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaarancione/3'><button class='button");
            client.print(fO[2]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaverde/1'><button class='button");
            client.print(fG[0]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaverde/2'><button class='button");
            client.print(fG[1]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaverde/3'><button class='button");
            client.print(fG[2]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciarossa/1'><button class='button");
            client.print(fR[0]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciarossa/2'><button class='button");
            client.print(fR[1]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciarossa/3'><button class='button");
            client.print(fR[2]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciablu/1'><button class='button");
            client.print(fB[0]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciablu/2'><button class='button");
            client.print(fB[1]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciablu/3'><button class='button");
            client.print(fB[2]);
            client.print("'></button></a></p><spessore1></spessore1><p><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaarancione/4'><button class='button");
            client.print(fO[3]);
            client.print("'></button></a><spessore></spessore><button class='button6'></button><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaarancione/6'><button class='button");
            client.print(fO[5]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaverde/4'><button class='button");
            client.print(fG[3]);
            client.print("'></button></a><spessore></spessore><button class='button3'></button><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaverde/6'><button class='button");
            client.print(fG[5]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciarossa/4'><button class='button");
            client.print(fR[3]);
            client.print("'></button></a><spessore></spessore><button class='button5'></button><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciarossa/6'><button class='button");
            client.print(fR[5]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciablu/4'><button class='button");
            client.print(fB[3]);
            client.print("'></button></a><spessore></spessore><button class='button4'></button><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciablu/6'><button class='button");
            client.print(fB[5]);
            client.print("'></button></a></p><spessore1></spessore1><p><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaarancione/7'><button class='button");
            client.print(fO[6]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaarancione/8'><button class='button");
            client.print(fO[7]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaarancione/9'><button class='button");
            client.print(fO[8]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaverde/7'><button class='button");
            client.print(fG[6]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaverde/8'><button class='button");
            client.print(fG[7]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciaverde/9'><button class='button");
            client.print(fG[8]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciarossa/7'><button class='button");
            client.print(fR[6]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciarossa/8'><button class='button");
            client.print(fR[7]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciarossa/9'><button class='button");
            client.print(fR[8]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciablu/7'><button class='button");
            client.print(fB[6]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciablu/8'><button class='button");
            client.print(fB[7]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciablu/9'><button class='button");
            client.print(fB[8]);
            client.print("'></button></a></p><spessore1></spessore1><p><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciagialla/1'><button class='button");
            client.print(fY[0]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciagialla/2'><button class='button");
            client.print(fY[1]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciagialla/3'><button class='button");
            client.print(fY[2]);
            client.print("'></button></a><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button>");
            client.print("<spessore></spessore><button class='button8'></button></p><spessore1></spessore1><p><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciagialla/4'><button class='button");
            client.print(fY[3]);
            client.print("'></button></a><spessore></spessore><button class='button2'></button><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciagialla/6'><button class='button");
            client.print(fY[5]);
            client.print("'></button></a><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button>");
            client.print("<spessore></spessore><button class='button8'></button></p><spessore1></spessore1><p><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciagialla/7'><button class='button");
            client.print(fY[6]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciagialla/8'><button class='button");
            client.print(fY[7]);
            client.print("'></button></a><spessore></spessore><a href='http://");
            client.print(WiFi.localIP());
            client.print("/facciagialla/9'><button class='button");
            client.print(fY[8]);
            client.print("'></button></a><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button><spessore></spessore><button class='button8'></button></p></body></html>");
            client.println();  //infine gli facciamo capire che è terminata la pagina
            break;
          } else {  //se arriva un invio svuota la stringa della riga
            lineacorrente = "";
          }
        } else if (c != '\r') {  //se abbiamo un altro carattere che non è "/r"
          lineacorrente += c;    //lo aggiungiamo alla stringa della riga
        }
      }
    }
    if(scramble!=1){
      tempointernet=millis();
    }else{
      tempointernet=0;
    }
    timeout = 0;
    header = "";
    client.stop();  //diconnettiamoci dal client
  }
}

void seriale(){
  if(Serial.available()){
    i=0;
    while(i <= 47){
      if(Serial.available()){
        stringa[i] = Serial.read()-47;
        Serial.print(stringa[i]);
        i++;
      }
    }
    i=0;
    Serial.println("\nSTART");
    scramble = 0;
    for(i=1;i<=250;i++){
    algoritmo[i-1] = 0;
    }
    colore = 1;
    af_W(stringa[0   ],stringa[1   ],stringa[2   ],stringa[3   ],stringa[4   ],stringa[5   ],stringa[6   ],stringa[7   ]);
    af_Y(stringa[0+8 ],stringa[1+8 ],stringa[2+8 ],stringa[3+8 ],stringa[4+8 ],stringa[5+8 ],stringa[6+8 ],stringa[7+8 ]);
    af_G(stringa[0+16],stringa[1+16],stringa[2+16],stringa[3+16],stringa[4+16],stringa[5+16],stringa[6+16],stringa[7+16]);
    af_B(stringa[0+24],stringa[1+24],stringa[2+24],stringa[3+24],stringa[4+24],stringa[5+24],stringa[6+24],stringa[7+24]);
    af_R(stringa[0+32],stringa[1+32],stringa[2+32],stringa[3+32],stringa[4+32],stringa[5+32],stringa[6+32],stringa[7+32]);
    af_O(stringa[0+40],stringa[1+40],stringa[2+40],stringa[3+40],stringa[4+40],stringa[5+40],stringa[6+40],stringa[7+40]);
    start();
    mtt = mosse();
    tgs = tempo();
    err = errori();
    Serial.print("errore: ");
    Serial.println(err);
    Serial.print("tempo: ");
    Serial.println(tgs);
    Serial.print("mosse: ");
    Serial.println(mtt);
    if(err > 0){
      messaggio = 2;
      scramble = 0;
    }else{
      messaggio = 1;
      scramble = 1;
      statotasti = 3;
      for(i=1;i<=mtt;i++){
        algoritmo[i-1]=mossa(i);
      }
      for(i=1;i<=mtt;i++){
        Serial.print(algoritmo[i-1]);
        Serial.print(" ");
      }
    Serial.print("\n");
    }
  }
}