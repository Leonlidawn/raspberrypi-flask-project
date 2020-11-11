from __future__ import print_function
import qwiic_max3010x
import time
import sys
import datetime
import os
import signal

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)
    
def millis():
    return int(round(time.time() * 1000))

def runExample():

    print("\nMAX3010x \n")
    sensor = qwiic_max3010x.QwiicMax3010x()

    if sensor.begin() == False:
        print("The MAX3010x device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    else:
        print("The MAX3010x is connected.")

    print("Place your index finger on the sensor with steady pressure.")

    if sensor.setup() == False:
        print("Device setup failure. Please check your connection", \
            file=sys.stderr)
        return
    else:
        print("Setup complete.")

    sensor.setPulseAmplitudeRed(0x0A) # Turn Red LED to low to indicate sensor is running
    sensor.setPulseAmplitudeGreen(0) # Turn off Green LED

    RATE_SIZE = 4 # Increase this for more averaging. 4 is good.
    rates = list(range(RATE_SIZE)) # list of heart rates
    rateSpot = 0
    lastBeat = 0 # Time at which the last beat occurred
    beatsPerMinute = 0.00
    beatAvg = 0
    samplesTaken = 0 # Counter for calculating the Hz or read rate
    startTime = millis() # Used to calculate measurement rate
    beatFlag = False
    REAL_BEAT = 80000 #anik - find the value
    
    path_to_script = os.path.dirname(os.path.abspath(__file__))
    #print(path_to_script)
    try:
        os.mkdir("logs")
    except:
        pass
    new_file_path = os.path.join(path_to_script,"logs")
    #print(new_file_path)
    
    while True:
                
        irValue = sensor.getIR()
        samplesTaken += 1
        if sensor.checkForBeat(irValue) == True:
            if(irValue > REAL_BEAT): #irValue for a real beat??
                # We sensed a beat!
                beatFlag = True
                now = datetime.datetime.now()
                print('[' + str(now) +']' + ' SENSED A BEAT')
            else:
                beatFlag = False
                now = datetime.datetime.now()
                print('[' + str(now) +']' + ' NO FINGER DETECTED')
                
            delta = ( millis() - lastBeat )
            lastBeat = millis() 
    
            beatsPerMinute = 60 / (delta / 1000.0)
            beatsPerMinute = round(beatsPerMinute,1)
    
            if beatsPerMinute < 255 and beatsPerMinute > 20:
                rateSpot += 1
                rateSpot %= RATE_SIZE # Wrap variable
                rates[rateSpot] = beatsPerMinute # Store this reading in the array

                # Take average of readings
                beatAvg = 0
                for x in range(0, RATE_SIZE):
                    beatAvg += rates[x]
                beatAvg /= RATE_SIZE
                beatAvg = round(beatAvg)
        
        Hz = round(float(samplesTaken) / ( ( millis() - startTime ) / 1000.0 ) , 2)
        if ((samplesTaken % 200 ) == 0 and beatFlag == True):
            now = datetime.datetime.now()
            print(\
                    '[' + str(now) +']',\
                    'IR=', irValue , ' \t',\
                    'BPM=', beatsPerMinute , '\t',\
                                                                       #'DCE', getDCE() , '\t',\
                    'Avg=', beatAvg , '\t',\
                    'Hz=', Hz, \
                )
            with open(os.path.join(new_file_path, 'hblog.txt'), 'a') as f:
                f.write("BPM: "+ str(beatsPerMinute)+ " " + "Avg:"+ str(beatAvg) +"\n")
        '''try:
            time.sleep(30)
        except KeyboardInterrupt:
            print('keyboard interrupt detected, exiting...')'''
    
if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 5")
        sys.exit(0)



