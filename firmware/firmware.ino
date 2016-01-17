int value[6];
int raw_value[6];
bool invert_sign[6];
bool invert_couple[3];

#define LEDPIN 13
#define RESOLUTIONINT 12
#define RESOLUTION 4096
#define HALFRESOLUTION 2048

void setup() {
  Serial.begin(9600);
  Serial.println("Ready");
  pinMode(LEDPIN, OUTPUT);
  digitalWrite(LEDPIN, HIGH);
  analogReadResolution(RESOLUTIONINT);
  //dirty calibration
  invert_sign[0] = true;
  invert_sign[1] = true;
  invert_sign[2] = false;
  invert_sign[3] = true;
  invert_sign[4] = false;
  invert_sign[5] = false;

  invert_couple[0] = false;
  invert_couple[1] = true;
  invert_couple[2] = false;
}

//read the values and store them in value[]
void read_values() {
  //read the values
  for(int i(0); i<6; ++i)
  {
    raw_value[i] = analogRead(A0 + i);
  }

  //transform the values
  for(int i(0); i<6; ++i)
  {
    if(invert_sign[i])
      value[i] = -raw_value[i] + HALFRESOLUTION;
    else
      value[i] = raw_value[i] - HALFRESOLUTION;
  }

  for(int i(0); i<3; ++i)
  {
    if(invert_couple[i])
    {
      int tmp = value[2*i];
      value[2*i] = value[2*i + 1];
      value[2*i + 1] = tmp;
    }
  }
}

void print_values()
{
  // print out the value you read:
  for(int i(0); i<6; ++i)
  {
    Serial.print(value[i]);
    Serial.print(' ');
  }
  Serial.print('\n');
}

void loop() {

  if(Serial.available())
  {
    char inByte = Serial.read();
    if(inByte == 'v')
    {
      //version mode
      Serial.print("0.1\n");
    }
    else if(inByte == 'g')
    {
      //get mode
      read_values();
      print_values();
    }
    else if(inByte == 'd')
    {
      //debug mode
      while(1)
      {
        read_values();
        print_values();
        delay(100);
      }
    }
  }
  delay(10);        // delay in between reads for stability
}
