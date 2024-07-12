

from lakeshore import Model335



temp_controller = Model335(com_port="COM3", baud_rate=57600)
temperature = temp_controller.get_heater_output(1)
print(temperature)