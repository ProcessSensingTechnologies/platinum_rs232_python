from serial import Serial
from struct import unpack
from platinum.utilities.helpers import VariableIdEnum, generate_read_frame


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
        return self.read_live_data()["Version"]

    @property
    def status_flags(self):
        return self.read_live_data()["StatusFlags"]

    @property
    def sensor_reading(self):
        return self.read_live_data()["ReadingFloat"]

    @property
    def sensor_temperature(self):
        return self.read_live_data()["Temperature"]

    def read_live_data(self) -> dict[str : str | int]:
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

        data_struct = unpack("=HHffHHfLHHHH", data_bytes)

        live_data = {
            "Version": data_struct[0],
            "StatusFlags": data_struct[1],
            "ReadingFloat": round(data_struct[2], 4),
            "Temperature": round(data_struct[3], 4),
            "Det1": data_struct[4],
            "Ref": data_struct[5],
            "Fa": round(data_struct[6], 4),
            "Uptime (s)": data_struct[7] / 100,
            "DetMin": data_struct[8],
            "DetMax": data_struct[9],
            "RefMin": data_struct[10],
            "RefMax": data_struct[11],
        }

        return live_data
