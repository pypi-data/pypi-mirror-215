"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

import drake.experimental_lcmt_deformable_tri

class experimental_lcmt_deformable_tri_mesh_init(object):
    __slots__ = ["name", "num_vertices", "num_tris", "tris"]

    __typenames__ = ["string", "int32_t", "int32_t", "drake.experimental_lcmt_deformable_tri"]

    __dimensions__ = [None, None, None, ["num_tris"]]

    def __init__(self):
        self.name = ""
        self.num_vertices = 0
        self.num_tris = 0
        self.tris = []

    def encode(self):
        buf = BytesIO()
        buf.write(experimental_lcmt_deformable_tri_mesh_init._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        __name_encoded = self.name.encode('utf-8')
        buf.write(struct.pack('>I', len(__name_encoded)+1))
        buf.write(__name_encoded)
        buf.write(b"\0")
        buf.write(struct.pack(">ii", self.num_vertices, self.num_tris))
        for i0 in range(self.num_tris):
            assert self.tris[i0]._get_packed_fingerprint() == drake.experimental_lcmt_deformable_tri._get_packed_fingerprint()
            self.tris[i0]._encode_one(buf)

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != experimental_lcmt_deformable_tri_mesh_init._get_packed_fingerprint():
            raise ValueError("Decode error")
        return experimental_lcmt_deformable_tri_mesh_init._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = experimental_lcmt_deformable_tri_mesh_init()
        __name_len = struct.unpack('>I', buf.read(4))[0]
        self.name = buf.read(__name_len)[:-1].decode('utf-8', 'replace')
        self.num_vertices, self.num_tris = struct.unpack(">ii", buf.read(8))
        self.tris = []
        for i0 in range(self.num_tris):
            self.tris.append(drake.experimental_lcmt_deformable_tri._decode_one(buf))
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if experimental_lcmt_deformable_tri_mesh_init in parents: return 0
        newparents = parents + [experimental_lcmt_deformable_tri_mesh_init]
        tmphash = (0xd22caf8e7aa0f66d+ drake.experimental_lcmt_deformable_tri._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if experimental_lcmt_deformable_tri_mesh_init._packed_fingerprint is None:
            experimental_lcmt_deformable_tri_mesh_init._packed_fingerprint = struct.pack(">Q", experimental_lcmt_deformable_tri_mesh_init._get_hash_recursive([]))
        return experimental_lcmt_deformable_tri_mesh_init._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", experimental_lcmt_deformable_tri_mesh_init._get_packed_fingerprint())[0]

