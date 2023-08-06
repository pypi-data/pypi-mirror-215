import math
from dataclasses import dataclass
from typing import List, Optional, Union
from iqrfpy.utils.sensor_constants import SensorDataSize, SensorTypes, SensorFrcCommands, SensorFrcErrors
from iqrfpy.utils.common import Common


@dataclass
class SensorData:
    sensor_type: SensorTypes
    index: int
    name: str
    short_name: str
    unit: str
    decimal_places: int
    frc_commands: List[int]
    value: Union[int, float, List[int], SensorFrcErrors, None]

    def __init__(self, sensor_type: SensorTypes, index: Union[int, None], name: Union[str, None],
                 short_name: Union[str, None], unit: Union[str, None], decimal_places: Union[int, None],
                 frc_commands: List[int], value: Optional[Union[int, float, List[int]]] = None):
        self.sensor_type = sensor_type
        self.index = index
        self.name = name
        self.short_name = short_name
        self.unit = unit
        self.decimal_places = decimal_places
        self.frc_commands = frc_commands
        self.value = value


@dataclass
class Temperature:
    type = SensorTypes.TEMPERATURE
    name = 'Temperature'
    short_name = 't'
    unit = '˚C'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE,
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class CarbonDioxide:
    type = SensorTypes.CARBON_DIOXIDE
    name = 'Carbon dioxide'
    short_name = 'CO2'
    unit = 'ppm'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE,
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class VolatileOrganicCompound:
    type = SensorTypes.VOLATILE_ORGANIC_COMPOUND
    name = 'Volatile organic compound'
    short_name = 'VOC'
    unit = 'ppm'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE,
        SensorFrcCommands.FRC_2BYTES
    ]


