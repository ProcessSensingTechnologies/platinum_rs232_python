from serial import Serial
from utilities.helpers import VariableIdEnum, generate_read_frame
from binary_reader import BinaryReader
from platinum_data_structures.live_data import LiveDataV4


class StructureVersionException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PlatinumSingleGas(Serial):
    """
    Main class for a Single Gas Platinum Sensor

    :param Serial: Child of Serial to use all included methods as standard
    """

    def __init__(self, port_name: str, baudrate: int = 38400):
        """
        Initialiser for Platinum Sensor communication.

        :param port_name: Portname for the connection. Likely "COM*" on windows or "/dev/ttyUSB*" in Linux
        :type port_name: str
        :param baudrate: baudrate setting for sensor communication
        :type baudrate: int
        :default baudrate: 38400
        """
        super().__init__(port_name, baudrate, timeout=1)

    @property
    def live_data_version(self):
        """
        Return the current version of the "Live Data" Structure

        :return:
        :rtype: float
        """
        return self.read_live_data().Version

    @property
    def status_flags(self):
        return self.read_live_data().StatusFlags

    @property
    def sensor_reading(self):
        return self.read_live_data().Reading

    @property
    def sensor_temperature(self):
        return self.read_live_data().Temperature

    def read_live_data(self) -> LiveDataV4:
        """
        Return all 'Live Data' fields from the sensor as a dictionary

        :return: Live Data dictionary
        :rtype: dict[str : str | int]
        """
        frame = generate_read_frame(VariableIdEnum.LIVE_DATA)

        self.write(frame)
        self.flushOutput()
        returned_data = self.read_until(b"")

        if b"\x10\x10" in returned_data:
            returned_data = returned_data.replace(b"\x10\x10", b"\x10")

        data_bytes = returned_data[3:-4]

        if data_bytes[0] != 4:
            raise StructureVersionException(
                f"Invalid Structure Version: {data_bytes[0]}"
            )

        data_structure = LiveDataV4()

        data_reader = BinaryReader(data_bytes)

        data_structure.Version = data_reader.read_uint16()
        data_structure.StatusFlags = data_reader.read_uint16()
        data_structure.Reading = data_reader.read_float()
        data_structure.Temperature = data_reader.read_float()
        data_structure.Det1 = data_reader.read_uint16()
        data_structure.Ref = data_reader.read_uint16()
        data_structure.Fa = data_reader.read_float()
        data_structure.Uptime = data_reader.read_uint32()
        data_structure.DetMin = data_reader.read_uint16()
        data_structure.DetMax = data_reader.read_uint16()
        data_structure.RefMin = data_reader.read_uint16()
        data_structure.RefMax = data_reader.read_uint16()

        return data_structure


if __name__ == "__main__":
    sensor = PlatinumSingleGas("COM8")

    while True:
        print(f"{sensor.sensor_reading = }")
        print(f"{sensor.sensor_temperature = }")
