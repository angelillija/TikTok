from enum import IntEnum, unique

class ProtoError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


@unique
class ProtoFieldType(IntEnum):
    VARINT = 0
    INT64 = 1
    STRING = 2
    GROUPSTART = 3
    GROUPEND = 4
    INT32 = 5
    ERROR1 = 6
    ERROR2 = 7


class ProtoField:
    def __init__(self, idx, type, val):
        self.idx = idx
        self.type = type
        self.val = val

    def isAsciiStr(self):
        if (type(self.val) != bytes):
            return False

        for b in self.val:
            if b < 0x20 or b > 0x7e:
                return False
        return True

    def __str__(self):
        if ((self.type == ProtoFieldType.INT32) or
            (self.type == ProtoFieldType.INT64) or
                (self.type == ProtoFieldType.VARINT)):
            return '%d(%s): %d' % (self.idx, self.type.name, self.val)
        elif self.type == ProtoFieldType.STRING:
            if self.isAsciiStr():  # self.val.isalnum()
                return '%d(%s): "%s"' % (self.idx, self.type.name, self.val.decode('ascii'))
            else:
                return '%d(%s): h"%s"' % (self.idx, self.type.name, self.val.hex())
        elif ((self.type == ProtoFieldType.GROUPSTART) or (self.type == ProtoFieldType.GROUPEND)):
            return '%d(%s): %s' % (self.idx, self.type.name, self.val)
        else:
            return '%d(%s): %s' % (self.idx, self.type.name, self.val)


class ProtoReader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def seek(self, pos):
        self.pos = pos

    def isRemain(self, length):
        return self.pos + length <= len(self.data)

    def read0(self):
        assert (self.isRemain(1))
        ret = self.data[self.pos]
        self.pos += 1
        return ret & 0xFF

    def read(self, length):
        assert (self.isRemain(length))
        ret = self.data[self.pos:self.pos+length]
        self.pos += length
        return ret

    def readInt32(self):
        return int.from_bytes(self.read(4), byteorder='little', signed=False)

    def readInt64(self):
        return int.from_bytes(self.read(8), byteorder='little', signed=False)

    def readVarint(self):
        vint = 0
        n = 0
        while True:
            byte = self.read0()
            vint |= ((byte & 0x7F) << (7 * n))
            if byte < 0x80:
                break
            n += 1

        return vint

    def readString(self):
        len = self.readVarint()
        return self.read(len)


class ProtoWriter:
    def __init__(self):
        self.data = bytearray()

    def write0(self, byte):
        self.data.append(byte & 0xFF)

    def write(self, bytes):
        self.data.extend(bytes)

    def writeInt32(self, int32):
        bs = int32.to_bytes(4, byteorder='little', signed=False)
        self.write(bs)

    def writeInt64(self, int64):
        bs = int64.to_bytes(8, byteorder='little', signed=False)
        self.write(bs)

    def writeVarint(self, vint):
        vint = vint & 0xFFFFFFFF
        while (vint > 0x80):
            self.write0((vint & 0x7F) | 0x80)
            vint >>= 7
        self.write0(vint & 0x7F)

    def writeString(self, bytes):
        self.writeVarint(len(bytes))
        self.write(bytes)

    def toBytes(self):
        return bytes(self.data)


