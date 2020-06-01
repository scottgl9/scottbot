// written by Scott Glover (scottgl@gmail.com)

#include <AFMotor.h>
#include <string.h>
AF_DCMotor motor1(1, MOTOR12_64KHZ); // create motor #1, 64KHz pwm
AF_DCMotor motor2(2, MOTOR12_64KHZ); // create motor #2, 64KHz pwm
AF_DCMotor motor3(3, MOTOR12_64KHZ); // create motor #3, 64KHz pwm
AF_DCMotor motor4(4, MOTOR12_64KHZ); // create motor #4, 64KHz pwm

#define MAX_STR_LEN 10

uint8_t m1dir, m2dir, m3dir, m4dir;
uint8_t m1speed, m2speed, m3speed, m4speed;

void setup() {
  Serial.begin(9600); // set up Serial library at 9600 bps
  pinMode(LED_BUILTIN, OUTPUT);

  //while (!Serial) {
  //  ; // wait for serial port to connect.
  //}

  //Serial.println("I");

  m1dir = RELEASE;
  m2dir = RELEASE;
  m3dir = RELEASE;
  m4dir = RELEASE;

  m1speed = 255;
  m2speed = 255;
  m3speed = 255;
  m4speed = 255;

  motor1.setSpeed(m1speed);
  motor2.setSpeed(m2speed);
  motor3.setSpeed(m3speed);
  motor4.setSpeed(m4speed);

  motor1.run(m1dir);
  motor2.run(m2dir);
  motor3.run(m3dir);
  motor4.run(m4dir);

  digitalWrite(LED_BUILTIN, HIGH);
  //Serial.println("K");
}

// flush incoming serial buffer
/*
void serialFlush(){
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
}
*/

// OLDFORMAT: C M SS D \n (6 bytes)
// C = 'X': execute command in format above (X F FF 1 \n)
// C = 'T': Run motor test (M, SS, and D arbitrary values)
// NEWFORMAT: C (1 byte)
// Set SPEED commands:
// '0' = set speed 4 motors 100%
// '1' = set speed 4 motors 75%
// '2' = set speed 4 motors 50%
// '3' = set speed 4 motors 25%
// '4' = set speed 2 left motors 75%
// '5' = set speed 2 left motors 50%
// '6' = set speed 2 left motors 25%
// '7' = set speed 2 right motors 75%
// '8' = set speed 2 right motors 50%
// '9' = set speed 2 right motors 25%
// 'A' = set speed 4 motors 0%
// Set DIRECTION commands:
// 'F' set all 4 motors direction to forward
// 'B' set all 4 motors direction to reverse
// 'S' set all 4 motors direction to stop (no direction)
// 'L' set left two motors direction to reverse, right two to forward
// 'R' set right two motors direction to reverse, left two to forward
void loop() {
  bool speed_change = false, dir_change = false;
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    switch (cmd) {
      case '0': // set speed 4 motors 100%
        m1speed = 255;
        m2speed = 255;
        m3speed = 255;
        m4speed = 255;
        speed_change = true;
        break;
      case '1': // set speed 4 motors 75%
        m1speed = 191;
        m2speed = 191;
        m3speed = 191;
        m4speed = 191;
        speed_change = true;
        break;
      case '2': // set speed 4 motors 50%
        m1speed = 127;
        m2speed = 127;
        m3speed = 127;
        m4speed = 127;
        speed_change = true;
        break;
      case '3': // set speed 4 motors 25%
        m1speed = 63;
        m2speed = 63;
        m3speed = 63;
        m4speed = 63;
        speed_change = true;
        break;
      case '4': // set speed 2 left motors 75%
        m1speed = 191;
        m2speed = 191;
        speed_change = true;
        break;
      case '5': // set speed 2 left motors 50%
        m1speed = 127;
        m2speed = 127;
        speed_change = true;
        break;
      case '6': // set speed 2 left motors 25%
        m1speed = 63;
        m2speed = 63;
        speed_change = true;
        break;
      case '7': // set speed 2 right motors 75%
        m3speed = 191;
        m4speed = 191;
        speed_change = true;
        break;
      case '8': // set speed 2 right motors 50%
        m3speed = 127;
        m4speed = 127;
        speed_change = true;
        break;
      case '9': // set speed 2 right motors 25%
        m3speed = 63;
        m4speed = 63;
        speed_change = true;
        break;
      case 'A': // set speed 4 motors 0%
        m1speed = 0;
        m2speed = 0;
        m3speed = 0;
        m4speed = 0;
        speed_change = true;
      case 'F': // set all 4 motors direction to forward
        m1dir = FORWARD;
        m2dir = FORWARD;
        m3dir = FORWARD;
        m4dir = FORWARD;
        dir_change = true;
        break;
      case 'B': // set all 4 motors direction to backward
        m1dir = BACKWARD;
        m2dir = BACKWARD;
        m3dir = BACKWARD;
        m4dir = BACKWARD;
        dir_change = true;
        break;
      case 'S': // set all 4 motors direction to stop (no direction)
        m1dir = RELEASE;
        m2dir = RELEASE;
        m3dir = RELEASE;
        m4dir = RELEASE;
        dir_change = true;
        break;
      case 'L': // set left two motors direction to reverse, right two to forward
        m1dir = BACKWARD;
        m2dir = BACKWARD;
        m3dir = FORWARD;
        m4dir = FORWARD;
        dir_change = true;
        break;
      case 'R': // set right two motors direction to reverse, left two to forward
        m1dir = FORWARD;
        m2dir = FORWARD;
        m3dir = BACKWARD;
        m4dir = BACKWARD;
        dir_change = true;
        break;
      default:
        Serial.write('E');
        return;
    }

    if (speed_change) {
      motor1.setSpeed(m1speed);
      motor2.setSpeed(m2speed);
      motor3.setSpeed(m3speed);
      motor4.setSpeed(m4speed);
    } else if (dir_change) {
      motor1.run(m1dir);
      motor2.run(m2dir);
      motor3.run(m3dir);
      motor4.run(m4dir);
    }

    Serial.write('K');
  }
}