class ExtraLowVoltage:
    type = SensorTypes.EXTRA_LOW_VOLTAGE
    name = 'Extra-low voltage'
    short_name = 'U'
    unit = 'V'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class EarthsMagneticField:
    type = SensorTypes.EARTHS_MAGNETIC_FIELD
    name = "Earth's magnetic field"
    short_name = 'B'
    unit = 'T'
    decimal_places = 7
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class LowVoltage:
    type = SensorTypes.LOW_VOLTAGE
    name = 'Low voltage'
    short_name = 'U'
    unit = 'V'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Current:
    type = SensorTypes.CURRENT
    name = 'Current'
    short_name = 'I'
    unit = 'A'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Power:
    type = SensorTypes.POWER
    name = 'Power'
    short_name = 'E'
    unit = 'W'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class MainsFrequency:
    type = SensorTypes.MAINS_FREQUENCY
    name = 'Mains frequency'
    short_name = 'f'
    unit = 'Hz'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class TimeSpan:
    type = SensorTypes.TIME_SPAN
    name = 'Timespan',
    short_name = 't'
    unit = 's'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Illuminance:
    type = SensorTypes.ILLUMINANCE
    name = 'Illuminance'
    short_name = 'Ev'
    unit = 'lx'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class NitrogenDioxide:
    type = SensorTypes.NITROGEN_DIOXIDE
    name = 'Nitrogen dioxide'
    short_name = 'NO2'
    unit = 'ppm'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class SulfurDioxide:
    type = SensorTypes.SULFUR_DIOXIDE
    name = 'Sulfur dioxide'
    short_name = 'SO2'
    unit = 'ppm'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class CarbonMonoxide:
    type = SensorTypes.CARBON_MONOXIDE
    name = 'Carbon monoxide'
    short_name = 'CO'
    unit = 'ppm'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Ozone:
    type = SensorTypes.OZONE
    name = 'Ozone'
    short_name = 'O3'
    unit = 'ppm'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class AtmosphericPressure:
    type = SensorTypes.ATMOSPHERIC_PRESSURE
    name = 'Atmospheric pressure'
    short_name = 'p'
    unit = 'hPa'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class ColorTemperature:
    type = SensorTypes.COLOR_TEMPERATURE
    name = 'Color temperature'
    short_name = 'Tc'
    unit = 'K'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class ParticulatesPM25:
    type = SensorTypes.PARTICULATES_PM2_5
    name = 'Particulates PM2.5'
    short_name = 'PM2.5'
    unit = 'µg/m3'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class SoundPressureLevel:
    type = SensorTypes.SOUND_PRESSURE_LEVEL
    name = 'Sound pressure level'
    short_name = 'Lp'
    unit = 'dB'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Altitude:
    type = SensorTypes.ALTITUDE
    name = 'Altitude'
    short_name = 'h'
    unit = 'm'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Acceleration:
    types = SensorTypes.ACCELERATION
    name = 'Acceleration'
    short_name = 'a'
    unit = 'm/s2'
    decimal_places = 8
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Ammonia:
    types = SensorTypes.AMMONIA
    name = 'Ammonia'
    short_name = 'NH3'
    unit = 'ppm'
    decimal_places = 1
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Methane:
    type = SensorTypes.METHANE
    name = 'Methane'
    short_name = 'CH4'
    unit = '%'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class ShortLength:
    type = SensorTypes.SHORT_LENGTH
    name = 'Short length'
    short_length = 'l'
    unit = 'm'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class ParticulatesPM1:
    type = SensorTypes.PARTICULATES_PM1
    name = 'Particulates PM1'
    short_name = 'PM1'
    unit = 'µg/m3'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class ParticulatesPM4:
    type = SensorTypes.PARTICULATES_PM4
    name = 'Particulates PM4'
    short_name = 'PM4'
    unit = 'µg/m3'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class ParticulatesPM10:
    type = SensorTypes.PARTICULATES_PM10
    name = 'Particulates PM10'
    short_name = 'PM10'
    unit = 'µg/m3'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class TotalVolatileOrganicCompound:
    type = SensorTypes.TOTAL_VOLATILE_ORGANIC_COMPOUND
    name = 'Total volatile organic compound'
    short_name = 'TVOC'
    unit = 'µg/m3'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class NitrogenOxides:
    type = SensorTypes.NITROGEN_OXIDES
    name = 'Nitrogen oxides'
    short_name = 'NOX'
    unit = ''
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class RelativeHumidity:
    type = SensorTypes.RELATIVE_HUMIDITY
    name = 'Relative humidity'
    short_name = 'RH'
    unit = '%'
    decimal_places = 1
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


class BinaryData7:
    type = SensorTypes.BINARY_DATA7
    name = 'Binary data7'
    short_name = 'bin7'
    unit = ''
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


class PowerFactor:
    type = SensorTypes.POWER_FACTOR
    name = 'Power factor'
    short_name = 'cos θ'
    unit = ''
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


class UVIndex:
    type = SensorTypes.UV_INDEX
    name = 'UV index'
    short_name = 'UV'
    unit = ''
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


class PH:
    type = SensorTypes.PH
    name = 'pH'
    short_name = 'pH'
    unit = ''
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


class RSSI:
    type = SensorTypes.RSSI
    name = 'RSSI'
    short_name = 'RSSI'
    unit = 'dBm'
    decimal_places = 1
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


class BinaryData30:
    type = SensorTypes.BINARY_DATA30
    name = 'Binary data30'
    short_name = 'bin30'
    unit = ''
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES,
        SensorFrcCommands.FRC_4BYTES
    ]


class Consumption:
    type = SensorTypes.CONSUMPTION
    name = 'Consumption'
    short_name = 'E'
    unit = 'Wh'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


class Datetime:
    type = SensorTypes.DATETIME
    name = 'DateTime'
    short_name = 'DateTime'
    unit = ''
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


class TimeSpanLong:
    type = SensorTypes.TIME_SPAN_LONG
    name = 'Timespan long'
    short_name = 't'
    unit = 's'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


class Latitude:
    type = SensorTypes.LATITUDE
    name = 'Latitude'
    short_name = 'LAT'
    unit = '°'
    decimal_places = 7
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


