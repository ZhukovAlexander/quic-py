class Alarm:
    """
    Simple alarm implementation

    """

    def __init__(self, loop, on_fired=lambda: None):
        self._callback = on_fired
        self._loop = loop
        self._handler = None

    def set(self, when):
        self._handler = self._loop.call_at(when, self._callback)

    def reset(self):
        self._handler.cancel()
