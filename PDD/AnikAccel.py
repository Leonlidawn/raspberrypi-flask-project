# Simple demo of reading the MMA8451 orientation every second.
# Author: Tony DiCola
import time
import board
import busio
import adafruit_mma8451
import os
import json
import datetime


# Initialize I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
time.sleep(1) #anik
# Initialize MMA8451 module.
sensor = adafruit_mma8451.MMA8451(i2c)
# Optionally change the address if it's not the default:
# sensor = adafruit_mma8451.MMA8451(i2c, address=0x1C)

# Optionally change the range from its default of +/-4G:
# sensor.range = adafruit_mma8451.RANGE_2G  # +/- 2G
# sensor.range = adafruit_mma8451.RANGE_4G  # +/- 4G (default)
# sensor.range = adafruit_mma8451.RANGE_8G  # +/- 8G

# Optionally change the data rate from its default of 800hz:
# sensor.data_rate = adafruit_mma8451.DATARATE_800HZ  #  800Hz (default)
# sensor.data_rate = adafruit_mma8451.DATARATE_400HZ  #  400Hz
# sensor.data_rate = adafruit_mma8451.DATARATE_200HZ  #  200Hz
# sensor.data_rate = adafruit_mma8451.DATARATE_100HZ  #  100Hz
# sensor.data_rate = adafruit_mma8451.DATARATE_50HZ   #   50Hz
# sensor.data_rate = adafruit_mma8451.DATARATE_12_5HZ # 12.5Hz
# sensor.data_rate = adafruit_mma8451.DATARATE_6_25HZ # 6.25Hz
# sensor.data_rate = adafruit_mma8451.DATARATE_1_56HZ # 1.56Hz

path_to_script = os.path.dirname(os.path.abspath(__file__))
#print(path_to_script)
try:
    os.mkdir("logs")
except:
    pass
new_file_path = os.path.join(path_to_script,"logs")
    #print(new_file_path)
    
# Main loop to print the acceleration and orientation every second.
while True:
    with open(os.path.join(new_file_path, 'accellog.json'), 'a') as f:
        x, y, z = sensor.acceleration
        print(
            "Acceleration: x={0:0.3f}m/s^2 y={1:0.3f}m/s^2 z={2:0.3f}m/s^2".format(x, y, z)
        )
        data = {}
        data['time'] = str(datetime.datetime.now())
        data['x'] = x
        data['y'] = y
        data['z'] = z
        
        #with open(os.path.join(new_file_path, 'acceldump.txt'), 'a') as f:
        
        # f.write("Acceleration:" + " x = " + str(x) + " y = " + str(y) + " z= " + str(z)+"\n")
        #f.write("test")
        orientation = sensor.orientation
        # Orientation is one of these values:
        #  - PL_PUF: Portrait, up, front
        #  - PL_PUB: Portrait, up, back
        #  - PL_PDF: Portrait, down, front
        #  - PL_PDB: Portrait, down, back
        #  - PL_LRF: Landscape, right, front
        #  - PL_LRB: Landscape, right, back
        #  - PL_LLF: Landscape, left, front
        #  - PL_LLB: Landscape, left, back
        print("Orientation: ", end="")
        if orientation == adafruit_mma8451.PL_PUF:
            t_orientation =  ("Portrait, up, front")
            data['orientation']=t_orientation
            json_data = json.dumps(data)
            json.dump(data,f)
            f.write("\n")
            print("Portrait, up, front")
            # f.write("Portrait, up, front"+"\n")
        elif orientation == adafruit_mma8451.PL_PUB:
            t_orientation = ("Portrait, up, back")
            data['orientation']=t_orientation
            json_data = json.dumps(data)
            json.dump(data,f)
            f.write("\n")
            print("Portrait, up, back")
            # f.write("Portrait, up, back"+"\n")
        elif orientation == adafruit_mma8451.PL_PDF:
            t_orientation = ("Portrait, down, front")
            data['orientation']=t_orientation
            json_data = json.dumps(data)
            json.dump(data,f)
            f.write("\n")
            print("Portrait, down, front"+"\n")
            # f.write("Portrait, down, front")
        elif orientation == adafruit_mma8451.PL_PDB:
            t_orientation = ("Portrait, down, back")
            data['orientation']=t_orientation
            json_data = json.dumps(data)
            json.dump(data,f)
            f.write("\n")
            print("Portrait, down, back")
            # f.write("Portrait, down, back"+"\n")
        elif orientation == adafruit_mma8451.PL_LRF:
            t_orientation = ("Landscape, right, front")
            data['orientation']=t_orientation
            json_data = json.dumps(data)
            json.dump(data,f)
            f.write("\n")
            print("Landscape, right, front")
            # f.write("Landscape, right, front"+"\n")
        elif orientation == adafruit_mma8451.PL_LRB:
            t_orientation = ("Landscape, right, back")
            data['orientation']=t_orientation
            json_data = json.dumps(data)
            json.dump(data,f)
            f.write("\n")
            print("Landscape, right, back")
            # f.write("Landscape, right, back"+"\n")
        elif orientation == adafruit_mma8451.PL_LLF:
            t_orientation = ("Landscape, left, front")
            data['orientation']=t_orientation
            json_data = json.dumps(data)
            json.dump(data,f)
            f.write("\n")
            print("Landscape, left, front")
            # f.write("Landscape, left, front"+"\n")
        elif orientation == adafruit_mma8451.PL_LLB:
            t_orientation = ("Landscape, left, back")
            data['orientation']=t_orientation
            json_data = json.dumps(data)
            json.dump(data,f)
            f.write("\n")
            print("Landscape, left, back")
            # f.write("Landscape, left, back"+"\n")
        time.sleep(1.0)
