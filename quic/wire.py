
import sys


class Frame:
    """"""

    def __init__(self, locals_):
        locals_.pop('self')
        for name, val in locals_.items():
            setattr(self, name, val)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @classmethod
    def from_bytes(self, bytedata):

        type_byte = bytedata[0]

        if type_byte >= 128:
            return StreamFrame.from_bytes(bytedata)
        if type_byte >= 64:
            return AckFrame.from_bytes(bytedata)
        if type_byte >= 32:
            return CongestionFeedbackFrame.from_bytes(bytedata)

        switch = {
            PaddingFrame.TYPE_BYTE[0]: PaddingFrame,
            ResetStreamFrame.TYPE_BYTE[0]: ResetStreamFrame,
            ConnectionCloseFrame.TYPE_BYTE[0]: ConnectionCloseFrame,
            GoAwayFrame.TYPE_BYTE[0]: GoAwayFrame,
            MaxDataFrame.TYPE_BYTE[0]: MaxDataFrame,
            MaxStreamDataFrame.TYPE_BYTE[0]: MaxStreamDataFrame,
            MaxStreamIDFrame.TYPE_BYTE[0]: MaxStreamIDFrame,
            PingFrame.TYPE_BYTE[0]: PingFrame,
            BlockedFrame.TYPE_BYTE[0]: BlockedFrame,
            StreamBlockedFrame.TYPE_BYTE[0]: StreamBlockedFrame,
            StreamIDNeededFrame.TYPE_BYTE[0]: StreamIDNeededFrame,
            NewConnectionIDFrame.TYPE_BYTE[0]: NewConnectionIDFrame
        }

        try:
            return switch[type_byte].from_bytes(bytedata)
        except KeyError:
            raise Exception('Invalid frame type')


class RegularFrame(Frame):
    """"""

    TYPE_BYTE = b'\x00'

    def to_bytes(self):
        return self.TYPE_BYTE

    @classmethod
    def from_byte(cls, bytedata):
        return cls()


class PaddingFrame(RegularFrame):
    """"""
    TYPE_BYTE = b'\x00'


class ResetStreamFrame(Frame):
    """"""
    TYPE_BYTE = b'\x01'

    def __init__(self, stream_id, offset, error):
        self.stream_id = stream_id
        self.offset = offset
        self.error = error

    @classmethod
    def from_bytes(cls, bytedata):
        return cls(int.from_bytes(bytedata[1:4], sys.byteorder),
                   int.from_bytes(bytedata[5:12], sys.byteorder),
                   int.from_bytes(bytedata[13:16], sys.byteorder))

    def to_bytes(self):
        return (self.TYPE_BYTE +
                self.stream_id.to_bytes(4, sys.byteorder) +
                self.offset.to_bytes(8, sys.byteorder) +
                self.error.to_bytes(4, sys.byteorder))


class ConnectionCloseFrame(Frame):
    """"""
    TYPE_BYTE = b'\x02'


class GoAwayFrame(Frame):
    """"""
    TYPE_BYTE = b'\x03'


class MaxDataFrame(Frame):

    TYPE_BYTE = b'\x04'

    def __init__(self, max_data):
        super().__init__(locals())

    @classmethod
    def from_bytes(cls, bytedata):
        return cls(int.from_bytes(bytedata[1:4], sys.byteorder))

    def to_bytes(self):
        return self.TYPE_BYTE + self.max_data.to_bytes(4, sys.byteorder)


class MaxStreamDataFrame(Frame):
    """"""
    TYPE_BYTE = b'\x05'

    def __init__(self, stream_id, offset):
        self.stream_id = stream_id
        self.offset = offset

    @classmethod
    def from_bytes(cls, bytedata):
        return cls(int.from_bytes(bytedata[1:4], sys.byteorder),
                   int.from_bytes(bytedata[5:12], sys.byteorder))

    def to_bytes(self):
        return (self.TYPE_BYTE +
                self.stream_id.to_bytes(4, sys.byteorder) +
                self.offset.to_bytes(8, sys.byteorder))


class MaxStreamIDFrame(Frame):
    """"""
    TYPE_BYTE = b'\x06'

    def __init__(self, max_stream_id):
        super().__init__(locals())

    @classmethod
    def from_bytes(cls, bytedata):
        return cls(int.from_bytes(bytedata[1:4], sys.byteorder))

    def to_bytes(self):
        return self.TYPE_BYTE + self.max_stream_id.to_bytes(4, sys.byteorder)


class PingFrame(RegularFrame):
    """"""
    TYPE_BYTE = b'\x07'


