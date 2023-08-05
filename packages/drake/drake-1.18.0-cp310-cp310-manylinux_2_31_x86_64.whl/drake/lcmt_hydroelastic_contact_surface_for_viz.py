"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

import drake.lcmt_point

import drake.lcmt_hydroelastic_quadrature_per_point_data_for_viz

class lcmt_hydroelastic_contact_surface_for_viz(object):
    __slots__ = ["geometry1_name", "body1_name", "model1_name", "body1_unique", "collision_count1", "geometry2_name", "body2_name", "model2_name", "body2_unique", "collision_count2", "centroid_W", "force_C_W", "moment_C_W", "num_quadrature_points", "quadrature_point_data", "num_vertices", "p_WV", "pressure", "poly_data_int_count", "poly_data"]

    __typenames__ = ["string", "string", "string", "boolean", "int32_t", "string", "string", "string", "boolean", "int32_t", "double", "double", "double", "int32_t", "drake.lcmt_hydroelastic_quadrature_per_point_data_for_viz", "int32_t", "drake.lcmt_point", "double", "int32_t", "int32_t"]

    __dimensions__ = [None, None, None, None, None, None, None, None, None, None, [3], [3], [3], None, ["num_quadrature_points"], None, ["num_vertices"], ["num_vertices"], None, ["poly_data_int_count"]]

    def __init__(self):
        self.geometry1_name = ""
        self.body1_name = ""
        self.model1_name = ""
        self.body1_unique = False
        self.collision_count1 = 0
        self.geometry2_name = ""
        self.body2_name = ""
        self.model2_name = ""
        self.body2_unique = False
        self.collision_count2 = 0
        self.centroid_W = [ 0.0 for dim0 in range(3) ]
        self.force_C_W = [ 0.0 for dim0 in range(3) ]
        self.moment_C_W = [ 0.0 for dim0 in range(3) ]
        self.num_quadrature_points = 0
        self.quadrature_point_data = []
        self.num_vertices = 0
        self.p_WV = []
        self.pressure = []
        self.poly_data_int_count = 0
        self.poly_data = []

    def encode(self):
        buf = BytesIO()
        buf.write(lcmt_hydroelastic_contact_surface_for_viz._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        __geometry1_name_encoded = self.geometry1_name.encode('utf-8')
        buf.write(struct.pack('>I', len(__geometry1_name_encoded)+1))
        buf.write(__geometry1_name_encoded)
        buf.write(b"\0")
        __body1_name_encoded = self.body1_name.encode('utf-8')
        buf.write(struct.pack('>I', len(__body1_name_encoded)+1))
        buf.write(__body1_name_encoded)
        buf.write(b"\0")
        __model1_name_encoded = self.model1_name.encode('utf-8')
        buf.write(struct.pack('>I', len(__model1_name_encoded)+1))
        buf.write(__model1_name_encoded)
        buf.write(b"\0")
        buf.write(struct.pack(">bi", self.body1_unique, self.collision_count1))
        __geometry2_name_encoded = self.geometry2_name.encode('utf-8')
        buf.write(struct.pack('>I', len(__geometry2_name_encoded)+1))
        buf.write(__geometry2_name_encoded)
        buf.write(b"\0")
        __body2_name_encoded = self.body2_name.encode('utf-8')
        buf.write(struct.pack('>I', len(__body2_name_encoded)+1))
        buf.write(__body2_name_encoded)
        buf.write(b"\0")
        __model2_name_encoded = self.model2_name.encode('utf-8')
        buf.write(struct.pack('>I', len(__model2_name_encoded)+1))
        buf.write(__model2_name_encoded)
        buf.write(b"\0")
        buf.write(struct.pack(">bi", self.body2_unique, self.collision_count2))
        buf.write(struct.pack('>3d', *self.centroid_W[:3]))
        buf.write(struct.pack('>3d', *self.force_C_W[:3]))
        buf.write(struct.pack('>3d', *self.moment_C_W[:3]))
        buf.write(struct.pack(">i", self.num_quadrature_points))
        for i0 in range(self.num_quadrature_points):
            assert self.quadrature_point_data[i0]._get_packed_fingerprint() == drake.lcmt_hydroelastic_quadrature_per_point_data_for_viz._get_packed_fingerprint()
            self.quadrature_point_data[i0]._encode_one(buf)
        buf.write(struct.pack(">i", self.num_vertices))
        for i0 in range(self.num_vertices):
            assert self.p_WV[i0]._get_packed_fingerprint() == drake.lcmt_point._get_packed_fingerprint()
            self.p_WV[i0]._encode_one(buf)
        buf.write(struct.pack('>%dd' % self.num_vertices, *self.pressure[:self.num_vertices]))
        buf.write(struct.pack(">i", self.poly_data_int_count))
        buf.write(struct.pack('>%di' % self.poly_data_int_count, *self.poly_data[:self.poly_data_int_count]))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != lcmt_hydroelastic_contact_surface_for_viz._get_packed_fingerprint():
            raise ValueError("Decode error")
        return lcmt_hydroelastic_contact_surface_for_viz._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = lcmt_hydroelastic_contact_surface_for_viz()
        __geometry1_name_len = struct.unpack('>I', buf.read(4))[0]
        self.geometry1_name = buf.read(__geometry1_name_len)[:-1].decode('utf-8', 'replace')
        __body1_name_len = struct.unpack('>I', buf.read(4))[0]
        self.body1_name = buf.read(__body1_name_len)[:-1].decode('utf-8', 'replace')
        __model1_name_len = struct.unpack('>I', buf.read(4))[0]
        self.model1_name = buf.read(__model1_name_len)[:-1].decode('utf-8', 'replace')
        self.body1_unique = bool(struct.unpack('b', buf.read(1))[0])
        self.collision_count1 = struct.unpack(">i", buf.read(4))[0]
        __geometry2_name_len = struct.unpack('>I', buf.read(4))[0]
        self.geometry2_name = buf.read(__geometry2_name_len)[:-1].decode('utf-8', 'replace')
        __body2_name_len = struct.unpack('>I', buf.read(4))[0]
        self.body2_name = buf.read(__body2_name_len)[:-1].decode('utf-8', 'replace')
        __model2_name_len = struct.unpack('>I', buf.read(4))[0]
        self.model2_name = buf.read(__model2_name_len)[:-1].decode('utf-8', 'replace')
        self.body2_unique = bool(struct.unpack('b', buf.read(1))[0])
        self.collision_count2 = struct.unpack(">i", buf.read(4))[0]
        self.centroid_W = struct.unpack('>3d', buf.read(24))
        self.force_C_W = struct.unpack('>3d', buf.read(24))
        self.moment_C_W = struct.unpack('>3d', buf.read(24))
        self.num_quadrature_points = struct.unpack(">i", buf.read(4))[0]
        self.quadrature_point_data = []
        for i0 in range(self.num_quadrature_points):
            self.quadrature_point_data.append(drake.lcmt_hydroelastic_quadrature_per_point_data_for_viz._decode_one(buf))
        self.num_vertices = struct.unpack(">i", buf.read(4))[0]
        self.p_WV = []
        for i0 in range(self.num_vertices):
            self.p_WV.append(drake.lcmt_point._decode_one(buf))
        self.pressure = struct.unpack('>%dd' % self.num_vertices, buf.read(self.num_vertices * 8))
        self.poly_data_int_count = struct.unpack(">i", buf.read(4))[0]
        self.poly_data = struct.unpack('>%di' % self.poly_data_int_count, buf.read(self.poly_data_int_count * 4))
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if lcmt_hydroelastic_contact_surface_for_viz in parents: return 0
        newparents = parents + [lcmt_hydroelastic_contact_surface_for_viz]
        tmphash = (0x4efd7d8f630a0b66+ drake.lcmt_hydroelastic_quadrature_per_point_data_for_viz._get_hash_recursive(newparents)+ drake.lcmt_point._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if lcmt_hydroelastic_contact_surface_for_viz._packed_fingerprint is None:
            lcmt_hydroelastic_contact_surface_for_viz._packed_fingerprint = struct.pack(">Q", lcmt_hydroelastic_contact_surface_for_viz._get_hash_recursive([]))
        return lcmt_hydroelastic_contact_surface_for_viz._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", lcmt_hydroelastic_contact_surface_for_viz._get_packed_fingerprint())[0]

