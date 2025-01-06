from platinum.platinum_single_range import PlatinumSingleGas
from time import sleep

if __name__ == "__main__":
    sensor = PlatinumSingleGas("COM8")

    while True:
        print(f"{sensor.sensor_reading = }")
        print(f"{sensor.sensor_temperature = }")
        sleep(1)