/*
void loop() {
  if (Serial.available() > 0) {
    char c = Serial.read();

    if (count == 0 && c != 'X' && c != 'T') {
      return;
    }
    buf[count] = c;
    count++;
    if (count >= 5) {
      count = 0;
      serialFlush();
      processCommand();
    }
  }
}

void processCommand() {
    byte mselect, mspeed, mdir, mdir2;

    // run motor test
    if (buf[0] == 'T') {
        //digitalWrite(LED_BUILTIN, HIGH);
        motor1.run(FORWARD);
        motor2.run(FORWARD);
        motor3.run(FORWARD);
        motor4.run(FORWARD);
        delay(1000);
        //digitalWrite(LED_BUILTIN, LOW);
        motor1.run(RELEASE);
        motor2.run(RELEASE);
        motor3.run(RELEASE);
        motor4.run(RELEASE);
        delay(1000);
        //digitalWrite(LED_BUILTIN, HIGH);
        motor1.run(BACKWARD);
        motor2.run(BACKWARD);
        motor3.run(BACKWARD);
        motor4.run(BACKWARD);
        delay(1000);
        //digitalWrite(LED_BUILTIN, LOW);
        motor1.run(RELEASE);
        motor2.run(RELEASE);
        motor3.run(RELEASE);
        motor4.run(RELEASE);
        Serial.write('K');
        serialFlush();
        return;
    }

    mselect = (uint8_t)buf[1] - '0';
    mspeed = (uint8_t)((buf[2] - '0') << 4);
    mspeed |= (uint8_t)(buf[3] - '0');
    mdir2 = (uint8_t)(buf[4] - '0');

    if (mdir2 == 0) {
      mdir = RELEASE;
    } else if (mdir2 == 1) {
      mdir = FORWARD;
    } else if (mdir2 == 2) {
      mdir = BACKWARD;
    } else {
      Serial.write('E');
      return;
    }

    // handle motor 1
    if (mselect & 1) {
      if (mspeed != m1speed) {
        motor1.setSpeed(mspeed);
        m1speed = mspeed;
      }
      if (mdir != m1dir) {
        motor1.run(mdir);
        m1dir = mdir;
      }
    }

    // handle motor 2
    if (mselect & 2) {
      if (mspeed != m2speed) {
        motor2.setSpeed(mspeed);
        m2speed = mspeed;
      }
      if (mdir != m2dir) {
        motor2.run(mdir);
        m2dir = mdir;
      }
    }

    // handle motor 3
    if (mselect & 4) {
      if (mspeed != m3speed) {
        motor3.setSpeed(mspeed);
        m3speed = mspeed;
      }
      if (mdir != m3dir) {
        motor3.run(mdir);
        m3dir = mdir;
      }
    }

    // handle motor 4
    if (mselect & 8) {
      if (mspeed != m4speed) {
        motor4.setSpeed(mspeed);
        m4speed = mspeed;
      }
      if (mdir != m4dir) {
        motor4.run(mdir);
        m4dir = mdir;
      }
    }
    Serial.write('K');
}
*/
