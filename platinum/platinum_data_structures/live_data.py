from binary_reader import BinaryReader


class LiveData:
    pass


class LiveDataV4(LiveData):
    def __init__(self, data_stream: str):
        data_reader = BinaryReader(data_stream)

        self.version = data_reader.read_uint16()
        self.status_flags = data_reader.read_uint16()
        self.reading = data_reader.read_float()
        self.temperature = data_reader.read_float()
        self.det_1 = data_reader.read_uint16()
        self.ref = data_reader.read_uint16()
        self.fa = data_reader.read_float()
        self.uptime = data_reader.read_uint32()
        self.det_min = data_reader.read_uint16()
        self.det_max = data_reader.read_uint16()
        self.ref_min = data_reader.read_uint16()
        self.ref_max = data_reader.read_uint16()
