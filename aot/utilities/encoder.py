import struct
import logging

logger = logging.getLogger(__name__)


class Encoder:

    def __init__(self, data):
        self.__data = data

    def putStr32(self, value, label=None,remove_last=True):
        if remove_last:
            self.__data.write(struct.pack('I', len(value) + 1))
            enc = bytes(value, "utf-8") + b'\x00'
        else:
            self.__data.write(struct.pack('I', len(value)))
            enc = bytes(value, "utf-8")
        self.__data.write(enc)
        if label:
            logger.debug("[WRITE] {}={} with len={} ".format(label, enc, len(value) + 1))

    def putStr16(self, value,label=None,remove_last=True):
        if remove_last:
            self.__data.write(struct.pack('H', len(value) + 1))
            enc = bytes(value, "utf-8") + b'\x00'
        else:
            self.__data.write(struct.pack('H', len(value)))
            enc = bytes(value, "utf-8")
        self.__data.write(enc)
        if label:
            logger.debug("[WRITE] {}={} with len={} ".format(label, enc, len(value) + 1))


    def putUInt32(self, value,label=None):
        self.__data.write(struct.pack('I', value))
        if label:
            logger.debug("[WRITE Uint32] {}={}".format(label,value))


    def putInt32(self, value, label=None):
        if label:
            logger.debug("Write int32 {}={}".format(label, value))
        self.__data.write(struct.pack('i', value))


    def putUInt16(self, value):
        self.__data.write(struct.pack('H', value))


    def putInt16(self, value):
        self.__data.write(struct.pack('h', value))


    def putUInt8(self, value):
        self.__data.write(struct.pack('B', value))


    def putInt8(self, value):
        self.__data.write(struct.pack('b', value))


    def putFloat(self, value):
        self.__data.write(struct.pack('f', value))


    def putDouble(self, value):
        self.__data.write(struct.pack('d', value))


    def putBytes(self, value):
        self.__data.write(value)


    def putAscii(self, value, maxSize=None):
        value = value.strip()
        if maxSize:
            if len(value) > maxSize:
                self.__data.write(bytes(value[:maxSize], "utf-8"))
            else:
                fill = "\x00" * (maxSize - len(value))
                self.__data.write(bytes(value + fill, "utf-8"))
        else:
            self.__data.write(bytes(value, "utf-8"))
