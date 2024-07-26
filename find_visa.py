import pyvisa

# Initialize the resource manager
rm = pyvisa.ResourceManager()

# List all connected instruments
instruments = rm.list_resources()
print("Connected instruments:", instruments)

# Assuming you found your instrument, open a session
if instruments:
    for instrument in instruments:
        print(instrument)
        try:
            inst = rm.open_resource(instrument)
            idn = inst.query("*IDN?")
            print(f"Instrument {instrument}: {idn}")
        except Exception as e:
            print(f"Failed to connect to {instrument}: {e}")
else:
    print("No instruments found.")
