import serial
import time

# Define the serial port settings
port = "/dev/cu.usbserial-AB0NF8HO"  # Replace with your actual port
baudrate = 9600  # Replace with your baud rate

# Initialize serial connection
ser = serial.Serial(port, baudrate, timeout=2)  # Increased timeout to 2 seconds

# Check if the connection is open
if ser.isOpen():
    print(f"Connected to {port} at {baudrate} baud.")

    # Example commands
    commands = [
        "*IDN?",                # Query device identification
        "SOURCE:FREQ 200HZ"      # Set frequency to 1 kHz using SOURCE:FREQ
    ]

    for command in commands:
        # Send command with appropriate termination
        command = command + "\n"  # Append \n for EOS terminator
        ser.write(command.encode('utf-8'))
        time.sleep(1)  # Optional delay depending on device response time

        # Read response
        response = ser.read_all().decode('utf-8').strip()
        print(f"Sent command: {command.strip()}, Response: {response}")
        

    # Close serial connection
    ser.close()
    print("Serial connection closed.")

else:
    print(f"Failed to open {port}.")
