import serial
import time

# Define the serial port settings
port = "/dev/cu.usbserial-AB0NF8HO"  # Correct port name
baudrate = 9600  # Replace with your baud rate

try:
    # Initialize serial connection
    ser = serial.Serial(port, baudrate, timeout=2)  # Increased timeout to 2 seconds
    print(f"Opened serial port {port} at {baudrate} baud.")
except Exception as e:
    print(f"Failed to open serial port {port}: {e}")
    exit()

# Function to send a command and read the response
def send_command(command):
    print(f"Sending command: {command}")
    command = command + "\r"  # Append \r for EOS terminator
    ser.write(command.encode('utf-8'))
    time.sleep(1)  # Delay depending on device response time
    response = ""
    while ser.in_waiting > 0:
        response_chunk = ser.read(ser.in_waiting).decode('utf-8')
        response += response_chunk
        time.sleep(0.1)  # Small delay to ensure complete response
    print(f"Raw response: {response}")
    return response.strip()

# Check if the connection is open
if ser.isOpen():
    print(f"Connected to {port} at {baudrate} baud.")

    # Example commands
    commands = [
        "*IDN?",                # Query device identification
        "SOURCE:FREQ 200HZ",    # Set frequency to 200 Hz
        "SOURCE:VOLTAGE 2"      # Set amplitude to 2V
    ]

    for command in commands:
        response = send_command(command)
        print(f"Response to {command.strip()}: {response}")

    # Read back the amplitude to verify
    print("Reading back amplitude...")
    amplitude_response = send_command("SOURCE:VOLTAGE?")
    print(f"Amplitude readback: {amplitude_response}")

    # Close serial connection
    ser.close()
    print("Serial connection closed.")

else:
    print(f"Failed to open {port}.")
