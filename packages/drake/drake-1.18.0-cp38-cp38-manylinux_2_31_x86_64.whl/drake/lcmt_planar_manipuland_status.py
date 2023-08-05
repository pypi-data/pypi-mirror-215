"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class lcmt_planar_manipuland_status(object):
    __slots__ = ["utime", "position", "theta", "velocity", "thetadot"]

    __typenames__ = ["int64_t", "double", "double", "double", "double"]

    __dimensions__ = [None, [2], None, [2], None]

    def __init__(self):
        self.utime = 0
        self.position = [ 0.0 for dim0 in range(2) ]
        self.theta = 0.0
        self.velocity = [ 0.0 for dim0 in range(2) ]
        self.thetadot = 0.0

    def encode(self):
        buf = BytesIO()
        buf.write(lcmt_planar_manipuland_status._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">q", self.utime))
        buf.write(struct.pack('>2d', *self.position[:2]))
        buf.write(struct.pack(">d", self.theta))
        buf.write(struct.pack('>2d', *self.velocity[:2]))
        buf.write(struct.pack(">d", self.thetadot))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != lcmt_planar_manipuland_status._get_packed_fingerprint():
            raise ValueError("Decode error")
        return lcmt_planar_manipuland_status._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = lcmt_planar_manipuland_status()
        self.utime = struct.unpack(">q", buf.read(8))[0]
        self.position = struct.unpack('>2d', buf.read(16))
        self.theta = struct.unpack(">d", buf.read(8))[0]
        self.velocity = struct.unpack('>2d', buf.read(16))
        self.thetadot = struct.unpack(">d", buf.read(8))[0]
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if lcmt_planar_manipuland_status in parents: return 0
        tmphash = (0xd2ae3532484f4461) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if lcmt_planar_manipuland_status._packed_fingerprint is None:
            lcmt_planar_manipuland_status._packed_fingerprint = struct.pack(">Q", lcmt_planar_manipuland_status._get_hash_recursive([]))
        return lcmt_planar_manipuland_status._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", lcmt_planar_manipuland_status._get_packed_fingerprint())[0]

