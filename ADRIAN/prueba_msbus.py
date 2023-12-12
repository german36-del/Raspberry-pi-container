import smbus

device_address = 0x77

bus_number = 1

bus = smbus.SMBus (bus_number)

registro = 0x00

num_bytes = 8

data = bus.read_i2c_block_data(device_address, registro, num_bytes)

print("Datos leídos:", data)
