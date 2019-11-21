import struct
import logging

logger = logging.getLogger(__name__)


class Encoder:

    def __init__(self, data):
        self.__data = data

    def put_str32(self, value, label=None, remove_last=True):
        if remove_last:
            self.__data.write(struct.pack('I', len(value) + 1))
            enc = bytes(value, "utf-8") + b'\x00'
        else:
            self.__data.write(struct.pack('I', len(value)))
            enc = bytes(value, "utf-8")
        self.__data.write(enc)
        if label:
            logger.debug("[WRITE] {}={} with len={} ".format(label, enc, len(value) + 1))

    def put_str16(self, value, label=None, remove_last=True):
        if remove_last:
            self.__data.write(struct.pack('H', len(value) + 1))
            enc = bytes(value, "utf-8") + b'\x00'
        else:
            self.__data.write(struct.pack('H', len(value)))
            enc = bytes(value, "utf-8")
        self.__data.write(enc)
        if label:
            logger.debug("[WRITE] {}={} with len={} ".format(label, enc, len(value) + 1))

    def put_u32(self, value, label=None):
        self.__data.write(struct.pack('I', value))
        if label:
            logger.debug("[WRITE Uint32] {}={}".format(label, value))

    def put_s32(self, value, label=None):
        if label:
            logger.debug("Write int32 {}={}".format(label, value))
        self.__data.write(struct.pack('i', value))

    def put_u16(self, value):
        self.__data.write(struct.pack('H', value))

    def put_s16(self, value):
        self.__data.write(struct.pack('h', value))

    def put_u8(self, value):
        self.__data.write(struct.pack('B', value))

    def put_s8(self, value):
        self.__data.write(struct.pack('b', value))

    def put_float(self, value):
        self.__data.write(struct.pack('f', value))

    def putDouble(self, value):
        self.__data.write(struct.pack('d', value))

    def put_bytes(self, value):
        self.__data.write(value)

    def put_ascii(self, value, maxSize=None):
        value = value.strip()
        if maxSize:
            if len(value) > maxSize:
                self.__data.write(bytes(value[:maxSize], "utf-8"))
            else:
                fill = "\x00" * (maxSize - len(value))
                self.__data.write(bytes(value + fill, "utf-8"))
        else:
            self.__data.write(bytes(value, "utf-8"))
