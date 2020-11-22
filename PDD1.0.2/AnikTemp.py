import sys
sys.path.append('../')
import time
import os
import json
import datetime

from DFRobot_ADS1115 import ADS1115
ADS1115_REG_CONFIG_PGA_6_144V        = 0x00 # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V        = 0x02 # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V        = 0x04 # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V        = 0x06 # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V        = 0x08 # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V        = 0x0A # 0.256V range = Gain 16
ads1115 = ADS1115()

#print(ads1115)
#ads1115.setAddr_ADS1115(0x49)
#while(1):
#    ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)
#    adc0 = ads1115.readVoltage(0)
#    print(adc0)
#    time.sleep(0.5)
#    temperature = (adc0["r"]/0.01)-50
#    print("Temperature : %0.02f°F" % temperature)
#    time.sleep(0.5)
   
ads1115.setAddr_ADS1115(0x49)
ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)

path_to_script = os.path.dirname(os.path.abspath(__file__))
#print(path_to_script)
try:
    os.mkdir("logs")
except:
    pass
new_file_path = os.path.join(path_to_script,"logs")
#print(new_file_path)
    
while True:
    adc0 = ads1115.readVoltage(0)
    temp = (adc0['r'] - 500) / 10
    data = {}
    data['Time'] = str(datetime.datetime.now())
    data['Temp'] = temp
    json_data = json.dumps(data)
    print(temp)
    with open(os.path.join(new_file_path, 'templog.json'), 'a') as f:
        json.dump(data,f)
        f.write("\n")
        # f.write("Temp: "+ str(temp)+"\n")