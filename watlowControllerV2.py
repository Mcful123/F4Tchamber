 # -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 09:29:00 2021

@author: chomi
"""
from pyModbusTCP.client import ModbusClient
import struct

c = ModbusClient(host="192.167.0.222", auto_open=True)
temps = []

def convert(t):
    #convert celsius to hex 32bit IEEE-754 and splitting into lower and higher bytes
    full = hex(struct.unpack('<I', struct.pack('<f', t))[0])
    high = full[0:6]
    low = '0x' + full[6:11]
    if(len(low) == 2):
        low += '0'
    return [int(low,0), int(high,0)]

def reconnect():
    #connecting to chamber controller 
    global c
    c = ModbusClient(host="192.167.0.222", auto_open=True)

def set_profile(t_hr, t_min, profile):
    #staging profile  for edit
    global temps
    if(0 < profile < 40):
        c.write_single_register(18888, profile) # select 4
        c.write_single_register(18890, 1770) # set to edit mode
    else:
        print('Profile number out of range')
        return
    
    #setting profile
    if(len(temps) == 0):
        print('temps empty')
        return
    step_count = 2*len(temps) + 1
    t_idx = 0
    for i in range(1,step_count):
        if(i%2==0): #setting every other step as soak for 30 minutes
            c.write_single_register(19094+((i-1)*170), 87) #set step i to soak
            c.write_single_register(19096+((i-1)*170), t_hr) # 0 hours
            c.write_single_register(19098+((i-1)*170), t_min) # 30 minutes
            c.write_single_register(19100+((i-1)*170), 0) # 0 seconds
            c.write_single_register(19168+((i-1)*170), 62) #set event 8 OFF
        else:
            tempC = temps[t_idx] # getting temperature of step   
            t_idx += 1
            c.write_single_register(19094+((i-1)*170), 1927) #set step i to instant change
            c.write_single_register(19096+((i-1)*170), 0) # hours
            c.write_single_register(19098+((i-1)*170), 0) # 0 minutes
            c.write_single_register(19100+((i-1)*170), 2) # 2 seconds
            c.write_single_register(19138+((i-1)*170), 63) # set guranteed soak on
            c.write_multiple_registers(19114+((i-1)*170), convert(tempC)) # set temperature
            c.write_single_register(19168+((i-1)*170), 62) # set event 8 OFF

    b = c.read_holding_registers(18920) #gets number of steps in profile 
    c.write_single_register(19168+((b[0]-1)*170), 63) # turn event 8 ON for last step
    # event 8 = 'turn chamber off after end of step'

def start_profile(profile):
    reg = 18484 + 2*profile
    c.write_single_register(reg, 1782)

def set_temps():
    global temps
    #populate temps with desired soak temperatures in order
    for i in range(13):
        x = i
        if(i > 6):
            x = -(x-12)
        t = -20 + x*20
        temps.append(t)
    # temps = [-20, 0, 20, 40, 60, 80, 100, 80, 60, 40, 20, 0, -20]
    
def terminate():
    # put one step profile at profile 40.
    # set it to turn off at the end of profile. 
    # start profile and after 1 second, chamber will turn off
    c.write_single_register(16566, 148) # terminate current profile
    c.write_single_register(18888, 40) # select 40
    c.write_single_register(18890, 1770) # set to edit mode
    c.write_single_register(19094, 1927) # set to instant change
    c.write_single_register(19096, 0) # 0 hours
    c.write_single_register(19098, 0) # 0 minutes
    c.write_single_register(19100, 1) # 1 seconds
    c.write_single_register(19138, 62) # set guranteed soak off
    c.write_multiple_registers(19114, convert(20)) # set temperature
    c.write_single_register(19168, 63) # set event 8 ON
    c.write_single_register(18564, 1782) #start profile 40
    
def pause():
    # pause currently running profile
    c.write_single_register(16566, 146)
    
def resume():
    # resume currently paused profile
    c.write_single_register(16564, 147)
        
