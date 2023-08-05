"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class lcmt_viewer_geometry_data(object):
    __slots__ = ["type", "position", "quaternion", "color", "string_data", "num_float_data", "float_data"]

    __typenames__ = ["int8_t", "float", "float", "float", "string", "int32_t", "float"]

    __dimensions__ = [None, [3], [4], [4], None, None, ["num_float_data"]]

    BOX = 1
    SPHERE = 2
    CYLINDER = 3
    MESH = 4
    CAPSULE = 5
    ELLIPSOID = 6

    def __init__(self):
        self.type = 0
        self.position = [ 0.0 for dim0 in range(3) ]
        self.quaternion = [ 0.0 for dim0 in range(4) ]
        self.color = [ 0.0 for dim0 in range(4) ]
        self.string_data = ""
        self.num_float_data = 0
        self.float_data = []

    def encode(self):
        buf = BytesIO()
        buf.write(lcmt_viewer_geometry_data._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">b", self.type))
        buf.write(struct.pack('>3f', *self.position[:3]))
        buf.write(struct.pack('>4f', *self.quaternion[:4]))
        buf.write(struct.pack('>4f', *self.color[:4]))
        __string_data_encoded = self.string_data.encode('utf-8')
        buf.write(struct.pack('>I', len(__string_data_encoded)+1))
        buf.write(__string_data_encoded)
        buf.write(b"\0")
        buf.write(struct.pack(">i", self.num_float_data))
        buf.write(struct.pack('>%df' % self.num_float_data, *self.float_data[:self.num_float_data]))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != lcmt_viewer_geometry_data._get_packed_fingerprint():
            raise ValueError("Decode error")
        return lcmt_viewer_geometry_data._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = lcmt_viewer_geometry_data()
        self.type = struct.unpack(">b", buf.read(1))[0]
        self.position = struct.unpack('>3f', buf.read(12))
        self.quaternion = struct.unpack('>4f', buf.read(16))
        self.color = struct.unpack('>4f', buf.read(16))
        __string_data_len = struct.unpack('>I', buf.read(4))[0]
        self.string_data = buf.read(__string_data_len)[:-1].decode('utf-8', 'replace')
        self.num_float_data = struct.unpack(">i", buf.read(4))[0]
        self.float_data = struct.unpack('>%df' % self.num_float_data, buf.read(self.num_float_data * 4))
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if lcmt_viewer_geometry_data in parents: return 0
        tmphash = (0xae971a65992bed83) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if lcmt_viewer_geometry_data._packed_fingerprint is None:
            lcmt_viewer_geometry_data._packed_fingerprint = struct.pack(">Q", lcmt_viewer_geometry_data._get_hash_recursive([]))
        return lcmt_viewer_geometry_data._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", lcmt_viewer_geometry_data._get_packed_fingerprint())[0]

