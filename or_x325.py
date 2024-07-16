import serial
import time

# Define the serial port settings
port = "/dev/cu.usbserial-AB0NF8HO"  # Correct port name
baudrate = 9600  # Replace with your baud rate

# Initialize serial connection
ser = serial.Serial(port, baudrate, timeout=2)  # Increased timeout to 2 seconds

# Check if the connection is open
if ser.isOpen():
    print(f"Connected to {port} at {baudrate} baud.")

    # Example commands
    commands = [
        "*IDN?",                # Query device identification
        "SOURCE:FREQ 200HZ"     # Set frequency to 200 Hz
    ]

    for command in commands:
        # Send command with appropriate termination
        command = command + "\r\n"  # Append \r\n for EOS terminator
        ser.write(command.encode('utf-8'))
        time.sleep(1)  # Optional delay depending on device response time

        # Read response
        response = ""
        while ser.in_waiting > 0:
            response += ser.read(ser.in_waiting).decode('utf-8')
            time.sleep(1)  # Small delay to ensure complete response
        print(f"Sent command: {command.strip()}, Response: {response.strip()}")

    # Close serial connection
    ser.close()
    print("Serial connection closed.")

else:
    print(f"Failed to open {port}.")