class BlockedFrame(Frame):
    """"""
    TYPE_BYTE = b'\x08'

    def __init__(self, stream_id):
        self.stream_id = stream_id

    @classmethod
    def from_bytes(cls, bytedata):
        return cls(int.from_bytes(bytedata[1:4], sys.byteorder))

    def to_bytes(self):
        return self.TYPE_BYTE + self.stream_id.to_bytes(4, sys.byteorder)


class StreamBlockedFrame(Frame):
    """"""
    TYPE_BYTE = b'\x09'

    def __init__(self, stream_id):
        super().__init__(locals())

    @classmethod
    def from_bytes(cls, bytedata):
        return cls(int.from_bytes(bytedata[1:4], sys.byteorder))

    def to_bytes(self):
        return self.TYPE_BYTE + self.stream_id.to_bytes(4, sys.byteorder)


class StreamIDNeededFrame(RegularFrame):
    """"""
    TYPE_BYTE = b'\x0a'


class NewConnectionIDFrame(Frame):
    """"""
    TYPE_BYTE = b'\x0b'

    def __init__(self, sequence, connection_id):
        super().__init__(locals())

    @classmethod
    def from_bytes(cls, bytedata):
        return cls(int.from_bytes(bytedata[1:2], sys.byteorder),
                   int.from_bytes(bytedata[3:6], sys.byteorder))

    def to_bytes(self):
        return (self.TYPE_BYTE +
                self.sequence.to_bytes(2, sys.byteorder) +
                self.connection_id.to_bytes(8, sys.byteorder))


class StopWaitingFrame(Frame):
    """"""






class StreamFrame(Frame):

    def __init__(self, stream_id, offset, fin, payload):
        self.stream_id = stream_id
        self.offset = offset
        self.fin = fin
        self.payload = payload

    @classmethod
    def from_bytes(cls, bytedata):
        type_byte = bytedata[0]
        fin = type_byte & 0x40 > 0
        data_len_present = type_byte & 0x20 > 0
        offset_len = type_byte & 0x1C >> 2
        pos = 1

        stream_id_len = (type_byte & 0x03) + 1

        stream_id = int.from_bytes(bytedata[1:stream_id_len + 1], sys.byteorder)
        pos += stream_id_len
        offset = int.from_bytes(bytedata[pos:pos + offset_len + 1], sys.byteorder)
        pos += offset_len

        if not data_len_present:
            data_length = len(bytedata) - pos
        else:
            data_length = int.from_bytes(bytedata[pos:pos + 3], sys.byteorder)
            pos += 3

        payload = bytedata[pos:data_length]
        return cls(stream_id, offset, fin, payload)

    def _get_sream_id_length(self):
        return self.stream_id.bit_length() // 8 + 1

    def _get_offset_length(self):
            return self.offset.bit_length() // 8 + 1

    def to_bytes(self):

        type_byte = 0x80

        if self.fin:
            type_byte ^= 0x40

        else:
            type_byte ^= 0x20

        offset_length = self._get_offset_length()

        if offset_length > 0:
            type_byte ^= (offset_length - 1) << 2

        stream_id_len = self._get_sream_id_length()
        type_byte ^= stream_id_len - 1

        stream_id = self.stream_id.to_bytes(stream_id_len, sys.byteorder)
        offset = self.offset.to_bytes(offset_length, sys.byteorder)
        data_len = len(self.payload).to_bytes(2, sys.byteorder)

        return type_byte.to_bytes(1, sys.byteorder) + stream_id + offset + data_len + self.payload


class AckFrame(Frame):
    """"""


class QUICPacket:
    """"""


if __name__ == '__main__':
    f = StreamFrame(1, 3, False, b'test')
    assert Frame.from_bytes(f.to_bytes()) == f

    rst_stream = ResetStreamFrame(1, 1, 1)
    assert Frame.from_bytes(rst_stream.to_bytes()) == rst_stream

    blocked = BlockedFrame(1)
    assert Frame.from_bytes(blocked.to_bytes()) == blocked

    stream_blocked = StreamBlockedFrame(1)
    assert Frame.from_bytes(stream_blocked.to_bytes()) == stream_blocked

    max_data = MaxDataFrame(1)
    assert Frame.from_bytes(max_data.to_bytes()) == max_data

    new_conn_id = NewConnectionIDFrame(1, 1)
    assert Frame.from_bytes(new_conn_id.to_bytes()) == new_conn_id

    max_stream_id = MaxStreamIDFrame(1)
    assert Frame.from_bytes(max_stream_id.to_bytes()) == max_stream_id
