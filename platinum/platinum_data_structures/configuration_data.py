from binary_reader import BinaryReader


class ConfigData:
    pass


class ConfigDataV8(ConfigData):
    def __init__(self, data_stream: str):
        data_reader = BinaryReader(data_stream)

        self.version = data_reader.read_uint16()
        self.sensor_type = data_reader.read_str(8)

        self.Mode_bit_structure = ModeBitsStructure(data_reader.read_uint16())
        self.sensor_fsd = data_reader.read_float(4)
        self.zero_off = data_reader.read_float(2)
        self.zero_cal_temperature = data_reader.read_float(2)

        self.span_cal_temperature = data_reader.read_float(4)
        self.pos_zero_suppression = data_reader.read_float(2)
        self.neg_zero_suppression = data_reader.read_float(2)

        self.calibration_gas_value = data_reader.read_float(4)
        self.span_offset = data_reader.read_float(4)
        self.el = data_reader.read_float(4)
        self.power = data_reader.read_float(4)
        self.rounding = data_reader.read_float(4)

        self.baud_structure = BaudRateStructure(data_reader.read_uint16())
        self.warmup = data_reader.read_uint16()

        self.temperature_offset = data_reader.read_float()
        self.dac_zero = data_reader.read_float()
        self.dac_fsd = data_reader.read_float()
        self.dac_powerup = data_reader.read_uint16()
        self.slope_biogas = data_reader.read_float()

        self.cross_reference_range1 = data_reader.read_float()
        self.cross_reference_range3 = data_reader.read_float()


class BaudRateStructure:
    baudrate_options = 4800, 9600, 19200, 38400

    def __init__(self, data):
        self.baudrate = self.baudrate_options[data & 0x0003]
        self.is_uart_enabled = (data & 0x0004) > 0
        self.is_manual_calibration_mode_Enabled = (data & 0x0008) > 0


class ModeBitsStructure:
    over_range_limit_options = 200, 150, 125, 100

    def __init__(self, data):
        self.analogue_output = (data & 0x0001) > 0
        self.is_range_one_enabled = (data & 0x0002) > 0
        self.is_range_two_enabled = (data & 0x0004) > 0
        self.is_range_three_enabled = (data & 0x0008) > 0
        self.is_range_four_enabled = (data & 0x0010) > 0

        self.is_span_gas_check_enabled = (data & 0x0100) > 0
        self.is_dac_mon_enabled = (data & 0x0200) > 0
        self.over_range_limit = self.over_range_limit_options[(data >> 10) & 0x0003]
        self.is_det1_reading_format_fsd = (data & 0x1000) > 0
        self.is_det2_reading_format_fsd = (data & 0x2000) > 0
        self.is_live_data_reading_type_int = (data & 0x4000) > 0
        self.calibration_emulation = (data & 0x8000) > 0