class Longitude:
    type = SensorTypes.LONGITUDE
    name = 'Longitude'
    short_name = 'LONG'
    unit = '°'
    decimal_places = 7
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


class DataBlock:
    type = SensorTypes.DATA_BLOCK
    name = 'Data block'
    short_name = 'datablock'
    unit = ''
    decimal_places = 0
    frc_commands = []


class SensorParser:
    _type_classes = {
        SensorTypes.TEMPERATURE: Temperature,
        SensorTypes.CARBON_DIOXIDE: CarbonDioxide,
        SensorTypes.VOLATILE_ORGANIC_COMPOUND: VolatileOrganicCompound,
        SensorTypes.EXTRA_LOW_VOLTAGE: ExtraLowVoltage,
        SensorTypes.EARTHS_MAGNETIC_FIELD: EarthsMagneticField,
        SensorTypes.LOW_VOLTAGE: LowVoltage,
        SensorTypes.CURRENT: Current,
        SensorTypes.POWER: Power,
        SensorTypes.MAINS_FREQUENCY: MainsFrequency,
        SensorTypes.TIME_SPAN: TimeSpan,
        SensorTypes.ILLUMINANCE: Illuminance,
        SensorTypes.NITROGEN_DIOXIDE: NitrogenDioxide,
        SensorTypes.SULFUR_DIOXIDE: SulfurDioxide,
        SensorTypes.CARBON_MONOXIDE: CarbonMonoxide,
        SensorTypes.OZONE: Ozone,
        SensorTypes.ATMOSPHERIC_PRESSURE: AtmosphericPressure,
        SensorTypes.COLOR_TEMPERATURE: ColorTemperature,
        SensorTypes.PARTICULATES_PM2_5: ParticulatesPM25,
        SensorTypes.SOUND_PRESSURE_LEVEL: SoundPressureLevel,
        SensorTypes.ALTITUDE: Altitude,
        SensorTypes.ACCELERATION: Acceleration,
        SensorTypes.AMMONIA: Ammonia,
        SensorTypes.METHANE: Methane,
        SensorTypes.SHORT_LENGTH: ShortLength,
        SensorTypes.PARTICULATES_PM1: ParticulatesPM1,
        SensorTypes.PARTICULATES_PM4: ParticulatesPM4,
        SensorTypes.PARTICULATES_PM10: ParticulatesPM10,
        SensorTypes.TOTAL_VOLATILE_ORGANIC_COMPOUND: TotalVolatileOrganicCompound,
        SensorTypes.NITROGEN_OXIDES: NitrogenOxides,
        SensorTypes.RELATIVE_HUMIDITY: RelativeHumidity,
        SensorTypes.BINARY_DATA7: BinaryData7,
        SensorTypes.POWER_FACTOR: PowerFactor,
        SensorTypes.UV_INDEX: UVIndex,
        SensorTypes.PH: PH,
        SensorTypes.RSSI: RSSI,
        SensorTypes.BINARY_DATA30: BinaryData30,
        SensorTypes.CONSUMPTION: Consumption,
        SensorTypes.DATETIME: Datetime,
        SensorTypes.TIME_SPAN_LONG: TimeSpanLong,
        SensorTypes.LATITUDE: Latitude,
        SensorTypes.LONGITUDE: Longitude,
        SensorTypes.DATA_BLOCK: DataBlock,
    }

    @classmethod
    def get_sensor_class(cls, sensor_type: Union[SensorTypes, int]):
        if not SensorTypes.has_value(sensor_type):
            raise ValueError(f'Unknown or unsupported sensor type: {sensor_type}')
        if sensor_type not in cls._type_classes:
            raise ValueError(f'Data unavailable for sensor type: {sensor_type}')
        return cls._type_classes[sensor_type]

    @staticmethod
    def _data_len_from_type(sensor_type: int):
        if SensorDataSize.DATA_1BYTE_MIN <= sensor_type <= SensorDataSize.DATA_1BYTE_MAX:
            return 1
        elif SensorDataSize.DATA_2BYTES_MIN <= sensor_type <= SensorDataSize.DATA_2BYTES_MAX:
            return 2
        elif SensorDataSize.DATA_4BYTES_MIN <= sensor_type <= SensorDataSize.DATA_4BYTES_MAX:
            return 4
        else:
            raise ValueError('Unsupported sensor type.')

    @staticmethod
    def _data_len_from_frc_command(frc_command: int):
        if frc_command == SensorFrcCommands.FRC_2BITS:
            return 0.25
        if frc_command == SensorFrcCommands.FRC_1BYTE:
            return 1
        if frc_command == SensorFrcCommands.FRC_2BYTES:
            return 2
        if frc_command == SensorFrcCommands.FRC_4BYTES:
            return 4
        else:
            raise ValueError('Unsupported frc command')

    @classmethod
    def enumerate_from_dpa(cls, dpa: List[int]) -> List[SensorData]:
        sensor_data = []
        for i in range(len(dpa)):
            sensor_type_value = dpa[i]
            if not SensorTypes.has_value(sensor_type_value):
                raise ValueError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type_value)
            sensor_class = cls._type_classes[sensor_type]
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=len(sensor_data),
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands
                )
            )
        return sensor_data

    @classmethod
    def enumerate_from_json(cls, json: List[dict]) -> List[SensorData]:
        sensor_data = []
        for i in range(len(json)):
            data = json[i]
            sensor_type_value = data['type']
            if not SensorTypes.has_value(sensor_type_value):
                raise ValueError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type_value)
            sensor_class = cls._type_classes[sensor_type]
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=len(sensor_data),
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands
                )
            )
        return sensor_data

    @classmethod
    def read_sensors_dpa(cls, sensor_types: List[int], dpa: List[int]) -> List[SensorData]:
        sensor_data = []
        data_index = 0
        sensor_index = 0
        while data_index < len(dpa):
            if sensor_index >= len(sensor_types):
                raise ValueError('Too little sensor types provided for the amount of sensor data.')
            sensor_type_value = sensor_types[sensor_index]
            if not SensorTypes.has_value(sensor_type_value):
                raise ValueError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type_value)
            if sensor_type == SensorTypes.DATA_BLOCK:
                data_len = dpa[data_index]
                if (data_index + data_len) >= len(dpa):
                    raise ValueError('Data length longer than actual data.')
            else:
                data_len = cls._data_len_from_type(sensor_type)
                if (data_index + data_len) > len(dpa):
                    raise ValueError('Data length longer than actual data.')
            sensor_data.extend([sensor_type_value] + dpa[data_index:data_index + data_len])
            data_index += data_len
            sensor_index += 1
        return cls.read_sensors_with_types_from_dpa(sensor_data)

    @classmethod
    def read_sensors_with_types_from_dpa(cls, dpa: List[int]) -> List[SensorData]:
        sensor_data = []
        index = 0
        while index < len(dpa):
            sensor_type_value = dpa[index]
            if not SensorTypes.has_value(sensor_type_value):
                raise ValueError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type_value)
            if sensor_type == SensorTypes.DATA_BLOCK:
                data_length = dpa[index + 1]
                if (index + 1 + data_length) >= len(dpa):
                    raise ValueError('Data length longer than actual data.')
                data = dpa[index + 2:index + 2 + data_length]
            else:
                data_length = cls._data_len_from_type(sensor_type)
                if (index + data_length) >= len(dpa):
                    raise ValueError('Data length longer than actual data.')
                data = cls.convert(sensor_type, dpa[index + 1:index + 1 + data_length])
            sensor_class = cls._type_classes[sensor_type]
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=len(sensor_data),
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands,
                    value=data
                )
            )
            index += (data_length + 1)
        return sensor_data

    @classmethod
    def read_sensors_with_types_from_json(cls, json: List[dict]) -> List[SensorData]:
        sensor_data = []
        for i in range(len(json)):
            data = json[i]
            sensor_type_value = data['type']
            if not SensorTypes.has_value(sensor_type_value):
                raise ValueError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type_value)
            sensor_class = cls._type_classes[sensor_type]
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=len(sensor_data),
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands,
                    value=data['value']
                )
            )
        return sensor_data

    @classmethod
    def frc_dpa(cls, sensor_type: Union[SensorTypes, int], sensor_index: int, frc_command: int, data: List[int],
                extra_result: List[int] = [], count: Union[int, None] = None):
        if isinstance(sensor_type, int):
            if not SensorTypes.has_value(sensor_type):
                raise ValueError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type)
        sensor_class = cls._type_classes[sensor_type]
        dpa = data
        if frc_command == SensorFrcCommands.FRC_1BYTE:
            dpa = data[1:]
        elif frc_command == SensorFrcCommands.FRC_2BYTES:
            dpa = data[2:]
        elif frc_command == SensorFrcCommands.FRC_4BYTES:
            dpa = data[4:]
        if extra_result is not None:
            dpa.extend(extra_result)
        data_len = cls._data_len_from_frc_command(frc_command=frc_command)
        if count is None:
            if frc_command != SensorFrcCommands.FRC_2BITS and len(dpa) % data_len != 0:
                raise ValueError('Invalid length of combined frc data and extra result data.')
        else:
            if frc_command != SensorFrcCommands.FRC_2BITS:
                if len(dpa) < count * data_len:
                    raise ValueError(f'Combined length of frc data and extra result is less than length of data'
                                     f'required to process {count} devices.')
                dpa = dpa[:count * data_len]
        if data_len == 0.25:
            itr = count + 1 if count is not None else 240
            frc_values = []
            for i in range(1, itr):
                mask = 1 << (i % 8)
                idx = math.floor(i / 8)
                if (idx + 32) >= len(dpa):
                    raise ValueError('Combined length of frc data and extra result is too short.')
                val = 0
                if (dpa[idx] & mask) != 0:
                    val = 1
                if (dpa[idx + 32] & mask) != 0:
                    val |= 2
                frc_values.append(val)
        elif data_len == 1:
            frc_values = [x for x in dpa]
        elif data_len == 2:
            frc_values = [(dpa[i + 1] << 8) + dpa[i] for i in range(0, len(dpa), 2)]
        else:
            frc_values = [(dpa[i + 3] << 24) + (dpa[i + 2] << 16) + (dpa[i + 1] << 8) + dpa[i] for i in range(0, len(dpa), 4)]
        sensor_data = []
        for frc_value in frc_values:
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=sensor_index,
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands,
                    value=cls.frc_convert(sensor_type, frc_command, frc_value) if sensor_type != SensorTypes.DATA_BLOCK else frc_values
                )
            )
        return sensor_data

    @staticmethod
    def convert(sensor_type: int, values: List[int]):
        match sensor_type:
            case SensorTypes.TEMPERATURE | SensorTypes.LOW_VOLTAGE:
                sensor_value = values[0] + (values[1] << 8)
                return (Common.word_complement(sensor_value) / 16.0) if sensor_value != 0x8000 else None
            case SensorTypes.ATMOSPHERIC_PRESSURE:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 16.0) if sensor_value != 0xFFFF else None
            case SensorTypes.CARBON_DIOXIDE | SensorTypes.VOLATILE_ORGANIC_COMPOUND | SensorTypes.COLOR_TEMPERATURE:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value if sensor_value != 0x8000 else None
            case SensorTypes.TIME_SPAN | SensorTypes.ILLUMINANCE | SensorTypes.TOTAL_VOLATILE_ORGANIC_COMPOUND | \
                    SensorTypes.NITROGEN_OXIDES:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value if sensor_value != 0xFFFF else None
            case SensorTypes.EXTRA_LOW_VOLTAGE | SensorTypes.CURRENT:
                sensor_value = values[0] + (values[1] << 8)
                return (Common.word_complement(sensor_value) / 1000.0) if sensor_value != 0x8000 else None
            case SensorTypes.MAINS_FREQUENCY | SensorTypes.NITROGEN_DIOXIDE | SensorTypes.SULFUR_DIOXIDE | \
                    SensorTypes.METHANE | SensorTypes.SHORT_LENGTH:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 1000.0) if sensor_value != 0xFFFF else None
            case SensorTypes.EARTHS_MAGNETIC_FIELD:
                sensor_value = values[0] + (values[1] << 8)
                return (Common.word_complement(sensor_value) / 10000000.0) if sensor_value != 0x8000 else None
            case SensorTypes.POWER:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 4.0) if sensor_value != 0xFFFF else None
            case SensorTypes.CARBON_MONOXIDE:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 100.0) if sensor_value != 0xFFFF else None
            case SensorTypes.OZONE:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 10000.0) if sensor_value != 0xFFFF else None
            case SensorTypes.PARTICULATES_PM2_5 | SensorTypes.PARTICULATES_PM1 | SensorTypes.PARTICULATES_PM4 | \
                    SensorTypes.PARTICULATES_PM10:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 4.0) if sensor_value != 0x8000 else None
            case SensorTypes.SOUND_PRESSURE_LEVEL:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 16.0) if sensor_value != 0x8000 else None
            case SensorTypes.ALTITUDE:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 4.0 - 1024) if sensor_value != 0xFFFF else None
            case SensorTypes.ACCELERATION:
                sensor_value = values[0] + (values[1] << 8)
                return (Common.word_complement(sensor_value) / 256.0) if sensor_value != 0x8000 else None
            case SensorTypes.AMMONIA:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 10.0) if sensor_value != 0xFFFF else None
            case SensorTypes.RELATIVE_HUMIDITY:
                return (values[0] / 2.0) if values[0] != 0xEE else None
            case SensorTypes.BINARY_DATA7:
                aux = values[0] & 0x80
                return values[0] if aux == 0 else None
            case SensorTypes.POWER_FACTOR:
                return (values[0] / 200.0) if values[0] != 0xEE else None
            case SensorTypes.UV_INDEX:
                return (values[0] / 8.0) if values[0] != 0xFF else None
            case SensorTypes.PH:
                return (values[0] / 16.0) if values[0] != 0xFF else None
            case SensorTypes.RSSI:
                return ((values[0] - 254) / 2.0) if values[0] != 0xFF else None
            case SensorTypes.BINARY_DATA30:
                sensor_value = values[0] + (values[1] << 8) + (values[2] << 16) + (values[3] << 24)
                return sensor_value if (values[3] & 0x80) == 0 else None
            case SensorTypes.CONSUMPTION | SensorTypes.DATETIME:
                sensor_value = values[0] + (values[1] << 8) + (values[2] << 16) + (values[3] << 24)
                return sensor_value if sensor_value != 0xFFFFFFFF else None
            case SensorTypes.TIME_SPAN_LONG:
                sensor_value = values[0] + (values[1] << 8) + (values[2] << 16) + (values[3] << 24)
                return (sensor_value / 16.0) if sensor_value != 0xFFFFFFFF else None
            case SensorTypes.LATITUDE | SensorTypes.LONGITUDE:
                if values[0] == 0xFF or (values[2] & 0x40) == 0:
                    return None
                sensor_value = values[3] + ((values[2] & 0x3F) + (values[0] + (values[1] << 8)) / 10000) / 60
                if (values[2] & 0x80) != 0:
                    sensor_value = -sensor_value
                return sensor_value
            case SensorTypes.DATETIME:
                length = values[0]
                return values[1:1 + length]
            case _:
                return None

    @staticmethod
    def frc_convert(sensor_type: int, frc_command: int, frc_value: int):
        value = None
        if frc_command == SensorFrcCommands.FRC_2BITS:
            if 0 <= frc_value <= 1:
                return SensorFrcErrors(frc_value)
        else:
            if 0 <= frc_value <= 3:
                return SensorFrcErrors(frc_value)
        match sensor_type:
            case SensorTypes.TEMPERATURE:
                if frc_command == SensorFrcCommands.FRC_1BYTE:
                    value = (Common.byte_complement(frc_value) / 2.0) - 22
                elif frc_command == SensorFrcCommands.FRC_2BYTES:
                    value = Common.word_complement(frc_value ^ 0x8000) / 16.0
            case SensorTypes.LOW_VOLTAGE:
                value = Common.word_complement(frc_value ^ 0x8000) / 16.0
            case SensorTypes.ATMOSPHERIC_PRESSURE | SensorTypes.SOUND_PRESSURE_LEVEL | SensorTypes.TIME_SPAN_LONG:
                value = (frc_value - 4) / 16.0
            case SensorTypes.CARBON_DIOXIDE | SensorTypes.VOLATILE_ORGANIC_COMPOUND:
                if frc_command == SensorFrcCommands.FRC_1BYTE:
                    value = (frc_value - 4) * 16
                elif frc_command == SensorFrcCommands.FRC_2BYTES:
                    value = frc_value - 4
            case SensorTypes.COLOR_TEMPERATURE | SensorTypes.TIME_SPAN | SensorTypes.ILLUMINANCE | \
                    SensorTypes.CONSUMPTION | SensorTypes.DATETIME | SensorTypes.TOTAL_VOLATILE_ORGANIC_COMPOUND | \
                    SensorTypes.NITROGEN_OXIDES:
                value = frc_value - 4
            case SensorTypes.EXTRA_LOW_VOLTAGE | SensorTypes.CURRENT:
                value = Common.word_complement(frc_value ^ 0x8000) / 1000.0
            case SensorTypes.EARTHS_MAGNETIC_FIELD:
                value = Common.word_complement(frc_value ^ 0x8000) / 10000000.0
            case SensorTypes.POWER | SensorTypes.PARTICULATES_PM1 | SensorTypes.PARTICULATES_PM2_5 | \
                    SensorTypes.PARTICULATES_PM4 | SensorTypes.PARTICULATES_PM10:
                value = (frc_value - 4) / 4.0
            case SensorTypes.CARBON_MONOXIDE:
                value = (frc_value - 4) / 100.0
            case SensorTypes.OZONE:
                value = (frc_value - 4) / 10000.0
            case SensorTypes.ALTITUDE:
                value = (Common.word_complement(frc_value ^ 0x8000) / 4.0) - 1024
            case SensorTypes.ACCELERATION:
                value = (Common.word_complement(frc_value) - 4) / 256.0
            case SensorTypes.AMMONIA:
                value = (frc_value - 4) / 10.0
            case SensorTypes.RELATIVE_HUMIDITY:
                value = (frc_value - 4) / 2.0
            case SensorTypes.BINARY_DATA7:
                if frc_command == SensorFrcCommands.FRC_2BITS:
                    value = frc_value & 0x01
                elif frc_command == SensorFrcCommands.FRC_1BYTE:
                    value = frc_value - 4
            case SensorTypes.POWER_FACTOR:
                value = (frc_value - 4) / 200.0
            case SensorTypes.UV_INDEX:
                value = (frc_value - 4) / 8.0
            case SensorTypes.PH:
                value = (frc_value - 4) / 16.0
            case SensorTypes.RSSI:
                value = (frc_value - 258) / 2.0
            case SensorTypes.BINARY_DATA30:
                if frc_command == SensorFrcCommands.FRC_2BYTES or frc_command == SensorFrcCommands.FRC_4BYTES:
                    value = frc_value - 4
            case SensorTypes.LATITUDE | SensorTypes.LONGITUDE:
                value = frc_value
        return value
