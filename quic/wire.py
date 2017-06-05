
import sys


class Frame:
    """"""

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
            0x0: PaddingFrame,
            0x1: ResetStreamFrame,
            0x2: ConnectionCloseFrame,
            0x3: GoAwayFrame,
            0x4: WindowUpdateFrame,
            0x5: BlockedFrame,
            0x6: StopWaitingFrame,
            0x7: PingFrame
        }

        try:
            return switch[type_byte].from_bytes(bytedata)
        except KeyError:
            raise Exception('Invalid frame type')


class PaddingFrame(Frame):
    """"""

    @classmethod
    def from_bytes(cls, bytedata):
        return cls()

    def to_bytes(self):
        return b'\x00'


class ResetStreamFrame(Frame):
    """"""

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
        return (b'\x01' +
                self.stream_id.to_bytes(4, sys.byteorder) +
                self.offset.to_bytes(8, sys.byteorder) +
                self.error.to_bytes(4, sys.byteorder))



class ConnectionCloseFrame(Frame):
    """"""


class GoAwayFrame(Frame):
    """"""


class WindowUpdateFrame(Frame):
    """"""

    def __init__(self, stream_id, offset):
        self.stream_id = stream_id
        self.offset = offset

    @classmethod
    def from_bytes(cls, bytedata):
        return cls(int.from_bytes(bytedata[1:4], sys.byteorder),
                   int.from_bytes(bytedata[5:12], sys.byteorder))

    def to_bytes(self):
        return (b'\x04' +
                self.stream_id.to_bytes(4, sys.byteorder) +
                self.offset.to_bytes(8, sys.byteorder))


class BlockedFrame(Frame):
    """"""


class StopWaitingFrame(Frame):
    """"""


class PingFrame(Frame):
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


class CongestionFeedbackFrame(Frame):
    """"""


class QUICPacket:
    """"""


if __name__ == '__main__':
    f = StreamFrame(1, 3, False, b'test')
    assert Frame.from_bytes(f.to_bytes()) == f

    rst_stream = ResetStreamFrame(1, 1, 1)
    assert Frame.from_bytes(rst_stream.to_bytes()) == rst_stream

    window_update = WindowUpdateFrame(1, 1)
    assert Frame.from_bytes(window_update.to_bytes()) == window_update
