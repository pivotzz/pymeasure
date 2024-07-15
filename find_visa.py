import pyvisa

def list_resources():
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    for resource in resources:
        print(resource)

if __name__ == "__main__":
    list_resources()



