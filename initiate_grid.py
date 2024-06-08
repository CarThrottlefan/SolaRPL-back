import datetime
import numpy as np
from timely_beliefs import TimedBelief
from datetime import timedelta
import pytz

# In-memory data storage
class InMemoryDB:
    def __init__(self):
        self.generic_asset_types = []
        self.generic_assets = []
        self.sensors = []
        self.custom_sources = []
        self.beliefs = []

db = InMemoryDB()

# Define the Generic Asset Type class
class GenericAssetType:
    def __init__(self, name, description):
        self.name = name
        self.description = description

# Define the Generic Asset class
class GenericAsset:
    def __init__(self, name, generic_asset_type):
        self.name = name
        self.generic_asset_type = generic_asset_type

# Define the Sensor class
class Sensor:
    def __init__(self, name, unit, generic_asset):
        self.name = name
        self.unit = unit
        self.generic_asset = generic_asset

# Define the Custom Source class
class CustomSource:
    def __init__(self, name):
        self.name = name

# Add asset types to the in-memory database
solar_type = GenericAssetType(name="solar_panel", description="Solar Panel")
wind_type = GenericAssetType(name="wind_turbine", description="Wind Turbine")
grid_type = GenericAssetType(name="grid", description="Electric Grid")
battery_type = GenericAssetType(name="battery_storage", description="Battery Storage")
consumer_type = GenericAssetType(name="consumer_meter", description="Consumer Meter")

db.generic_asset_types.extend([solar_type, wind_type, grid_type, battery_type, consumer_type])

# Define Generic Assets
solar_asset = GenericAsset(name="Solar Farm 1", generic_asset_type=solar_type)
wind_asset = GenericAsset(name="Wind Farm 1", generic_asset_type=wind_type)
grid_asset = GenericAsset(name="Main Grid", generic_asset_type=grid_type)
battery_asset = GenericAsset(name="Battery Storage 1", generic_asset_type=battery_type)
consumer_assets = [GenericAsset(name=f"Consumer Home {i}", generic_asset_type=consumer_type) for i in range(5)]

db.generic_assets.extend([solar_asset, wind_asset, grid_asset, battery_asset] + consumer_assets)

# Define Sensors
solar_sensor = Sensor(name="solar_panel_sensor", unit="kWh", generic_asset=solar_asset)
wind_sensor = Sensor(name="wind_turbine_sensor", unit="kWh", generic_asset=wind_asset)
grid_sensor = Sensor(name="grid_sensor", unit="kWh", generic_asset=grid_asset)
battery_sensor = Sensor(name="battery_storage_sensor", unit="kWh", generic_asset=battery_asset)
consumer_sensors = [Sensor(name=f"consumer_meter_{i}", unit="kWh", generic_asset=consumer_assets[i]) for i in range(5)]

db.sensors.extend([solar_sensor, wind_sensor, grid_sensor, battery_sensor] + consumer_sensors)

# Example usage of the sensors
print(f"Solar Sensor: {solar_sensor.name}")
print(f"Wind Sensor: {wind_sensor.name}")
print(f"Grid Sensor: {grid_sensor.name}")
print(f"Battery Sensor: {battery_sensor.name}")
for i, consumer_sensor in enumerate(consumer_sensors):
    print(f"Consumer Sensor {i}: {consumer_sensor.name}")

# Add the Custom Source to the in-memory database
custom_source = CustomSource(name="Simulation Source")
db.custom_sources.append(custom_source)

# Function to add a reading
def add_reading(sensor, value, timestamp):
    belief = TimedBelief(
        event_start=timestamp,
        event_value=value,
        sensor=sensor,
        source=custom_source.name,
    )
    
    db.beliefs.append(belief)

# Function to collect data from sensors
def collect_data(sensor):
    now = datetime.datetime.now(pytz.UTC)
    if "solar_panel" in sensor.name:
        value = max(0, np.sin(now.hour / 24.0 * 2 * np.pi) * 100)
    elif "wind_turbine" in sensor.name:
        value = max(0, np.random.normal(50, 10))
    elif "battery_storage" in sensor.name:
        value = 50
    else:
        value = np.random.uniform(1, 10)  # Placeholder for consumer meters or other types of sensors
    add_reading(sensor, value, now)
    return {"sensor": sensor, "datetime": now, "value": value}

# Simulate data collection
for sensor in [solar_sensor, wind_sensor, grid_sensor, battery_sensor] + consumer_sensors:
    print(collect_data(sensor))

# Print data from the in-memory database
def print_data():
    print("\nGeneric Asset Types:")
    for asset_type in db.generic_asset_types:
        print(f"Name: {asset_type.name}, Description: {asset_type.description}")

    print("\nGeneric Assets:")
    for asset in db.generic_assets:
        print(f"Name: {asset.name}, Type: {asset.generic_asset_type.name}")

    print("\nSensors:")
    for sensor in db.sensors:
        print(f"Name: {sensor.name}, Unit: {sensor.unit}, Asset: {sensor.generic_asset.name}")

    print("\nCustom Sources:")
    for source in db.custom_sources:
        print(f"Name: {source.name}")

    print("\nBeliefs (Sensor Readings):")
    for belief in db.beliefs:
        print(f"Sensor: {belief.sensor.name}, Value: {belief.event_value}, Timestamp: {belief.event_start}, Source: {belief.source.name}")

print_data()
