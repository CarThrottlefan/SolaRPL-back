from flexmeasures import Sensor, add_reading
import datetime
import numpy as np
from ripplenet import send_payment

# Define sensors for renewable energy sources
solar_sensor = Sensor(name="solar_panel", unit="kWh", type="electricity", location="solar_farm")
wind_sensor = Sensor(name="wind_turbine", unit="kWh", type="electricity", location="wind_farm")

# Define sensors for constant energy sources
battery_sensor = Sensor(name="battery_storage", unit="kWh", type="electricity", location="battery_plant")

# Define sensors for consumer endpoints
consumer_sensors = [Sensor(name=f"consumer_meter_{i}", unit="kWh", type="electricity", location=f"consumer_home_{i}") for i in range(5)]

# Global variable to track whether consumers have been signaled to reduce consumption
consumers_reducing = False
consumers_increasing = False
reduction_period = 3  # Number of hours consumers reduce their consumption
current_reduction_hours = 0
max_token_reward = 30

# Track initial consumption to compare later
initial_consumption = {sensor.name: 0 for sensor in consumer_sensors}

# Function to simulate collecting data from the sensor
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
        if consumers_reducing:
            value = base_value * 0.5  # Reduce consumption by 50%
        else:
            value = base_value
    reading = {"sensor": sensor, "datetime": now, "value": value}
    add_reading(reading)  # Assuming add_reading function exists in flexmeasures
    return reading


battery_level = 1000  # Initial battery level in kWh
battery_capacity = 2000  # Maximum battery capacity in kWh
battery_threshold = 1800  # Threshold to signal consumers

def manage_battery(consumer_readings):
    global battery_level, consumers_reducing, current_reduction_hours
    net_energy = total_generation - total_consumption
    
    if net_energy > 0:
        # Charge the battery
        battery_level = min(battery_level + net_energy, battery_capacity)
    else:
        # Discharge the battery to meet demand
        battery_level = max(battery_level + net_energy, 0)
    
    # Check if battery level exceeds threshold
    if battery_level >= battery_threshold and not consumers_reducing:
        signal_consumers_to_reduce()

    # Reset consumers' consumption behavior after reduction period
    if consumers_reducing:
        current_reduction_hours += 1
        if current_reduction_hours >= reduction_period:
            check_and_reward_consumers(consumer_readings)
            consumers_reducing = False
            current_reduction_hours = 0

    return battery_level

solar_reading = collect_data(solar_sensor)
wind_reading = collect_data(wind_sensor)
consumer_readings = [collect_data(sensor) for sensor in consumer_sensors]
battery_reading = manage_battery(consumer_readings)
total_generation = solar_reading['value'] + wind_reading['value']
total_consumption = sum([reading['value'] for reading in consumer_readings])

def signal_consumers_to_reduce():
    global consumers_reducing, initial_consumption
    consumers_reducing = True
    print("Battery level is high. Consumers are advised to reduce their power consumption to maintain grid stability.")
    for sensor in consumer_sensors:
        initial_consumption[sensor.name] = collect_data(sensor)['value']

def signal_consumers_to_increase():
    global consumers_increasing, initial_consumption
    consumers_increasing = True
    print(". Consumers are advised to reduce their power consumption to maintain grid stability.")
    for sensor in consumer_sensors:
        initial_consumption[sensor.name] = collect_data(sensor)['value']

def check_and_reward_consumers(consumer_readings, actionName):
    for reading in consumer_readings:
        initial_value = initial_consumption[reading['sensor'].name]
        if actionName == "reduced":
            if initial_value * 0.8 <= reading['value'] < initial_value:  # Check if consumption reduced by max 20%
            # Trigger payment to consumer's wallet
                send_payment(10)  # Adjust amount and address accordingly
                print(f"Reward sent to {reading['sensor'].name} for reducing consumption.")
            elif initial_value * 0.1 <= reading['value'] < initial_value * 0.8:
                reduct_per = reading['value']/initial_value 
                send_payment(1 / reduct_per * max_token_reward)  # Adjust amount and address accordingly
                print(f"Reward sent to {reading['sensor'].name} for reducing consumption.")
        elif actionName == "increased":
            if initial_value * 1.5 <= reading['value'] < initial_value * 1.8:  # Check if consumption increased by 50-79%
            # Trigger payment to consumer's wallet
                reduct_per = reading['value']/initial_value 
                send_payment(reduct_per * max_token_reward)  # Adjust amount and address accordingly
                print(f"Reward sent to {reading['sensor'].name} for reducing consumption.")
            elif initial_value * 1.8 <= reading['value']: # Check if consumption increased by 80%+
                send_payment(10)  # Adjust amount and address accordingly
                print(f"Reward sent to {reading['sensor'].name} for reducing consumption.")
        
        

def balance_load():
    # Log the readings for analysis
    log_readings(solar_reading, wind_reading, consumer_readings, battery_reading)

def log_readings(solar_reading, wind_reading, consumer_readings, battery_reading):
    print(f"Solar: {solar_reading['value']:.2f} kWh, Wind: {wind_reading['value']:.2f} kWh")
    for i, reading in enumerate(consumer_readings):
        print(f"Consumer {i+1}: {reading['value']:.2f} kWh")
    print(f"Battery Level: {battery_reading:.2f} kWh\n")
    
def check_grid_usage():
    curr_capacity_left_per = lambda total_generation, total_consumption: total_consumption / total_generation
    if(curr_capacity_left_per > 1): 
        signal_consumers_to_increase()
        check_and_reward_consumers(consumer_readings, "increased")
    elif(curr_capacity_left_per < 0.2):
        signal_consumers_to_increase()
        check_and_reward_consumers(consumer_readings, "reduced")
    