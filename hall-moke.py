import sys
import os

print(sys.path)
sys.path.append("/Users/pvtz/Documents/GitHub/pymeasure")

# Utilities
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import logging

# Instruments
from pymeasure.instruments.resources import list_resources
from lakeshore import Model335
from or_x import ORXFunctionGenerator

# pymeasure imports for running the experiment
from pymeasure.experiment import Procedure, Results, unique_filename
from pymeasure.experiment.parameters import FloatParameter
from pymeasure.display.Qt import QtWidgets
from pymeasure.display.windows import ManagedWindow


temp_controller = Model335(com_port = "COM3", baud_rate = 57600)
temp_controller.set_setpoint_ramp_parameter(1, False, 0)
temp_controller.set_control_setpoint(1, 280)
temp_controller.set_heater_range(1, temp_controller.HeaterRange.HIGH)

temp_controller.get_all_kelvin_reading()
print(temp_controller.get_all_kelvin_reading())
temp_controller.disconnect_usb()