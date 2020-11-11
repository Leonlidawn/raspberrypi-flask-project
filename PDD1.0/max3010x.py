from __future__ import print_function
import qwiic_max3010x
import time
import sys

def runExample():
    print("\MAX3010x Heartbeat Sensor - Example 1\n")
    sensor = qwiic_max3010x.QwiicMax3010x()

    if sensor.begin() == False:
        print("The MAX3010x device isn't connected to the system. Please check your connection", \
          file=sys.stderr)
        return
    else:
        print("The MAX3010x is connected.")

    if sensor.setup() == False:
        print("Device setup failure. Please check your connection", \
          file=sys.stderr)
        return
    else:
        print("Setup complete.") 

    while True:
        print(\
              'R[', sensor.getRed() , '] \t'\
              'IR[', sensor.getIR() , '] \t'\
              'G[', sensor.getGreen() , ']'\
         )
        time.sleep(0.1)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)