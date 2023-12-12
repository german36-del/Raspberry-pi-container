#!/usr/bin/env python

import bluerobotics_navigator as navigator

print("Initializing navigator module.")
navigator.init()

print("Setting led on!")
navigator.set_led(navigator.UserLed.Led1, True)

print(f"Temperature: {navigator.read_temp()}")
print(f"Pressure: {navigator.read_pressure()}")

print(
    f"Data ADC Channels: {navigator.read_adc_all().channel}"
)

print(f"Data ADC Channel: 1 = {navigator.read_adc(navigator.AdcChannel.Ch1)}")

data = navigator.read_mag()
print(f"Magnetic field: X = {data.x}, Y = {data.y}, Z = {data.z}")
