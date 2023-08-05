"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

import drake.lcmt_image

import drake.lcmt_header

class lcmt_image_array(object):
    __slots__ = ["header", "num_images", "images"]

    __typenames__ = ["drake.lcmt_header", "int32_t", "drake.lcmt_image"]

    __dimensions__ = [None, None, ["num_images"]]

    def __init__(self):
        self.header = drake.lcmt_header()
        self.num_images = 0
        self.images = []

    def encode(self):
        buf = BytesIO()
        buf.write(lcmt_image_array._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        assert self.header._get_packed_fingerprint() == drake.lcmt_header._get_packed_fingerprint()
        self.header._encode_one(buf)
        buf.write(struct.pack(">i", self.num_images))
        for i0 in range(self.num_images):
            assert self.images[i0]._get_packed_fingerprint() == drake.lcmt_image._get_packed_fingerprint()
            self.images[i0]._encode_one(buf)

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != lcmt_image_array._get_packed_fingerprint():
            raise ValueError("Decode error")
        return lcmt_image_array._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = lcmt_image_array()
        self.header = drake.lcmt_header._decode_one(buf)
        self.num_images = struct.unpack(">i", buf.read(4))[0]
        self.images = []
        for i0 in range(self.num_images):
            self.images.append(drake.lcmt_image._decode_one(buf))
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if lcmt_image_array in parents: return 0
        newparents = parents + [lcmt_image_array]
        tmphash = (0x3afa7aac7daa3b4e+ drake.lcmt_header._get_hash_recursive(newparents)+ drake.lcmt_image._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if lcmt_image_array._packed_fingerprint is None:
            lcmt_image_array._packed_fingerprint = struct.pack(">Q", lcmt_image_array._get_hash_recursive([]))
        return lcmt_image_array._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", lcmt_image_array._get_packed_fingerprint())[0]

