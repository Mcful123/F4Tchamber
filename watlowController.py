 # -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 09:29:00 2021

@author: chomi
"""
from pyModbusTCP.client import ModbusClient
import struct

#convert celsius to hex 32bit IEEE-754 and splitting into lower and higher bytes
def convert(f):
    full = hex(struct.unpack('<I', struct.pack('<f', f))[0])
    high = full[0:6]
    low = '0x' + full[6:11]
    if(len(low) == 2):
        low += '0'
    return [int(low,0), int(high,0)]

#connecting to chamber controller 
c = ModbusClient(host="192.167.0.222", auto_open=True)

#staging profile 4 for edit
c.write_single_register(18888, 4)
c.write_single_register(18890, 1770)

#setting
for i in range(1,27):
    if(i%2==0): #setting every other step as soak for 30 minutes
        c.write_single_register(19094+((i-1)*170), 87) #set step i to soak
        c.write_single_register(19096+((i-1)*170), 0) # 0 hours
        c.write_single_register(19098+((i-1)*170), 30) # 30 minutes
        c.write_single_register(19100+((i-1)*170), 0) # 0 seconds
        c.write_single_register(19168+((i-1)*170), 62) #set event 8 OFF
    else:
        if(i>13): 
            x = -(i-26)
        else: 
            x = i
        tempC = int(x*10 - 30) # getting temperature of step   
        c.write_single_register(19094+((i-1)*170), 1927) #set step i to instant change
        c.write_single_register(19096+((i-1)*170), 0) # hours
        c.write_single_register(19098+((i-1)*170), 0) # 0 minutes
        c.write_single_register(19100+((i-1)*170), 2) # 2 seconds
        c.write_single_register(19138+((i-1)*170), 63) # set guranteed soak on
        c.write_multiple_registers(19114+((i-1)*170), convert(tempC)) # set temperature
        c.write_single_register(19168+((i-1)*170), 62) # set event 8 OFF

b = c.read_holding_registers(18920)
print(b)
c.write_single_register(19168+((b[0]-1)*170), 63) # turn event 8 ON for last step
# event 8 = 'turn chamber off after end of step'

        