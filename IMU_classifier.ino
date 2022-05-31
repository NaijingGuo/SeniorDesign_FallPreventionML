/*
  IMU Classifier
  This example uses the on-board IMU to start reading acceleration and gyroscope
  data from on-board IMU, once enough samples are read, it then uses a
  TensorFlow Lite (Micro) model to try to classify the movement as a known gesture.
  Note: The direct use of C/C++ pointers, namespaces, and dynamic memory is generally
        discouraged in Arduino examples, and in the future the TensorFlowLite library
        might change to make the sketch simpler.
  The circuit:
  - Arduino Nano 33 BLE or Arduino Nano 33 BLE Sense board.
  Created by Don Coleman, Sandeep Mistry
  Modified by Dominic Pajak, Sandeep Mistry
  This example code is in the public domain.
*/

// import necessary libraries
#include <Arduino.h>
#include <Arduino_LSM9DS1.h>
#include <TensorFlowLite.h>
#include <tensorflow/lite/micro/all_ops_resolver.h>
#include <tensorflow/lite/micro/micro_error_reporter.h>
#include <tensorflow/lite/micro/micro_interpreter.h>
#include <tensorflow/lite/schema/schema_generated.h>
#include <tensorflow/lite/version.h>
#include "model.h"

// initialize variables
const int numSamples = 10;
float x, y, z, fall_risk;
int degreesX = 0;
int degreesY = 0;
int degreesZ = 0;
unsigned long time_elapsed;

int samplesRead = 0;
int alertCount = 0;

// global variables used for TensorFlow Lite (Micro)
tflite::MicroErrorReporter tflErrorReporter;
tflite::AllOpsResolver tflOpsResolver;

const tflite::Model* tflModel = nullptr;
tflite::MicroInterpreter* tflInterpreter = nullptr;
TfLiteTensor* tflInputTensor = nullptr;
TfLiteTensor* tflOutputTensor = nullptr;

// Create a static memory buffer for TFLM
constexpr int tensorArenaSize = 8 * 1024;
byte tensorArena[tensorArenaSize] __attribute__((aligned(16)));

// array to map gesture index to a name
const char* GESTURES[] = {
  "fall risk"
};

int NUM_GESTURES = 1;

// set up Serial Monitor

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // initialize the IMU
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // print out the samples rates of the IMUs
  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println();

  // get the TFL representation of the model byte array
  tflModel = tflite::GetModel(model);
  if (tflModel->version() != TFLITE_SCHEMA_VERSION) {
    Serial.println("Model schema mismatch!");
    while (1);
  }
  Serial.println("Model loaded.");

  // Create an interpreter to run the model
  tflInterpreter = new tflite::MicroInterpreter(tflModel, tflOpsResolver, tensorArena, tensorArenaSize, &tflErrorReporter);

  Serial.println("Interpreter created.");

  // Allocate memory for the model's input and output tensors
  tflInterpreter->AllocateTensors();

  Serial.println("Memory allocated.");

  // Get pointers for the model's input and output tensors
  tflInputTensor = tflInterpreter->input(0);
  tflOutputTensor = tflInterpreter->output(0);
}

int flip = 1;

void loop() {

  if (IMU.accelerationAvailable()) {

    // check if new acceleration data is available
    if (IMU.accelerationAvailable()) {
      // read the acceleration data
      IMU.readAcceleration(x, y, z);
    }
    x = 100 * x;
    y = 100 * y;
    z = 100 * z;

    // convert acceleration to degrees tilt
    degreesX = map(x, -100, 97, -90, 90);
    degreesY = map(y, -100, 97, -90, 90);
    degreesZ = map(z, -100, 97, -90, 90);
    if(flip == 1){
          // monitor output
    Serial.print(millis() / 1000.00);
    Serial.print(";");
    Serial.print(degreesX);
    Serial.print(";");
    Serial.print(degreesY);
    Serial.print(";");
    Serial.print(degreesZ);
    Serial.print("\n");
    }
    flip = flip *-1;

    // enforcing a 10 Hz sampling rate
    delay(100);

    // add IMU tilt data and store in the model's input tensor
    tflInputTensor->data.f[samplesRead * 3 + 0] = degreesX;
    tflInputTensor->data.f[samplesRead * 3 + 1] = degreesY;
    tflInputTensor->data.f[samplesRead * 3 + 2] = degreesZ;

    samplesRead++;
    //Serial.print("Samples read: ");
    //Serial.print(samplesRead);
    //Serial.print("\n");

//  Make an inference every 2 seconds
    if (samplesRead == numSamples*2) {
      samplesRead = 0;
      // Run inferencing
      TfLiteStatus invokeStatus = tflInterpreter->Invoke();
      if (invokeStatus != kTfLiteOk) {
        Serial.println("Invoke failed!");
        while (1);
        return;
      }
      
// NOTES:
//  - need to make a global variable for a tensor to update
//  - pull data from the last two seconds with some overlap compared to previous
//  - ensure to make count = 0 after every inference (could be every 1 second)
        alertCount = alertCount + 1;  
        Serial.print("\n");
        Serial.print(GESTURES[0]);
        Serial.print(": ");
        Serial.println(tflOutputTensor->data.f[0], 3);
        Serial.print("Alert count = ");
        Serial.print(alertCount);
        Serial.print("\n");
      }
    }
  }
}
