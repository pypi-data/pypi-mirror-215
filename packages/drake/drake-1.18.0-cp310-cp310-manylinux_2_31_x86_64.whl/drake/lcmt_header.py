"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class lcmt_header(object):
    __slots__ = ["seq", "utime", "frame_name"]

    __typenames__ = ["int32_t", "int64_t", "string"]

    __dimensions__ = [None, None, None]

    def __init__(self):
        self.seq = 0
        self.utime = 0
        self.frame_name = ""

    def encode(self):
        buf = BytesIO()
        buf.write(lcmt_header._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">iq", self.seq, self.utime))
        __frame_name_encoded = self.frame_name.encode('utf-8')
        buf.write(struct.pack('>I', len(__frame_name_encoded)+1))
        buf.write(__frame_name_encoded)
        buf.write(b"\0")

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != lcmt_header._get_packed_fingerprint():
            raise ValueError("Decode error")
        return lcmt_header._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = lcmt_header()
        self.seq, self.utime = struct.unpack(">iq", buf.read(12))
        __frame_name_len = struct.unpack('>I', buf.read(4))[0]
        self.frame_name = buf.read(__frame_name_len)[:-1].decode('utf-8', 'replace')
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if lcmt_header in parents: return 0
        tmphash = (0x9272c333198c72a) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if lcmt_header._packed_fingerprint is None:
            lcmt_header._packed_fingerprint = struct.pack(">Q", lcmt_header._get_hash_recursive([]))
        return lcmt_header._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", lcmt_header._get_packed_fingerprint())[0]

