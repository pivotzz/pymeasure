import sys
import os
import time

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
    min_temperature = FloatParameter("Minimum temperature", units="K", default=305)
    max_temperature = FloatParameter("Maximum temperature", units="K", default=310)
    ramp_rate = FloatParameter("Temperature ramp rate", units="K/min", default=0.5)
    time_per_measurement = FloatParameter(
        "Time per measurement", units="s", default=0.1
    )

    # These are the data values that will be measured/collected in the experiment
    DATA_COLUMNS = ["Elapsed Time (s)", "Temperature (K)"]

    def startup(self):
        """
        Necessary startup actions (Connecting and configuring to devices).
        """
        log.info("Starting up the experiment.")
        # Initialize the instruments
        try:
            self.temp_controller = Model335(com_port="COM3")
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
        start_time = time.time()
        
        try:
            # Start ramping
            self.temp_controller.set_control_setpoint(1, self.max_temperature)
            self.temp_controller.set_heater_range(1, self.temp_controller.HeaterRange.HIGH)
            self.temp_controller.set_setpoint_ramp_parameter(1, True, self.ramp_rate)
            
            # Main loop
            while True:
                sleep(self.time_per_measurement)  # wait for the specified measurement time
                elapsed_time = time.time() - start_time
                temperature = self.temp_controller.get_all_kelvin_reading()[0]  # Get sample stage temperature

                self.emit(
                    "results",
                    {"Elapsed Time (s)": elapsed_time, "Temperature (K)": temperature},
                )

                # stop measuring once reached max temperature
                if abs(temperature - self.max_temperature) < 0.1:
                    break

                if self.should_stop():
                    log.warning("Catch stop command in procedure")
                    self.temp_controller.all_heaters_off()
                    break

        except Exception as e:
            log.error(f"Error during execution: {e}")
            raise

        log.info("Experiment executed")

    def shutdown(self):
        """
        Shutdown all machines.
        """
        log.info("Shutting down")
        if hasattr(self, 'temp_controller'):
            self.temp_controller.set_control_setpoint(1, 0)
            self.temp_controller.all_heaters_off()
        else:
            log.error("temp_controller is not initialized.")


class TempMeasurementWindow(ManagedWindow):
    def __init__(self):
        super().__init__(
            procedure_class=TempController,
            inputs=[
                "min_temperature",
                "max_temperature",
                "ramp_rate",
                "time_per_measurement",
            ],
            displays=[
                "min_temperature",
                "max_temperature",
                "ramp_rate",
                "time_per_measurement",
            ],
            x_axis="Elapsed Time (s)",
            y_axis="Temperature (K)",
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
