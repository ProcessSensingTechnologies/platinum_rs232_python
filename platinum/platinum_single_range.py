from serial import Serial
from platinum.utilities.helpers import (
    VariableIdEnum,
    generate_read_frame,
)
from platinum.platinum_data_structures.live_data import LiveData, LiveDataV4
from platinum.platinum_data_structures.configuration_data import (
    ConfigData,
    ConfigDataV8,
)


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

        try:
            self.config_data = self._read_config_data()
        except StructureVersionException as error:
            self.config_data = None
            print(error)
            print("properties and methods using Configuration Data will not work")

        try:
            self._live_data = self._read_live_data()
        except StructureVersionException as error:
            self._live_data = None
            print(error)
            print("properties and methods using Live Data will not work")

    @property
    def live_data(self):
        if self._live_data:
            return self._read_live_data()

    @property
    def live_data_version(self):
        """
        Return the current version of the "Live Data" Structure

        :return:
        :rtype: float
        """
        if self._live_data:
            return self.live_data.version
        else:
            frame = generate_read_frame(VariableIdEnum.LIVE_DATA)

            self.write(frame)
            self.flushOutput()
            returned_data = self.read_until(b"")

            if b"\x10\x10" in returned_data:
                returned_data = returned_data.replace(b"\x10\x10", b"\x10")

            data_bytes = returned_data[3:-4]

            return data_bytes[0]

    @property
    def config_data_version(self):
        """
        Return the current version of the "Config Data" Structure

        :return:
        :rtype: float
        """
        if self.config_data:
            return self.config_data.version
        else:
            frame = generate_read_frame(VariableIdEnum.CONFIG_DATA)

            self.write(frame)
            self.flushOutput()
            returned_data = self.read_until(b"")

            if b"\x10\x10" in returned_data:
                returned_data = returned_data.replace(b"\x10\x10", b"\x10")

            data_bytes = returned_data[3:-4]

            return data_bytes[0]

    def _read_live_data(self) -> LiveData:
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

        match data_bytes[0]:
            case 4:
                data_structure = LiveDataV4(data_bytes)
            case _:
                raise StructureVersionException(
                    f"Invalid Live Data Structure Version: {data_bytes[0]}"
                )

        return data_structure

    def _read_config_data(self) -> ConfigData:
        """
        Return all 'Confguration Data' fields from the sensor as a dictionary

        :return: Config Data dictionary
        :rtype: dict[str : str | int | BaudRateStructure | ModeBitsStructure]
        """
        frame = generate_read_frame(VariableIdEnum.CONFIG_DATA)

        self.write(frame)
        self.flushOutput()
        returned_data = self.read_until(b"")

        if b"\x10\x10" in returned_data:
            returned_data = returned_data.replace(b"\x10\x10", b"\x10")

        data_bytes = returned_data[3:-4]

        match data_bytes[0]:
            case 8:
                data_structure = ConfigDataV8(data_bytes)
            case _:
                raise StructureVersionException(
                    f"Invalid Config Structure Version: {data_bytes[0]}"
                )

        return data_structure
