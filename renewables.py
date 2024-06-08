#for renewables; simulate different types that each fluctuate following a 
# function with random variations following a normal distribution 
from flexmeasures import Sensor

solar_sensor = Sensor(name="solar_panel", unit="kWh", type="electricity", location="solar_farm")
wind_sensor = Sensor(name="wind_turbine", unit="kWh", type="electricity", location="wind_farm")

battery_sensor = Sensor(name="battery_storage", unit="kWh", type="electricity", location="battery_plant")