class ProtoBuf:
    def __init__(self, data=None):
        self.fields = list[ProtoField]()
        if (data != None):
            if (type(data) != bytes and type(data) != dict):
                raise ProtoError(
                    'unsupport type(%s) to protobuf' % (type(data)))

            if (type(data) == bytes) and (len(data) > 0):
                self.__parseBuf(data)
            elif (type(data) == dict) and (len(data) > 0):
                self.__parseDict(data)

    def __getitem__(self, idx):
        pf = self.get(int(idx))
        if (pf == None):
            return None
        if (pf.type != ProtoFieldType.STRING):
            return pf.val
        if (type(idx) != int):
            return pf.val
        if (pf.val == None):
            return None
        if (pf.isAsciiStr()):
            return pf.val.decode('utf-8')
        return ProtoBuf(pf.val)

    def __parseBuf(self, bytes):
        reader = ProtoReader(bytes)
        while reader.isRemain(1):
            key = reader.readVarint()
            field_type = ProtoFieldType(key & 0x7)
            field_idx = key >> 3
            if (field_idx == 0):
                break
            if (field_type == ProtoFieldType.INT32):
                self.put(ProtoField(field_idx, field_type, reader.readInt32()))
            elif (field_type == ProtoFieldType.INT64):
                self.put(ProtoField(field_idx, field_type, reader.readInt64()))
            elif (field_type == ProtoFieldType.VARINT):
                self.put(ProtoField(field_idx, field_type, reader.readVarint()))
            elif (field_type == ProtoFieldType.STRING):
                self.put(ProtoField(field_idx, field_type, reader.readString()))
            else:
                raise ProtoError(
                    'parse protobuf error, unexpected field type: %s' % (field_type.name))

    def toBuf(self):
        writer = ProtoWriter()
        for field in self.fields:
            key = (field.idx << 3) | (field.type & 7)
            writer.writeVarint(key)
            if field.type == ProtoFieldType.INT32:
                writer.writeInt32(field.val)
            elif field.type == ProtoFieldType.INT64:
                writer.writeInt64(field.val)
            elif field.type == ProtoFieldType.VARINT:
                writer.writeVarint(field.val)
            elif field.type == ProtoFieldType.STRING:
                writer.writeString(field.val)
            else:
                raise ProtoError(
                    'encode to protobuf error, unexpected field type: %s' % (field.type.name))
        return writer.toBytes()

    def dump(self):
        for field in self.fields:
            print(field)

    def getList(self, idx):
        return [field for field in self.fields if field.idx == idx]

    def get(self, idx):
        for field in self.fields:
            if field.idx == idx:
                return field
        return None

    def getInt(self, idx):
        pf = self.get(idx)
        if (pf == None):
            return 0
        if ((pf.type == ProtoFieldType.INT32) or (pf.type == ProtoFieldType.INT64) or (pf.type == ProtoFieldType.VARINT)):
            return pf.val
        raise ProtoError("getInt(%d) -> %s" % (idx, pf.type))

    def getBytes(self, idx):
        pf = self.get(idx)
        if (pf == None):
            return None
        if (pf.type == ProtoFieldType.STRING):
            return pf.val
        raise ProtoError("getBytes(%d) -> %s" % (idx, pf.type))

    def getUtf8(self, idx):
        bs = self.getBytes(idx)
        if (bs == None):
            return None
        return bs.decode('utf-8')

    def getProtoBuf(self, idx):
        bs = self.getBytes(idx)
        if (bs == None):
            return None
        return ProtoBuf(bs)

    def put(self, field: ProtoField):
        self.fields.append(field)

    def putInt32(self, idx, int32):
        self.put(ProtoField(idx, ProtoFieldType.INT32, int32))

    def putInt64(self, idx, int64):
        self.put(ProtoField(idx, ProtoFieldType.INT64, int64))

    def putVarint(self, idx, vint):
        self.put(ProtoField(idx, ProtoFieldType.VARINT, vint))

    def putBytes(self, idx, data):
        self.put(ProtoField(idx, ProtoFieldType.STRING, data))

    def putUtf8(self, idx, data):
        self.put(ProtoField(idx, ProtoFieldType.STRING, data.encode('utf-8')))

    def putProtoBuf(self, idx, data):
        self.put(ProtoField(idx, ProtoFieldType.STRING, data.toBuf()))

    def __parseDict(self, data):
        for k, v in data.items():
            if (isinstance(v, int)):
                self.putVarint(k, v)
            elif (isinstance(v, str)):
                self.putUtf8(k, v)
            elif (isinstance(v, bytes)):
                self.putBytes(k, v)
            elif (isinstance(v, dict)):
                self.putProtoBuf(k, ProtoBuf(v))
            else:
                raise ProtoError('unsupport type(%s) to protobuf' % (type(v)))

    def toDict(self, out):
        for k, v in out.items():
            if (isinstance(v, int)):
                out[k] = self.getInt(k)
            elif (isinstance(v, str)):
                out[k] = self.getUtf8(k)
            elif (isinstance(v, bytes)):
                out[k] = self.getBytes(k)
            elif (isinstance(v, dict)):
                out[k] = self.getProtoBuf(k).toDict(v)
            else:
                raise ProtoError('unsupport type(%s) to protobuf' % (type(v)))
        return out
