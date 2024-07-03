import pyvisa

class ORXFunctionGenerator:
    def __init__(self, resource_name):
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(resource_name)
    
    def close(self):
        self.instrument.close()
        self.rm.close()

    def set_frequency(self, frequency):
        self.instrument.write(f'FREQ {frequency}')

    def set_amplitude(self, amplitude):
        self.instrument.write(f'VOLT {amplitude}')

    def enable_output(self):
        self.instrument.write('OUTP ON')

    def disable_output(self):
        self.instrument.write('OUTP OFF')

    def get_id(self):
        return self.instrument.query('*IDN?')

# Example usage
if __name__ == "__main__":
    fg = ORXFunctionGenerator('USB0::0x1AB1::0x0641::DG4E210300021::INSTR')  # Adjust the resource name as needed
    print(fg.get_id())
    fg.set_frequency(1000)  # Set frequency to 1000 Hz
    fg.set_amplitude(5)  # Set amplitude to 5 V
    fg.enable_output()
    fg.close()
