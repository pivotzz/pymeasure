import serial
import serial.tools.list_ports
import time

class ORX325FunctionGenerator:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None

    def connect(self):
        """Establish a connection to the function generator."""
        self.connection = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
        if self.connection.is_open:
            print(f"Connected to {self.port} at {self.baudrate} baud.")
        else:
            print("Failed to connect.")

    def disconnect(self):
        """Close the connection to the function generator."""
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Disconnected.")

    def send_command(self, command):
        """Send a command to the function generator."""
        if self.connection and self.connection.is_open:
            command += '\r\n'  # Ensure the command is terminated properly
            self.connection.write(command.encode())
            print(f"Sent command: {command.strip()}")
            time.sleep(0.5)  # Add a small delay to allow the device to respond
        else:
            print("No connection established.")

    def read_response(self):
        """Read the response from the function generator."""
        if self.connection and self.connection.is_open:
            response = self.connection.readline().decode().strip()
            print(f"Response: {response}")
            return response
        else:
            print("No connection established.")
            return None

    def set_frequency(self, frequency):
        """Set the frequency of the function generator."""
        command = f"FREQ {frequency}"
        self.send_command(command)

    def set_amplitude(self, amplitude):
        """Set the amplitude of the function generator."""
        command = f"VOLT {amplitude}"
        self.send_command(command)

    def set_waveform(self, waveform):
        """Set the waveform type of the function generator."""
        command = f"FUNC {waveform}"
        self.send_command(command)

    def get_id(self):
        """Query the function generator's ID."""
        self.send_command("*IDN?")
        return self.read_response()

# Example usage
if __name__ == "__main__":
    generator = ORX325FunctionGenerator(port='/dev/cu.usbserial-AB0NF8HO')
    generator.connect()
    generator.get_id()
    generator.set_frequency(100)  # Set frequency to 100 Hz
    generator.set_amplitude(2)    # Set amplitude to 2 V
    generator.set_waveform('SIN')  # Set waveform to sine
    generator.disconnect()
