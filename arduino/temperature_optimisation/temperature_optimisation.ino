#include <math.h>
#define TEMP_SENSOR A0

struct dataPoint {
  //arrays to store temp and time data
  float time;
  float temp;
};

enum PowerMode {
  ACTIVE,
  IDLE,
  POWER_DOWN
};

PowerMode currentMode = ACTIVE;

const int MAX_SAMPLES = 50;

float frequency[MAX_SAMPLES];
float magnitude[MAX_SAMPLES];


dataPoint data[MAX_SAMPLES];

int index = 0;

const int B = 4275000;
const int R0 = 100000;


void setup() {
  Serial.begin(9600);
}

void collect_temperature_data(){
  int sensorValue = analogRead(TEMP_SENSOR);

  if (sensorValue <= 0) {
    Serial.println("Sensor read error");
    return;
  }

  float R = 1023.0 / sensorValue - 1.0;
  R = R0*R;

  float degreesC = 1.0/(log(R/R0) / B + 1.0 / 298.15)- 273.15;
  
  float timeNow = millis()/1000.0; // time in secs 

  data[index].temp = degreesC;
  data[index].time = timeNow;

  Serial.print("  Time: ");
  Serial.print(timeNow);
  Serial.print("    Temp: ");
  Serial.println(degreesC);

  index++; 
}


void apply_dft() { //convert temp to frequency data
  for ( int k=0; k<MAX_SAMPLES; k++){
    float re = 0;
    float im = 0;

    for (int n = 0; n<MAX_SAMPLES; n++){
      // angle of frequncy 
      float phi = 2 * 3.1415 * k * n / MAX_SAMPLES;

      re += data[n].temp*cos(phi);
      im -= data[n].temp*sin(phi);
    }  
  //magnitude of frequency 
  magnitude[k] = sqrt(re*re + im*im);

  float Fs = 1.0; // sampling rate
  frequency[k] = (k * Fs) / MAX_SAMPLES; // frequency in HZ
  }  
}


void send_data_to_pc() {
  if (index < MAX_SAMPLES){// read values up to 50 samples 
    collect_temperature_data();
    delay(1000); // 1sec delay between readings 
  }

  //run dft
  if (index == MAX_SAMPLES){
    apply_dft();
  
    currentMode = decide_power_mode();

    Serial.print("Mode:  ");
    if(currentMode == ACTIVE){
      Serial.println("ACTIVE");
    } else if(currentMode == IDLE) {
      Serial.println("IDLE");
    } else {
      Serial.println("POWER_DOWN");
    }
 
    while(1); //run once 
  }
}


PowerMode decide_power_mode() {
  int max_value = 1; 

  for (int i = 2; i<MAX_SAMPLES; i++){
    if(magnitude[i]>magnitude[max_value]){
      max_value = i;
    }
  }

  
  float max_frequency = frequency[max_value];

  if(max_frequency>0.5){
    return ACTIVE;
  } else if (max_frequency > 0.1){
    return IDLE;
  } else{
    return POWER_DOWN;
  }
}
 
void loop() {
  send_data_to_pc();
}

  







