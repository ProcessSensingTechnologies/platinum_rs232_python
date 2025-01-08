from platinum.platinum_single_range import PlatinumSingleGas

if __name__ == "__main__":
    sensor = PlatinumSingleGas("COM8")
    print(f"{sensor.config_data.sensor_type = }")
    print(f"{sensor.live_data_version = }")

    while True:
        print(f"{sensor.live_data.reading = }")
