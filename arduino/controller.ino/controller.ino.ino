typedef uint8_t Button;

const Button X_BUTTON = 9;
const Button A_BUTTON = 8;
const Button Y_BUTTON = 7;
const Button B_BUTTON = 6;

const Button RIGHT = 5;
const Button DOWN = 4;
const Button UP = 3;
const Button LEFT = 2; //Can you tell I got the pins backwards the first time?

const Button NONE = 10;

enum ButtonState {PRESSED = 0, RELEASED = 1, ERROR = 2};

char INPUT_BUFFER[2];
char OUTPUT_MESSAGE[128];

ButtonState getButtonState(char character){
  if(character == '-'){
    return RELEASED;
  } else if(character == '+') {
    return PRESSED;
  } else {
    return ERROR;
  }
}

Button getButton(char character){
  //Probably should update to iterate over elements rather than be a swith.
  switch(character){
    case 'A':
      return A_BUTTON;
    case 'B':
      return B_BUTTON;
    case 'X':
      return X_BUTTON;
    case 'Y':
      return Y_BUTTON;

    case 'L':
      return LEFT;
    case 'R':
      return RIGHT;
    case 'U':
      return UP;
    case 'D':
      return DOWN;
  }

  return NONE;
}

void setup() {
  //Again, probably could clean this up by iterating over an enumerated class
  pinMode(X_BUTTON, OUTPUT);
  digitalWrite(X_BUTTON, RELEASED);
  pinMode(A_BUTTON, OUTPUT);
  digitalWrite(A_BUTTON, RELEASED);
  pinMode(Y_BUTTON, OUTPUT);
  digitalWrite(Y_BUTTON, RELEASED);
  pinMode(B_BUTTON, OUTPUT);
  digitalWrite(B_BUTTON, RELEASED);

  pinMode(RIGHT, OUTPUT);
  digitalWrite(RIGHT, RELEASED);
  pinMode(DOWN, OUTPUT);
  digitalWrite(DOWN, RELEASED);
  pinMode(UP, OUTPUT);
  digitalWrite(UP, RELEASED);
  pinMode(LEFT, OUTPUT);
  digitalWrite(LEFT, RELEASED);

  Serial.begin(19200);
}

void loop() {
  while(!Serial.available());
  
  Serial.readBytes(INPUT_BUFFER,2);

  ButtonState buttonState = getButtonState(INPUT_BUFFER[0]);
  Button button = getButton(INPUT_BUFFER[1]);

  if(buttonState != ERROR){
    digitalWrite(button, buttonState);
    sprintf(OUTPUT_MESSAGE, "Received [%c,%c]. interpreted as [Pin %d, State %d].", INPUT_BUFFER[0], INPUT_BUFFER[1], button, buttonState);
    Serial.write(OUTPUT_MESSAGE);
  } else {
    Serial.write("Received Errored input message. Eating next byte to realign.");
    Serial.readBytes(INPUT_BUFFER,1);
  }
}
