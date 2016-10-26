import numpy as np
import scipy as sc
import matplotlib as plt
import visa
import pyvisa.highlevel
import time

class NetworkAnalyzer:



    def __init__(self,Address,Settings):
        rm = visa.ResourceManager()
        rm.list_resources()
        global dev
        dev = rm.open_resource(Address)


        #Stops the beeping!
        dev.write(':SYST:BEEP:WARN:STAT OFF')


        #Setup display to show two sweeps of s21, LogMag and Phase
        dev.write(':DISP:SPL D1_2')
        dev.write(':CALC1:PAR:DEF s21')
        dev.write(':CALC2:PAR:DEF s21')
        dev.write(':CALC1:TRAC:FORM MLOG')
        dev.write(':CALC2:TRAC:FORM PHAS')

        dev.InputBufferSize = 2 ^ 16
        dev.OutputBufferSize = 2 ^ 16
        dev.Timeout = 5

        # Define output format
        dev.write(':FORM:DATA REAL')
        dev.write(':FORM:BORD SWAP')
        time.sleep(0.1)

        # Stop automatic triggers
        dev.write(':INIT1:CONT OFF')
        dev.write(':TRIG:AVER OFF')
        dev.write(':TRIG:SOUR BUS')
        time.sleep(0.1)

        # Set linear frequency sweep.
        dev.write(':SENS:SWE:TYPE LIN')
        time.sleep(0.1)

        # Set stepped sweep.
        dev.write(':SENS:SWE:GEN ANAL')
        time.sleep(0.1)

        # Set sweep time to auto.
        dev.write(':SENS:SWE:TIME:AUTO ON')
        time.sleep(0.1)

        # Set sweep delay to zero.
        dev.write(':SENS:SWE:DEL 0')
        time.sleep(0.1)

        # Set frequency.
        dev.write(':SENS:FREQ:CENT ', str(Settings['NetworkAnalyzer']['FrequencyArray'][0]))
        time.sleep(0.1)

        # Set frequency span.
        dev.write(':SENS:FREQ:SPAN ', str(Settings['NetworkAnalyzer']['Frequency']['CenterSpan']))
        time.sleep(0.1)

        # Set Power
        dev.write(':SOUR:POW:LEV:IMM:AMPL ', str(Settings['NetworkAnalyzer']['PowerArray'][0]))
        time.sleep(0.1)

        # Set number of points
        dev.write(':SENS:SWE:POIN ', str(Settings['NetworkAnalyzer']['Frequency']['CenterPoints']))
        time.sleep(0.1)

        # Set IF Bandwidth
        dev.write(':SENS:BAND ', str(Settings['NetworkAnalyzer']['Averages']['IFBW']))
        time.sleep(0.1)

        # Set Averages
        dev.write(':SENS:AVER ON ')
        dev.write(':SENS:AVER:COUN ', str(Settings['NetworkAnalyzer']['Averages']['Points']))
        dev.write(':TRIG:AVER ON ')
        time.sleep(0.1)

        # Turn Smoothing Off
        dev.write(':CALC:SMO OFF ')
        time.sleep(0.1)

        # Trigger Measurements
        dev.write(':SENS:AVER:CLE ')
        dev.write(':INIT:CONT ON ')
        dev.write(':TRIG:SING ')
        time.sleep(0.1)

        # Auto-Scale Data
        dev.write(':DISP:WIND1:TRAC1:Y:AUTO ')
        dev.write(':INIT:CONT ON ')
        print(['Initialised: ', dev.query('*IDN?')])
        time.sleep(0.1)

        return

    def GetTrace(self):
        # Trigger Measurements
        dev.write(':SENS:AVER:CLE')
        dev.write(':INIT:CONT ON')
        dev.write(':TRIG:SING')

        # Measurement completion signalled by setting bit 4 (value=16) in operation status register ... so poll for that condition

        dev.write(':STAT:OPER:COND?')
        time.sleep(0.1)

        while (np.bitwise_and(np.int(dev.read()), 16) == 0):
            dev.write(':STAT:OPER:COND?')
            time.sleep(0.1)

        # Read the trace
        Signal = dev.query_binary_values(':CALC:DATA:SDAT?', datatype='d')


        sImag = []
        sReal = []

        for x in range(0,len(Signal)-1,2):
            sReal.append(Signal[x])
            sImag.append(Signal[x+1])


        # Read frequency data
        frequency = dev.query_binary_values(':SENS:FREQ:DATA?', datatype='d')

        return sReal,sImag,frequency

    def SetPower(self, Power):

        dev.write(':SOUR:POW:LEV:IMM:AMPL %f', Power)
        pause(0.1);

        out = np.double(dev.query(':SOUR:POW:LEV:IMM:AMPL?'))
        return out

    def SetCentralFrequency(self, Frequency):

        dev.write(':SENS:FREQ:CENT', Frequency)
        pause(0.1);

        out = np.double(dev.query(':SENS:FREQ:CENT?'))
        return out

