import datetime

from . import codes
from .code_types import info, action, option, data_single
from .core import SmpException, pack_bitbuf, unpack_bitbuf
from .types import *
from .value import *


def inspect_code_names():
    res = {
        'SDATA': {},
        'MDATA': {},
        'INFO': {},
        'OPT': {},
        'ACTION': {},
    }

    for name in dir(codes):
        parts = name.split('_')
        if len(parts) > 2 and parts[0] == 'SMP':
            res[parts[1]][getattr(codes, name)] = name

    return res


code_names = inspect_code_names()


class Command:
    type = UNKNOWN
    value = None

    def __init__(self, code):
        self.code = code

    @property
    def name(self):
        return 'SMP_UNKNOWN_CODE'

    @staticmethod
    def make_base_value(type, value):
        typename = type[0]
        if typename == 'NUM':
            res = Value(int(value))
        elif typename == 'INT':
            res = Value(int(value))
        elif typename == 'STRING':
            res = Value(str(value))
        elif typename == 'DATETIME':
            if type(value) is datetime.datetime:
                res = Value(value)
            else:
                raise SmpException()
        elif typename == 'DOUBLE':
            res = Value(float(value))
        elif typename == 'BITBUF':
            res = Value(value)
        else:
            raise SmpException()

        return res

    @staticmethod
    def write_base_value(type, packet, value):
        typename = type[0]
        if typename == 'NUM':
            packet.write_num(value.value)
        elif typename == 'INT':
            packet.write_int(value.value)
        elif typename == 'STRING':
            packet.write_string(value.value)
        elif typename == 'DATETIME':
            packet.write_datetime(value.value)
        elif typename == 'DOUBLE':
            packet.write_num(int(value.value * 10 ** type[1]))
        elif typename == 'BITBUF':
            packet.write_buffer(pack_bitbuf(value.value, type[1]))
        else:
            raise SmpException()

    @staticmethod
    def read_base_value(type, packet):
        typename = type[0]
        if typename == 'NUM':
            res = Value(packet.read_num())
        elif typename == 'INT':
            res = Value(packet.read_int())
        elif typename == 'STRING':
            res = Value(packet.read_string())
        elif typename == 'DATETIME':
            res = Value(packet.read_datetime())
        elif typename == 'DOUBLE':
            res = Value(packet.read_num() / 10 ** type[1])
        elif typename == 'BITBUF':
            res = Value(unpack_bitbuf(packet.read_buffer()[0], type[1]))
        else:
            raise SmpException()

        return res

    def require_dff(self):
        return self.code > 255

    def decode_param(self, packet):
        pass

    def encode_param(self, packet):
        pass

    def decode_value(self, packet):
        pass

    def encode_value(self, packet):
        pass


class CommandAction(Command):
    def __init__(self, code, value):
        super().__init__(code)
        self.type = action.get(code, UNKNOWN)
        self.value = self.make_base_value(self.type, value)

    def code_name(self):
        return code_names['ACTION'].get(self.code, 'SMP_UNKNOWN_CODE')

    def decode_value(self, packet):
        pass

    def encode_param(self, packet):
        self.write_base_value(self.type, packet, self.value)


class CommandInfo(Command):
    def __init__(self, code):
        super().__init__(code)
        self.type = info.get(code, UNKNOWN)

    def __eq__(self, other):
        return type(self) == type(other) and self.code == other.code

    @property
    def name(self):
        return code_names['INFO'].get(self.code, 'SMP_UNKNOWN_CODE')

    def decode_value(self, packet):
        return self.read_base_value(self.type, packet)


class CommandGetOption(Command):
    def __init__(self, code):
        super().__init__(code)
        self.type = option.get(code, UNKNOWN)

    def __eq__(self, other):
        return type(self) == type(other) and self.code == other.code

    @property
    def name(self):
        return code_names['OPT'].get(self.code, 'SMP_UNKNOWN_CODE')

    def decode_value(self, packet):
        return self.read_base_value(self.type, packet)


class CommandSetOption(Command):
    def __init__(self, code, value):
        super().__init__(code)
        self.type = option.get(code, UNKNOWN)
        self.value = self.make_base_value(self.type, value)

    def code_name(self):
        return code_names['OPT'].get(self.code, 'SMP_UNKNOWN_CODE')

    def decode_value(self, packet):
        pass

    def encode_param(self, packet):
        self.write_base_value(self.type, packet, self.value)


class CommandDataSingle(Command):
    def __init__(self, code, mask = 0):
        super().__init__(code)
        self.type = data_single.get(code, UNKNOWN)
        self.mask = mask

    def __eq__(self, other):
        return type(self) == type(other) and self.code == other.code and self.mask == other.mask

    @property
    def name(self):
        return code_names['SDATA'].get(self.code, 'SMP_UNKNOWN_CODE')

    @property
    def has_mask(self):
        self.type[0] == 'MASK'

    def decode_value(self, packet):
        if self.has_mask:
            raise SmpException()
        else:
            return self.read_base_value(self.type, packet)

    def decode_param(self, packet):
        pass

    def encode_param(self, packet):
        pass


class CommandDataMultiple(Command):
    def __init__(self, code, mask = 0, start = 0, end = 0):
        super().__init__(code)

    @property
    def name(self):
        return code_names['MDATA'].get(self.code, 'SMP_UNKNOWN_CODE')


class CommandDataSingleEx(Command):
    def __init__(self, code, mask = 0, start = 0, end = 0):
        super().__init__(code)


class CommandDataMultipleEx(Command):
    def __init__(self, code, mask = 0, start = 0, end = 0):
        super().__init__(code)
