#include <Arduino.h>
#include <Arduino_LSM9DS1.h>

float x, y, z;
int degreesX = 0;
int degreesY = 0;
int degreesZ = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println("Hz");
}

void loop() {

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

  }

  x = 100 * x;
  y = 100 * y;
  z = 100 * z;
  degreesX = map(x, -100, 97, -90, 90);
  degreesY = map(y, -100, 97, -90, 90);
  degreesZ = map(z, -100, 97, -90, 90);
  Serial.print(degreesX);
  Serial.print("\t");
  Serial.print(degreesY);
  Serial.print("\t");
  Serial.print(degreesZ);
  Serial.print("\n");
  
  delay(100);
}
