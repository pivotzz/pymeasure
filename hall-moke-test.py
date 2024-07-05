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

# pymeasure imports for running the experiment
from pymeasure.experiment import Procedure, Results, unique_filename
from pymeasure.experiment.parameters import FloatParameter
from pymeasure.display.Qt import QtWidgets
from pymeasure.display.windows import ManagedWindow

log = logging.getLogger("")
log.addHandler(logging.NullHandler())
log.setLevel(logging.INFO)


class TempController(Procedure):
    """
    Procedure class that contains all the code that communicates with the devices.
    3 sections - Startup, Execute, Shutdown.
    Outputs data to the GUI
    """

    # Parameters for the experiment, saved in csv
    min_temperature = FloatParameter("Minimum temperature", units="K", default=10)
    max_temperature = FloatParameter("Maximum temperature", units="K", default=15)
    ramp_rate = FloatParameter("Temperature ramp rate", units="K/min", default=0.5)
    resistance_range = FloatParameter("Resistance Range", units="Ohm", default=200000)
    time_per_measurement = FloatParameter(
        "Time per measurement", units="s", default=0.1
    )
    num_plc = FloatParameter(
        "Number of power line cycles aka. measurement accuracy (0.1/1/10)", default=1
    )

    # These are the data values that will be measured/collected in the experiment
    DATA_COLUMNS = ["Temperature (K)", "Resistance (ohm)"]

    def startup(self):
        """
        Necessary startup actions (Connecting and configuring to devices).
        """
        log.info("Starting up the experiment.")
        # Initialize the instruments
        try:
            self.temp_controller = Model335(com_port="COM3", baud_rate = 57600)
            # Configure LS335 and stabilize at min_temperature
            self.temp_controller.set_control_setpoint(1, self.min_temperature)
            self.temp_controller.set_heater_range(1, self.temp_controller.HeaterRange.LOW)
        except Exception as e:
            log.error(f"Error during startup: {e}")
            raise

    def execute(self):
        """
        Contains the 'experiment' of the procedure.
        Emits results with the data values defined in DATA_COLUMNS.
        """
        log.info("Executing experiment.")
        try:
            # Start ramping
            self.temp_controller.set_control_setpoint(1, self.max_temperature)
            self.temp_controller.set_heater_range(1, self.temp_controller.HeaterRange.HIGH)
            self.temp_controller.set_setpoint_ramp_parameter(1, True, self.ramp_rate)
            
            temperature = self.temp_controller.get_all_kelvin_reading()[0]
            self.emit("results", {"Temperature (K)": temperature})
        except Exception as e:
            log.error(f"Error during execution: {e}")
            raise

    def shutdown(self):
        """
        Shutdown all machines.
        """
        log.info("Shutting down the experiment.")
        try:
            if hasattr(self, 'temp_controller'):
                self.temp_controller.set_control_setpoint(1, 0)
                self.temp_controller.all_heaters_off()
            else:
                log.warning("TempController was not initialized.")
        except Exception as e:
            log.error(f"Error during shutdown: {e}")
            raise


class TempMeasurementWindow(ManagedWindow):
    def __init__(self):
        super().__init__(
            procedure_class=TempController,
            inputs=[
                "min_temperature",
                "max_temperature",
                "ramp_rate",
                "time_per_measurement",
                "num_plc",
            ],
            displays=[
                "min_temperature",
                "max_temperature",
                "ramp_rate",
                "time_per_measurement",
                "num_plc",
            ],
            x_axis="Temperature (K)",
            y_axis="Resistance (ohm)",
        )
        self.setWindowTitle("Temperature Sweep Measurement")

    def queue(self, procedure=None):
        directory = "./"  # Change this to the desired directory
        filename = unique_filename(directory, prefix="T_SWEEP")

        procedure = self.make_procedure()
        results = Results(procedure, filename)
        experiment = self.new_experiment(results)

        self.manager.queue(experiment)


def main():
    app = QtWidgets.QApplication([])
    window = TempMeasurementWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
