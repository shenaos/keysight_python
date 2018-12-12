#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 18:11:51 2018

@author: labfluidos
"""
import visa
import numpy as np
import matplotlib.pyplot as plt
##########
#some useful variables

ts = ""
datos = " "

values = []
s =  np.empty([])
N =  np.empty([])
t =  np.empty([])
########
rm = visa.ResourceManager()
my_instrument = rm.open_resource('TCPIPO::172.16.20.93::INSTR')#Set the VISA Address
print(my_instrument.query('*IDN?'))#get the id of the instrument
my_instrument.timeout = 20000# Set interface timeout to 10 seconds
my_instrument.chunk_size = 102400 #200000 #
#Initialize the instrument to a preset state
my_instrument.write('*RST')

##configure the  time parameters of the signal 
my_instrument.write(':TIMebase:RANGe 50E-4')#time base to 50us/div
my_instrument.write(':TIMebase:DELay 0')#delay to zero
my_instrument.write(':TIMebase:REFerence CENTer')#Display ref. at center


#vertcial parameters voltage
my_instrument.write(':CHANnel1:PROBe 10')#probe attenuation to 10:1
my_instrument.write(':CHANnel1:RANGe 2')#Vertical range 1.6 full scale
my_instrument.write(':CHANnel1:SCALe 1')

#trigger parameters
my_instrument.write(':TRIGger:SWEep NORMal')
my_instrument.write(':TRIGger:LEVel 0.8')
my_instrument.write(":TRIGger:SLOPe POSitive")



my_instrument.write(':WAVEFORM:SOURCE CHAN1')
my_instrument.write(":ACQuire:TYPE NORM")

#my_instrument.write(":ACQuire:TYPE AVERage")
my_instrument.write(":ACQuire:COMPlete 100")
#my_instrument.write(":ACQuire:COUNt 8")
my_instrument.write(":WAVeform:FORMat ASCII")
my_instrument.write(":WAV:POIN:MODE RAW")



my_instrument.write(':ACQ:POIN 10000')
my_instrument.write(':WAVEFORM:POINTS 10000')


#this instruction let you read the time scale
my_instrument.write(':WAV:XINC?')
ts =  my_instrument.read()
my_instrument.write(':DIGITIZE CHAN1')
#values = my_instrument.query(':WAV:DATA?',delay=None)
#my_instrument.write(':WAV:DATA?')
values = my_instrument.query_ascii_values(':WAV:DATA?',converter=u's')
my_instrument.close()


values =  values[1:]
for i in range(0,len(values)):
    
    values[i] = float(values[i])

values =  np.array(values, dtype = np.float32)

s = values 

#centering the signal
s = s - np.mean(s) 
ts = float(ts)
#time vector
N = len(s)
t = np.linspace(0, ts*N, N)



plt.plot(t, s)
plt.show()


  

    
    


