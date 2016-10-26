import numpy as np
import scipy as sc
import visa
import pyvisa.highlevel
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore



class Agilent34401A:


    def __init__(self, Address, Settings):
        rm = visa.ResourceManager()
        rm.list_resources()
        global dev
        dev = rm.open_resource(Address)

        print(['Initialised: ', dev.query('*IDN?')])


    def getPressure(self):

        pressure = dev.query('MEAS:VOLT:DC?')

        return pressure