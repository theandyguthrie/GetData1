#Author - Andrew Guthrie

import numpy as np
import scipy as sc
import matplotlib as plt
import visa
import time









def MeasurementsSettings():


    Measurements = {'MeasurementsDevice': '$15\,\mathrm{\mu m}$ sample (Contacts 1-2)',
                    'MeasurementsType': 'Pumping 1K pot. Excite 25mkm beam looking for 15mkm beam',
                    'LineAttenuation': -40}



    Frequency = {'CenterStart': 8.2e6,
                 'CenterStop': 8.2e6,
                 'CenterPoints': 1001,
                 'CenterSpan': 2e6,
                 'CenterPoints': 1601}


    FrequencyArray = np.linspace(Frequency['CenterStart'],Frequency['CenterStop'],Frequency['CenterPoints'])


    Power = {'Start': 10,
             'Stop': -10,
             'Points':1}

    PowerArray = np.linspace(Power['Start'],Power['Stop'],Power['Points'])


    Averages = {'Points:':1,
                'IFBW': 100}

    Field = {'Start': 5 ,
             'Stop': 5,
             'Points': 1,
             'SweepRate': 0.5}

    FieldArray = np.linspace(Field['Start'],Field['Stop'],Field['Points'])

    Temperature = {'Start': 1 ,
                   'Stop': 1,
                   'Points': 1}

    TemperatureArray = np.linspace(Temperature['Start'], Temperature['Stop'], Temperature['Points'])


    File = {'Dir': ['C:/Users/kafanovs/Dropbox/AL_Beams_in_Helium4/data/raw_data/NEMS/Data/', time.strftime("%d/%m/%Y"), '/'],
            'Log': 'C:/Users/kafanovs/Dropbox/AL_Beams_in_Helium4/data/raw_data/NEMS/LabBook_1.tex',
            'Data': ['C:/Users/kafanovs/Dropbox/AL_Beams_in_Helium4/data/raw_data/NEMS/Data/', time.strftime("%d/%m/%Y")]}


    NetworkAnalyzer = {'Frequency': Frequency,
                       'FrequencyArray': FrequencyArray,
                       'Power': Power,
                       'PowerArray': PowerArray,
                       'Averages': Averages}

    Settings = {'NetworkAnalyzer': NetworkAnalyzer,
                'Field': Field,
                'FieldArray': FieldArray,
                'Temperature':Temperature,
                'TemperatureArray':TemperatureArray,
                'Measurements': Measurements,
                'File': File}

    return Settings


def Initialize_AgilentE5071C(dev,Settings):

    # Define output format
    dev.write(':FORM:DATA REAL')
    dev.write(':FORM:BORD SWAP')
    time.sleep(0.1)

    #Stop automatic triggers
    dev.write(':INIT1:CONT OFF')
    dev.write(':TRIG:AVER OFF')
    dev.write(':TRIG:SOUR BUS')
    time.sleep(0.1)

    #Set linear frequency sweep.
    dev.write(':SENS:SWE:TYPE LIN')
    time.sleep(0.1)

    #Set stepped sweep.
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

    return





Settings = MeasurementsSettings()

rm = visa.ResourceManager()
rm.list_resources()
dev = rm.open_resource('GPIB1::17::INSTR')



Initialize_AgilentE5071C(dev,Settings)


