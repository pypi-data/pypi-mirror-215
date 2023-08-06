from .request import GetSet


def decode_getset(packet):
    gs = GetSet()
    gs.set_answer(packet)
    gs.decode()
    return gs.items()
