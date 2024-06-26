import datetime
import numpy as np
from timely_beliefs import TimedBelief
from datetime import timedelta
import pytz
import matplotlib.pyplot as plt 

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
        belief_horizon=timedelta(hours=0)
    )
    
    db.beliefs.append(belief)

consumers_reducing = False
consumers_increasing = False
reduction_period = 3  # Number of hours consumers reduce their consumption
current_reduction_hours = 0
max_token_reward = 30


# Function to collect data from sensors
def collect_data(sensor):
    now = datetime.datetime.now()
    if "solar_panel" in sensor.name:
        value = max(0, np.sin(now.hour / 24.0 * 2 * np.pi) * 100)  # Simulated solar power generation
    elif "wind_turbine" in sensor.name:
        value = max(0, np.random.normal(50, 10))  # Simulated wind power generation
    elif "battery_storage" in sensor.name:
        value = 50  # Placeholder for battery level
    else:
        # Simulated consumer usage, reduced if consumers are signaled to reduce consumption
        base_value = np.random.uniform(1, 10)
        initial_consumption = {"sensor": sensor, "datetime": now, "value": value}
        if consumers_reducing:
            value = base_value * 0.5  # Reduce consumption by 50%
        else:
            value = base_value
    reading = {"sensor": sensor, "datetime": now, "value": value}
    add_reading(reading)  # Assuming add_reading function exists in flexmeasures
    return initial_consumption, reading

start_time = datetime.datetime.now(pytz.UTC)
for hour in range(24):
    current_time = start_time + timedelta(hours=hour)
    for sensor in [solar_sensor, wind_sensor, grid_sensor, battery_sensor] + consumer_sensors:
        collect_data(sensor, current_time)
# Print data from the in-memory database

def extract_data(sensor_name):
    timestamps = []
    values = []
    for belief in db.beliefs:
        if belief.sensor.name == sensor_name:
            timestamps.append(belief.event_start)
            values.append(belief.event_value)
    return timestamps, values

def plot_sensor_data():
    plt.figure(figsize=(12, 8))

    # Plot Solar Panel Data
    timestamps, values = extract_data("solar_panel_sensor")
    plt.plot(timestamps, values, label="Solar Panel", color="orange")

    # Plot Wind Turbine Data
    timestamps, values = extract_data("wind_turbine_sensor")
    plt.plot(timestamps, values, label="Wind Turbine", color="blue")

    # Plot Grid Data
    timestamps, values = extract_data("grid_sensor")
    plt.plot(timestamps, values, label="Grid", color="green")

    # Plot Battery Storage Data
    timestamps, values = extract_data("battery_storage_sensor")
    plt.plot(timestamps, values, label="Battery Storage", color="red")

    # Plot Consumer Data
    for i in range(5):
        timestamps, values = extract_data(f"consumer_meter_{i}")
        plt.plot(timestamps, values, label=f"Consumer {i}", linestyle='--')

    plt.xlabel("Time")
    plt.ylabel("kWh")
    plt.title("Energy Fluctuations Over 24 Hours")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plot_sensor_data()

        
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
