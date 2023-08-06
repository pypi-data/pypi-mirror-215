from .command import *
from .core import *
from . import command


class Request:
    id = 0
    _tx = Packet(b'', False, 0)

    class RequestItem:
        def __init__(self, request):
            self._rq = request
            self._pos = 0
            self. _limit = min(len(request._cmds), len(request._vals))

        def __iter__(self):
            self._pos = 0
            return self

        def __next__(self):
            if self._pos >= self._limit:
                raise StopIteration
            else:
                res = self._rq._cmds[self._pos], self._rq._vals[self._pos]
                self._pos += 1
                return res

    def __init__(self):
        self._cmds = []
        self._vals = []

    def set_answer(self, data):
        p = Packet(data, 'auto')
        hdr = p.read_byte()
        if hdr != self.id:
            raise SmpException()
        self.ipf = p.read_byte() & 0x40 != 0
        self._rx = p

    def get_request(self):
        return self._tx.data

    def commands(self):
        return self._cmds

    def values(self):
        return self._vals

    def items(self):
        return Request.RequestItem(self)

    def decode(self):
        pass

    def encode(self):
        dff = False
        for cmd in self._cmds:
            if cmd.require_dff(): dff = True
        p = Packet(b'', dff, 0)
        p.write_byte(self.id)
        p.write_byte(0x80 if dff else 0)
        for cmd in self._cmds:
            p.write_param(cmd.code)
            cmd.encode_param(p)


        self._tx = p


class Action(Request):
    id = PERFORM_ACTION
    def add(self, code, value):
        self._cmds.append(CommandAction(code, value))


class GetSet(Request):
    id = GETSET
    _cmd_maker = {
        GET_DATA_SINGLE: command.CommandDataSingle,
        GET_DATA_MULTIPLE: command.CommandDataMultiple,
        GET_OPTION: command.CommandGetOption,
        SET_OPTION: command.CommandSetOption,
        GET_INFO: command.CommandInfo,
        PERFORM_ACTION: command.CommandAction,
        GET_OPTION1: command.CommandGetOption,
        GET_DATA_SINGLE_EX: command.CommandDataSingleEx,
        GET_DATA_MULTIPLE_EX: command.CommandDataMultipleEx,
        }

    def __init__(self):
        super().__init__()

    def decode(self):
        rx = self._rx
        while not rx.eof():
            code_class = rx.read_param()
            while not rx.eof():
                code = rx.read_param()
                if code == 0: # error
                    code = rx.read_param()
                    if code == 0: break # end of code class

                cmd = self._cmd_maker[code_class](code)
                cmd.decode_param(rx)
                if len(self._cmds) <= len(self._vals):
                    self._cmds.append(cmd)
                else:
                    if self._cmds[len(self._vals)] != cmd:
                        raise SmpException()
                self._vals.append(cmd.decode_value(rx))
