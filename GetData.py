#Author - Andrew Guthrie

import numpy as np
import scipy as sc
import visa
import pyvisa.highlevel
import time
from NetworkAnalyzer import NetworkAnalyzer
from Agilent34401A import Agilent34401A
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

from sys import argv
import os
import pyqtgraph.exporters
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)




def MeasurementsSettings():


    Measurements = {'MeasurementsDevice': '$15\,\mathrm{\mu m}$ sample (Contacts 1-2)',
                    'MeasurementsType': 'Pumping 1K pot. Excite 25mkm beam looking for 15mkm beam',
                    'LineAttenuation': -40}



    Frequency = {'CenterStart': 947.5e6,
                 'CenterStop': 1e9,
                 'CenterPoints': 1001,
                 'CenterSpan': 50e6,
                 'Points': 1001}


    FrequencyArray = np.linspace(Frequency['CenterStart'],Frequency['CenterStop'],Frequency['CenterPoints'])


    Power = {'Start': 0,
             'Stop': 0,
             'Points':1}

    PowerArray = np.linspace(Power['Start'],Power['Stop'],Power['Points'])


    Averages = {'Points':1,
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


    File = {'Data':'C:/Users/guthrie/PycharmProjects/GetData/.idea/Data/' + str(time.strftime("%Y-%m-%d-%H-%M-%S")),
            'Log':'C:/Users/guthrie/PycharmProjects/GetData/.idea/Labbook/Labbook.Tex',
            'Plots': 'C:/Users/guthrie/PycharmProjects/GetData/.idea/Plots/Plot1' + str(time.strftime("%Y-%m-%d-%H-%M-%S"))}


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


def Plot(Settings,sReal,sImag,frequency):


    #Caluclate magnitude and phase from real and imaginary parts of Signal

    phase = []
    magnitude = []
    for x in range(0, len(sReal)):
        if (sReal != 0):
            phase.append(np.arctan(sImag[x] / sReal[x]))
            magnitude.append(np.sqrt(np.power(sImag[x], 2) + np.power(sReal[x], 2)))
        else: phase.append(0)


    #Create Window

    win = pg.GraphicsWindow(title="")
    win.resize(600, 900)
    win.setBackground((255,255,255))

    win.setWindowTitle('Frequency Sweep')


    #Add Frequency vs Magnitude plot


    p1 = win.addPlot(title="Magnitude")
    p1.setLabel('left', "|S21|", units='')
    p1.setLabel('bottom', "Frequency", units='')
    p1.plot(frequency, magnitude,pen= pg.mkPen('r', width=2))

    win.nextRow()

    #Add Frequency vs Phase plot

    p2 = win.addPlot(title="Phase")
    p2.plot(frequency, phase, pen= pg.mkPen('b', width=2))
    p2.setLabel('left', "Phase", units='')
    p2.setLabel('bottom', "Frequency", units='')


    #Used in pyqtgraph to display interactive graph
    if __name__ == '__main__':
        import sys
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

            exporter = pg.exporters.ImageExporter(p1)
            exporter.parameters()['width'] = 1000
            exporter.parameters()['height'] = 1000
            exporter.export(str(Settings['File']['Plots'] + 'Mag.png'))

            exporter = pg.exporters.ImageExporter(p2)
            exporter.parameters()['width'] = 1000
            exporter.parameters()['height'] = 1000
            exporter.export(str(Settings['File']['Plots'] + 'Phase.png'))



    #Creates data file with all frequency and amplitude data
    data = open(Settings['File']['Data'] + '.txt', 'w')
    data.write("Frequency(Hz)" +  '\t' + 'In-Phase Amplitude' +  '\t' +  'Out-of-Phase Amplitude' + '\t' + 'Magnitude' + '\t' + 'Phase' '\n')

    for x in range(0,len(sReal)):
        data.write(str(frequency[x]) +  '\t' + str(sReal[x]) +  '\t' +  str(sImag[x]) + '\t' + str(magnitude[x]) + '\t' + str(phase[x]) + '\n')

    data.close()





    return



def Labbook(Settings):




    book = open(Settings['File']['Log'], 'r+')
    book.seek(0, os.SEEK_END)
    book.seek(book.tell() - 16, os.SEEK_SET)
    book.truncate()
    book.close()



    book = open(Settings['File']['Log'],'a')


    Tex =   [r'',
    r'    \section{' + time.strftime("%c")+'}',
    r'    \begin{tabular}{|p{0.6 \textwidth}|p{0.35\textwidth}|}',
    r'        \hline',
    r'        \begin{flushleft}',
    r'            \textbf{\underline{' +Settings['Measurements']['MeasurementsType']+'}}',
    r'        \end{flushleft}',
    r'        \includegraphics[width=\linewidth]{' + str(Settings['File']['Plots'] + 'Mag.png') + '}',
    r'        \includegraphics[width=\linewidth]{' + str(Settings['File']['Plots'] + 'Phase.png') + '}',
    r'        \newline \textbf{Program:} GetData.m',
    r'        \newline \textbf{Data file name:}',
    r'            \newline ' + str(Settings['File']['Data']) + '.txt',
    r'        \newline \textbf{Figure file name:}',
    r'            \newline ' + str(Settings['File']['Plots']) + '.png',
    '        &	',
    r'        \begin{flushright}',
    r'            \textbf{\underline{' + str(Settings['Measurements']['MeasurementsDevice']) +'}}',
    '        \end{flushright}',
    '        Line attenuation: ' + str(Settings['Measurements']['LineAttenuation']) + 'dB',
    r'        \newline \textbf{Instruments:}',
    r'        \newline Magnetic field is controlled by Oxford PS120;',
    r'        \newline Temperature is controlled by Lakeshore;',
    r'        \newline Pressure is obtained by Agilent34401A voltmeter;',
    r'        \newline Data are obtained by AgilentE5071C Network Analyzer;',
    r'        \vspace{1cm}',
    r'        \newline\textbf{Temperature settings:}',
    r'            \newline $T_{start} = ' + str(Settings['Temperature']['Start']) + '\,\mathrm{K}$',
    r'            \newline $T_{stop} = '+ str(Settings['Temperature']['Stop'])+ '\,\mathrm{K}$',
    r'            \newline $N_{T} = '+ str(Settings['Temperature']['Points'])+ '$',
    r'        \newline\textbf{Initial actual temperature measured by $\mathrm{RuO_x}$ thermometer:}',
    r'            \newline $T_{RuOx} = '+ 'str(Data.Temperature.RuOx(1))'+ '\,\mathrm{K}$',
    r'        \newline\textbf{Initial actual temperature measured by $\mathrm{^4He}$ thermometer:}',
    r'            \newline $T_{He} = '+ 'str(Data.Temperature.He4(1))'+ '\,\mathrm{K}$',
    r'        \newline\textbf{Magnet settings:}',
    r'            \newline $B_{start} = '+ str(Settings['Field']['Start'])+ '\,\mathrm{T}$',
    r'            \newline $B_{stop} = '+ str(Settings['Field']['Stop'])+ '\,\mathrm{T}$',
    r'            \newline Sweeping rate: $'+ str(Settings['Field']['SweepRate'])+ '\,\mathrm{T/min}$',
    r'            \newline $N = '+ str(Settings['Field']['Points'])+ '$',
    r'        \newline\textbf{Initial field:}',
    r'            \newline $B_{0} = '+ 'num2str(Data.Field(1))'+ '\,\mathrm{T}$',
    r'        \newline\textbf{Network analyzer settings:}',
    r'            \newline $f_{centre} =' + str(Settings['NetworkAnalyzer']['Frequency']['CenterStart']/1e6) + '\,\mathrm{MHz}$',
    r'            \newline $f_{span} =' + str(Settings['NetworkAnalyzer']['Frequency']['CenterSpan']/1e6) + '\,\mathrm{MHz}$',
    r'            \newline Points: $' + str(Settings['NetworkAnalyzer']['Frequency']['Points']) + '$',
    r'            \newline $P_{start} =' + str(Settings['NetworkAnalyzer']['Power']['Start']) + '\,\mathrm{dBm}$',
    r'            \newline $P_{stop} =' + str(Settings['NetworkAnalyzer']['Power']['Stop']) + '\,\mathrm{dBm}$',
    r'            \newline Points: $' + str(Settings['NetworkAnalyzer']['Power']['Points']) + '$',
    r'            \newline Bandwidth: $' + str(Settings['NetworkAnalyzer']['Averages']['IFBW']) + '\,\mathrm{Hz}$',
    r'        \\',
    '        \hline',
    '    \end{tabular}',
    '\end{document}'
      ]


    for x in range(0,len(Tex)):
        book.write(str(Tex[x]))
        book.write("\n")

    book.close()





Settings = MeasurementsSettings()
NetworkAnalyzer = NetworkAnalyzer('GPIB1::17::INSTR', Settings)
sReal, sImag, frequency = NetworkAnalyzer.GetTrace()


Agilent34401A = Agilent34401A('GPIB0::21::INSTR',Settings)


print(Agilent34401A.getPressure())


Plot(Settings,sReal,sImag,frequency)

Labbook(Settings)















