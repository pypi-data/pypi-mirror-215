class ValueError(Exception):
    pass


class Value:
    _error = None
    _value = None

    def __init__(self, value = None):
        self._value = value

    @property
    def error(self):
        return self._error

    @property
    def value(self):
        if self._error is not None:
            raise ValueError()
        return self._value
