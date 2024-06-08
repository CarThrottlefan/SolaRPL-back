from flexmeasures.data import db
from flexmeasures.data.models.generic_assets import GenericAsset, GenericAssetType
from flexmeasures.data.models.time_series import Sensor
from flexmeasures.data.models.user import User
import datetime
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from timely_beliefs import TimedBelief
from datetime import timedelta

Base = declarative_base()


class CustomSource(Base):
    __tablename__ = 'custom_sources'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


DATABASE_URL = 'postgresql://flexmeasures-user:fm-db-passwd@localhost:5432/flexmeasures-db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


Base.metadata.create_all(engine)
db.metadata.create_all(engine)


solar_type = GenericAssetType(name="solar_panel", description="Solar Panel")
wind_type = GenericAssetType(name="wind_turbine", description="Wind Turbine")
grid_type = GenericAssetType(name="grid", description="Electric Grid")
battery_type = GenericAssetType(name="battery_storage", description="Battery Storage")
consumer_type = GenericAssetType(name="consumer_meter", description="Consumer Meter")


session.add(solar_type)
session.add(wind_type)
session.add(grid_type)
session.add(battery_type)
session.add(consumer_type)
session.commit()


solar_asset = GenericAsset(name="Solar Farm 1", generic_asset_type=solar_type)
wind_asset = GenericAsset(name="Wind Farm 1", generic_asset_type=wind_type)
grid_asset = GenericAsset(name="Main Grid", generic_asset_type=grid_type)
battery_asset = GenericAsset(name="Battery Storage 1", generic_asset_type=battery_type)
consumer_assets = [GenericAsset(name=f"Consumer Home {i}", generic_asset_type=consumer_type) for i in range(5)]


session.add(solar_asset)
session.add(wind_asset)
session.add(grid_asset)
session.add(battery_asset)
for consumer_asset in consumer_assets:
    session.add(consumer_asset)
session.commit()


solar_sensor = Sensor(name="solar_panel_sensor", unit="kWh", generic_asset=solar_asset)
wind_sensor = Sensor(name="wind_turbine_sensor", unit="kWh", generic_asset=wind_asset)
grid_sensor = Sensor(name="grid_sensor", unit="kWh", generic_asset=grid_asset)
battery_sensor = Sensor(name="battery_storage_sensor", unit="kWh", generic_asset=battery_asset)
consumer_sensors = [Sensor(name=f"consumer_meter_{i}", unit="kWh", generic_asset=consumer_assets[i]) for i in range(5)]


session.add(solar_sensor)
session.add(wind_sensor)
session.add(grid_sensor)
session.add(battery_sensor)
for consumer_sensor in consumer_sensors:
    session.add(consumer_sensor)
session.commit()


print(f"Solar Sensor: {solar_sensor}")
print(f"Wind Sensor: {wind_sensor}")
print(f"Grid Sensor: {grid_sensor}")
print(f"Battery Sensor: {battery_sensor}")
for i, consumer_sensor in enumerate(consumer_sensors):
    print(f"Consumer Sensor {i}: {consumer_sensor}")


custom_source = CustomSource(name="Simulation Source")
session.add(custom_source)
session.commit()


def add_reading(sensor, value, timestamp):
    source = session.query(CustomSource).filter(CustomSource.name == "Simulation Source").first()
    source = source.name
    belief = TimedBelief(
        event_start=timestamp,
        event_value=value,
        sensor=sensor,
        source=source,
    )
    session.add(belief)
    session.commit()


def collect_data(sensor):
    now = datetime.datetime.now()
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

# Query and print data from the database
def print_data():
    print("\nGeneric Asset Types:")
    for asset_type in session.query(GenericAssetType).all():
        print(asset_type)

    print("\nGeneric Assets:")
    for asset in session.query(GenericAsset).all():
        print(asset)

    print("\nSensors:")
    for sensor in session.query(Sensor).all():
        print(sensor)

    print("\nCustom Sources:")
    for source in session.query(CustomSource).all():
        print(source)

    print("\nBeliefs (Sensor Readings):")
    for belief in session.query(TimedBelief).all():
        print(f"Sensor: {belief.sensor.name}, Value: {belief.event_value}, Timestamp: {belief.event_start}, Source: {belief.source.name}")
print_data()


