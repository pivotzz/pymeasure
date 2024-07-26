import pyvisa

# Initialize the VISA resource manager
rm = pyvisa.ResourceManager()

# List all connected instruments
instruments = rm.list_resources()
print(f"Connected instruments: {instruments}")

if instruments:
    instrument_address = 'GPIB0::12::INSTR'
    instrument = rm.open_resource(instrument_address)

    try:
        # Example SCPI commands to read digitized data
        instrument.write("*RST")  # Reset the instrument
        instrument.write("CONF:VOLT:DC")  # Configure the instrument to measure DC voltage
        instrument.write("INIT")  # Initialize the measurement

        # Read the digitized data
        data = instrument.query("READ?")
        print(f"Digitized Data: {data}")

    except pyvisa.VisaIOError as e:
        print(f"VISA IO Error: {e}")
    finally:
        # Close the connection
        instrument.close()
else:
    print("No instruments found.")
