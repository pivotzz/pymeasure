from pymeasure.instruments import Instrument
from pymeasure.adapters import SerialAdapter

class ORX325(Instrument):
    def __init__(self, name, address):
        super(ORX325, self).__init__(name=name, address=address, adapter=SerialAdapter(address), includeSCPI=False)

    def initialize(self):
        # Add any initialization specific to ORX325 if needed
        pass

    def set_frequency(self, frequency):
        self.adapter.write(f"FREQ {frequency}HZ")

    def set_amplitude(self, amplitude):
        self.adapter.write(f"AMPL {amplitude}V")

    def query_identity(self):
        return self.ask("*IDN?")  # Use Instrument's ask method directly

# Example usage:
if __name__ == "__main__":
    instrument = ORX325("ORX325", "/dev/cu.usbserial-AB0NF8HO")
    instrument.initialize()  # Initialize if required
    instrument.set_frequency(1000)
    instrument.set_amplitude(1.5)
    print("Identity:", instrument.query_identity())
    instrument.disconnect()
