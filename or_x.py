import pyvisa
import time

class ORXFunctionGenerator:
    def __init__(self, resource_name):
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(resource_name)
        # Set serial communication parameters
        self.instrument.baud_rate = 9600  # Confirm this value
        self.instrument.parity = pyvisa.constants.Parity.none
        self.instrument.stop_bits = pyvisa.constants.StopBits.one
        self.instrument.data_bits = 8
        self.instrument.timeout = 5000  # Increase timeout to 5000 ms

    def close(self):
        self.instrument.close()
        self.rm.close()

    def set_frequency(self, frequency):
        try:
            print(f"Setting frequency to {frequency} Hz")
            self.instrument.write(f'FREQ {frequency}')
            time.sleep(0.1)  # Add a short delay
        except pyvisa.VisaIOError as e:
            print(f"Failed to set frequency: {e}")

    def set_amplitude(self, amplitude):
        try:
            print(f"Setting amplitude to {amplitude} V")
            self.instrument.write(f'VOLT {amplitude}')
            time.sleep(0.1)  # Add a short delay
        except pyvisa.VisaIOError as e:
            print(f"Failed to set amplitude: {e}")

    def enable_output(self):
        try:
            print("Enabling output")
            self.instrument.write('OUTP ON')
            time.sleep(0.1)  # Add a short delay
        except pyvisa.VisaIOError as e:
            print(f"Failed to enable output: {e}")

    def disable_output(self):
        try:
            print("Disabling output")
            self.instrument.write('OUTP OFF')
            time.sleep(0.1)  # Add a short delay
        except pyvisa.VisaIOError as e:
            print(f"Failed to disable output: {e}")

    def get_id(self):
        try:
            print("Querying device ID")
            return self.instrument.query('*IDN?')
        except pyvisa.VisaIOError as e:
            print(f"Failed to get ID: {e}")
            return None

# Example usage
if __name__ == "__main__":
    resource_name = 'ASRL/dev/cu.usbserial-AB0NF8HO::INSTR'  # Replace with the correct resource name
    fg = ORXFunctionGenerator(resource_name)


    fg.set_frequency(100)  # Set frequency to 100 Hz
    fg.set_amplitude(1)  # Set amplitude to 1 V
    fg.enable_output()
    
    fg.close()

main()