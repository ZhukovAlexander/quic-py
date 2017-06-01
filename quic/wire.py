
import struct


class StructField:
    """
    Descriptor representing a simple structure field
    """

    def __init__(self, fmt):
        self.fmt = fmt
        self.struct_format = None

    def __get__(self, instance, cls):
        self._instance = instance
        self.struct_format = self.fmt.format(vars(instance))
        if instance is None:
            return self
        else:
            r = struct.unpack_from(self.struct_format, instance._buffer, self.offset)
            return r[0] if len(r) == 1 else r

    def __set__(self, instance, value):
        if instance is None:
            return None
        struct.pack_into(self.struct_format, instance._buffer, self.offset, value)


class NestedStruct:
    """
    Descriptor representing a nested structure
    """

    def __init__(self, name, struct_type, offset):
        self.name = name
        self.struct_type = struct_type
        self.offset = offset

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            data = instance._buffer[self.offset:
            self.offset + self.struct_type.struct_size]
            result = self.struct_type(data)
            # Save resulting structure back on instance to avoid
            # further recomputation of this step
            setattr(instance, self.name, result)
            return result

    def __set__(self, instance, value):
        pass



class StructureMeta(type):
    """
    Metaclass that automatically creates StructField descriptors
    """

    def __init__(self, clsname, bases, clsdict):
        fields = getattr(self, '_fields_', [])
        byte_order = ''
        offset = 0
        for fmt, fieldname in fields:
            if isinstance(fmt, Structure):
                setattr(self, fieldname,
                        NestedStruct(fieldname, fmt, offset))
                offset += fmt.struct_size
            else:
                if fmt.startswith(('<', '>', '!', '@')):
                    byte_order = fmt[0]
                    fmt = fmt[1:]
                fmt = byte_order + fmt
                clsdict[fieldname] = StructField(fmt, offset)
                # setattr(self, fieldname, StructField(fmt, offset))
                offset += struct.calcsize(fmt)
        setattr(self, 'struct_size', offset)


class Structure(metaclass=StructureMeta):

    def __init__(self, **kwargs):
        self._buffer = bytearray(100)
        for kw, val in kwargs.items():
            setattr(self, kw, val)

    def from_bytes(self, bytedata):
        self._buffer = memoryview(bytedata)


# class FrameType(Structure):
#     """
#     Represents frame type field
#     """
#
# class Frame(Structure):
#     """"""
#     _fields_ = (
#         (FrameType, 'frame_type'),
#     )
#
#     def pack(self):
#         buff = b''


class StreamFrame(Structure):

    def __init__(self, fin=False, data_length_present=True, offset_length=0, stream_id_length=8, **kwargs):
        self.fin = fin
        self.data_length_present = data_length_present
        self.offset_length = offset_length
        self.stream_id_length = stream_id_length
        super().__init__(self, **kwargs)

    _fields_ = (
        (lambda self: 'h' if not self.fin else None, 'data_length'),
        ('i', 'stream_id'),
        ('Q', 'offset'),
        (lambda self: '{0}s'.format(self.data_length), 'stream_data')

    )


class QUICPacket:
    """"""
