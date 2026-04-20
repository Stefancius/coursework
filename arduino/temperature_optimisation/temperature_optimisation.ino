#include <math.h>
#define TEMP_SENSOR A0

struct dataPoint {
  //arrays to store temp and time data
  float time;
  float temp;
};

enum powerMode {
  ACTIVE,
  IDLE,
  POWER_DOWN
};

powerMode currentMode = ACTIVE;


const int MAX_SAMPLES = 50;

float frequency[MAX_SAMPLES];
float magnitude[MAX_SAMPLES];

int sample_delay = 1000;

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
  for ( int i=0; i<MAX_SAMPLES; i++){
    float re = 0;
    float im = 0;

    for (int j = 0; j<MAX_SAMPLES; j++){
      // angle of frequncy 
      float phi = 2 * 3.1415 * i * j / MAX_SAMPLES;

      re += data[j].temp*cos(phi);
      im -= data[j].temp*sin(phi);
    }  
  //magnitude of frequency 
  magnitude[i] = sqrt(re*re + im*im);

  float sample_rate = 1.0;
  frequency[i] = (i * sample_rate) / MAX_SAMPLES; // frequency in HZ
  }  
}



powerMode decide_mode(){
  if (index < 2){
    return POWER_DOWN;
  
  }

  float temp_difference = data[index-1].temp - data[index-2].temp;

  float time_difference = data[index-1].time - data[index-2].time;

  if(time_difference<=0){
    return POWER_DOWN;
  }

  float rate_of_change = fabs(temp_difference/time_difference);

  if(rate_of_change>1){
    return ACTIVE;
  } else if(rate_of_change >0.1){
    return IDLE;
  } else {
    return POWER_DOWN;
  }

} 


void send_data_to_pc() {
  if (index < MAX_SAMPLES){// read values up to 50 samples 
    collect_temperature_data();
    delay(sample_delay); // 
  }

  //run dft
  if (index == MAX_SAMPLES){
    apply_dft();
  
    currentMode = decide_mode();

    Serial.print("Mode:  ");
    if(currentMode == ACTIVE){
      sample_delay = 1000;
      Serial.println("ACTIVE");
    } else if(currentMode == IDLE) {
      sample_delay = 5000;
      Serial.println("IDLE");
    } else {
      sample_delay = 30000;
      Serial.println("POWER_DOWN");
    }
 
    while(1); //run once 
  }
}

 
void loop() {
  send_data_to_pc();
}

  








