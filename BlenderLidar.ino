/*
 * Serial protocol is Header 0xFA, reserved, reserved ,ascention, declination, range, checksum
 * angles are calculated as (real_angle & 0xA0 ) >> 4 
 * range is low,high in mm 
 * reserved is for future use. set as 0xA5 0x5A for now
 */
#include <Servo.h>
#include <Math.h>


/*Vertical servo*/
#define ASC_PIN 10 //Ascention Servo pin, vertical angle
#define ASC_MAX 90
#define ASC_MIN 0
int ascDecVale = -1; used to reverse servo
int posAsc = 0;
Servo asc;

#define LIDAR_RX
#define LIDAR_TX

void setup()
{
  Serial.begin(115200);

  asc.attach(ASC_PIN); //setup asc servo
  posAsc = ASC_MAX;
  asc.write(posASC);
  
  
}

void loop()
{
  //If Serial from HOST -> Decode -> start? -> stop?
}
