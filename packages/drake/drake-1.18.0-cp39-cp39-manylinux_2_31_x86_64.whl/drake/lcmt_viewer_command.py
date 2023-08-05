"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class lcmt_viewer_command(object):
    __slots__ = ["command_type", "command_data"]

    __typenames__ = ["int8_t", "string"]

    __dimensions__ = [None, None]

    STATUS = 0
    LOAD_MODEL = 1
    LOAD_RENDERER = 2
    SHUTDOWN = 3
    START_RECORDING = 4
    STOP_RECORDING = 5
    LOAD_TERRAIN = 6
    SET_TERRAIN_TRANSFORM = 7

    def __init__(self):
        self.command_type = 0
        self.command_data = ""

    def encode(self):
        buf = BytesIO()
        buf.write(lcmt_viewer_command._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">b", self.command_type))
        __command_data_encoded = self.command_data.encode('utf-8')
        buf.write(struct.pack('>I', len(__command_data_encoded)+1))
        buf.write(__command_data_encoded)
        buf.write(b"\0")

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != lcmt_viewer_command._get_packed_fingerprint():
            raise ValueError("Decode error")
        return lcmt_viewer_command._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = lcmt_viewer_command()
        self.command_type = struct.unpack(">b", buf.read(1))[0]
        __command_data_len = struct.unpack('>I', buf.read(4))[0]
        self.command_data = buf.read(__command_data_len)[:-1].decode('utf-8', 'replace')
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if lcmt_viewer_command in parents: return 0
        tmphash = (0x7878fb2792b4a897) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if lcmt_viewer_command._packed_fingerprint is None:
            lcmt_viewer_command._packed_fingerprint = struct.pack(">Q", lcmt_viewer_command._get_hash_recursive([]))
        return lcmt_viewer_command._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", lcmt_viewer_command._get_packed_fingerprint())[0]

