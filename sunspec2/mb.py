"""
    Copyright (C) 2020 SunSpec Alliance

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.
"""

import struct
import base64
import collections

import sunspec2.mdef as mdef

SUNS_BASE_ADDR_DEFAULT = 40000
SUNS_SUNS_LEN = 2

SUNS_UNIMPL_INT16 = -32768
SUNS_UNIMPL_UINT16 = 0xffff
SUNS_UNIMPL_ACC16 = 0
SUNS_UNIMPL_ENUM16 = 0xffff
SUNS_UNIMPL_BITFIELD16 = 0xffff
SUNS_UNIMPL_INT32 = -2147483648
SUNS_UNIMPL_UINT32 = 0xffffffff
SUNS_UNIMPL_ACC32 = 0
SUNS_UNIMPL_ENUM32 = 0xffffffff
SUNS_UNIMPL_BITFIELD32 = 0xffffffff
SUNS_UNIMPL_IPADDR = 0
SUNS_UNIMPL_INT64 = -9223372036854775808
SUNS_UNIMPL_UINT64 = 0xffffffffffffffff
SUNS_UNIMPL_ACC64 = 0
SUNS_UNIMPL_IPV6ADDR = 0
SUNS_UNIMPL_FLOAT32 = 0x7fc00000
SUNS_UNIMPL_FLOAT64 = 0x7ff8000000000000
SUNS_UNIMPL_STRING = '\0'
SUNS_UNIMPL_SUNSSF = -32768
SUNS_UNIMPL_EUI48 = 'FF:FF:FF:FF:FF:FF'
SUNS_UNIMPL_PAD = 0

SUNS_BLOCK_FIXED = 'fixed'
SUNS_BLOCK_REPEATING = 'repeating'

SUNS_END_MODEL_ID = 0xffff

unimpl_value = {
    mdef.TYPE_INT16: SUNS_UNIMPL_INT16,
    mdef.TYPE_UINT16: SUNS_UNIMPL_UINT16,
    mdef.TYPE_ACC16: SUNS_UNIMPL_ACC16,
    mdef.TYPE_ENUM16: SUNS_UNIMPL_ENUM16,
    mdef.TYPE_BITFIELD16: SUNS_UNIMPL_BITFIELD16,
    mdef.TYPE_INT32: SUNS_UNIMPL_INT32,
    mdef.TYPE_UINT32: SUNS_UNIMPL_UINT32,
    mdef.TYPE_ACC32: SUNS_UNIMPL_ACC32,
    mdef.TYPE_ENUM32: SUNS_UNIMPL_ENUM32,
    mdef.TYPE_BITFIELD32: SUNS_UNIMPL_BITFIELD32,
    mdef.TYPE_IPADDR: SUNS_UNIMPL_IPADDR,
    mdef.TYPE_INT64: SUNS_UNIMPL_INT64,
    mdef.TYPE_UINT64: SUNS_UNIMPL_UINT64,
    mdef.TYPE_ACC64: SUNS_UNIMPL_ACC64,
    mdef.TYPE_IPV6ADDR: SUNS_UNIMPL_IPV6ADDR,
    mdef.TYPE_FLOAT32: SUNS_UNIMPL_FLOAT32,
    mdef.TYPE_STRING: SUNS_UNIMPL_STRING,
    mdef.TYPE_SUNSSF: SUNS_UNIMPL_SUNSSF,
    mdef.TYPE_EUI48: SUNS_UNIMPL_EUI48,
    mdef.TYPE_PAD: SUNS_UNIMPL_PAD
}


def create_unimpl_value(vtype, len=None):
    value = unimpl_value.get(vtype)
    if vtype is None:
        raise ValueError('Unknown SunSpec value type: %s' % vtype)
    if vtype == mdef.TYPE_STRING:
        if len is not None:
            return b'\0' * len
        else:
            raise ValueError('Unimplemented value creation for string requires a length')
    elif vtype == mdef.TYPE_IPV6ADDR:
        return b'\0' * 16
    return point_type_info[vtype][3](value)


class SunSpecError(Exception):
    pass


""" 
Functions to pack and unpack data string values
"""


def data_to_s16(data):
    s16 = struct.unpack('>h', data[:2])
    return s16[0]


def data_to_u16(data):
    u16 = struct.unpack('>H', data[:2])
    return u16[0]


def data_to_s32(data):
    s32 = struct.unpack('>l', data[:4])
    return s32[0]


def data_to_u32(data):
    u32 = struct.unpack('>L', data[:4])
    return u32[0]


def data_to_s64(data):
    s64 = struct.unpack('>q', data[:8])
    return s64[0]


def data_to_u64(data):
    u64 = struct.unpack('>Q', data[:8])
    return u64[0]


def data_to_ipv6addr(data):
    value = False
    for i in data:
        if i != 0:
            value = True
            break
    if value and len(data) == 16:
        return '%02X%02X%02X%02X:%02X%02X%02X%02X:%02X%02X%02X%02X:%02X%02X%02X%02X' % (
            data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
            data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15])


def data_to_eui48(data):
    value = False
    for i in data:
        if i != 0:
            value = True
            break
    if value and len(data) == 8:
        return '%02X:%02X:%02X:%02X:%02X:%02X' % (
            data[2], data[3], data[4], data[5], data[6], data[7])


def data_to_f32(data):
    f = struct.unpack('>f', data[:4])
    if str(f[0]) != str(float('nan')):
        return f[0]


def data_to_f64(data):
    d = struct.unpack('>d', data[:8])
    if str(d[0]) != str(float('nan')):
        return d[0]


def data_to_str(data):
    data = str(data, 'utf-8')

    if len(data) > 1:
        data = data[0] + data[1:].rstrip('\0')
    return data


def s16_to_data(s16, len=None):
    return struct.pack('>h', s16)


def u16_to_data(u16, len=None):
    return struct.pack('>H', u16)


def s32_to_data(s32, len=None):
    return struct.pack('>l', s32)


def u32_to_data(u32, len=None):
    return struct.pack('>L', u32)


def s64_to_data(s64, len=None):
    return struct.pack('>q', s64)


def u64_to_data(u64, len=None):
    return struct.pack('>Q', u64)


def ipv6addr_to_data(addr, slen=None):
    s = base64.b16decode(addr.replace(':', ''))
    if slen is None:
        slen = len(s)
    return struct.pack(str(slen) + 's', s)


def f32_to_data(f, len=None):
    return struct.pack('>f', f)


def f64_to_data(f, len=None):
    return struct.pack('>d', f)


def str_to_data(s, slen=None):
    if slen is None:
        slen = len(s)
    s = bytes(s, 'utf-8')
    return struct.pack(str(slen) + 's', s)


def eui48_to_data(eui48):
    return (b'\x00\x00' + base64.b16decode(eui48.replace(':', '')))


def is_impl_int16(value):
    return not value == SUNS_UNIMPL_INT16


def is_impl_uint16(value):
    return not value == SUNS_UNIMPL_UINT16


def is_impl_acc16(value):
    return not value == SUNS_UNIMPL_ACC16


def is_impl_enum16(value):
    return not value == SUNS_UNIMPL_ENUM16


def is_impl_bitfield16(value):
    return not value == SUNS_UNIMPL_BITFIELD16


def is_impl_int32(value):
    return not value == SUNS_UNIMPL_INT32


def is_impl_uint32(value):
    return not value == SUNS_UNIMPL_UINT32


def is_impl_acc32(value):
    return not value == SUNS_UNIMPL_ACC32


def is_impl_enum32(value):
    return not value == SUNS_UNIMPL_ENUM32


def is_impl_bitfield32(value):
    return not value == SUNS_UNIMPL_BITFIELD32


def is_impl_ipaddr(value):
    return not value == SUNS_UNIMPL_IPADDR


def is_impl_int64(value):
    return not value == SUNS_UNIMPL_INT64


def is_impl_uint64(value):
    return not value == SUNS_UNIMPL_UINT64


def is_impl_acc64(value):
    return not value == SUNS_UNIMPL_ACC64


def is_impl_ipv6addr(value):
    if value:
        return not value[0] == '\0'
    return False


def is_impl_float32(value):
    return (value == value) and (value != None)


def is_impl_float64(value):
    return (value == value) and (value != None)


def is_impl_string(value):
    if value:
        return not value[0] == '\0'
    return False


def is_impl_sunssf(value):
    return not value == SUNS_UNIMPL_SUNSSF


def is_impl_eui48(value):
    return not value == SUNS_UNIMPL_EUI48


def is_impl_pad(value):
    return True


PointInfo = collections.namedtuple('PointInfo', 'len is_impl data_to to_data to_type default')
point_type_info = {
    mdef.TYPE_INT16: PointInfo(1, is_impl_int16, data_to_s16, s16_to_data, mdef.to_int, 0),
    mdef.TYPE_UINT16: PointInfo(1, is_impl_uint16, data_to_u16, u16_to_data, mdef.to_int, 0),
    mdef.TYPE_COUNT: PointInfo(1, is_impl_uint16, data_to_u16, u16_to_data, mdef.to_int, 0),
    mdef.TYPE_ACC16: PointInfo(1, is_impl_acc16, data_to_u16, u16_to_data, mdef.to_int, 0),
    mdef.TYPE_ENUM16: PointInfo(1, is_impl_enum16, data_to_u16, u16_to_data, mdef.to_int, 0),
    mdef.TYPE_BITFIELD16: PointInfo(1, is_impl_bitfield16, data_to_u16, u16_to_data, mdef.to_int, 0),
    mdef.TYPE_PAD: PointInfo(1, is_impl_pad, data_to_u16, u16_to_data, mdef.to_int, 0),
    mdef.TYPE_INT32: PointInfo(2, is_impl_int32, data_to_s32, s32_to_data, mdef.to_int, 0),
    mdef.TYPE_UINT32: PointInfo(2, is_impl_uint32, data_to_u32, u32_to_data, mdef.to_int, 0),
    mdef.TYPE_ACC32: PointInfo(2, is_impl_acc32, data_to_u32, u32_to_data, mdef.to_int, 0),
    mdef.TYPE_ENUM32: PointInfo(2, is_impl_enum32, data_to_u32, u32_to_data, mdef.to_int, 0),
    mdef.TYPE_BITFIELD32: PointInfo(2, is_impl_bitfield32, data_to_u32, u32_to_data, mdef.to_int, 0),
    mdef.TYPE_IPADDR: PointInfo(2, is_impl_ipaddr, data_to_u32, u32_to_data, mdef.to_int, 0),
    mdef.TYPE_INT64: PointInfo(4, is_impl_int64, data_to_s64, s64_to_data, mdef.to_int, 0),
    mdef.TYPE_UINT64: PointInfo(4, is_impl_uint64, data_to_u64, u64_to_data, mdef.to_int, 0),
    mdef.TYPE_ACC64: PointInfo(4, is_impl_acc64, data_to_u64, u64_to_data, mdef.to_int, 0),
    mdef.TYPE_IPV6ADDR: PointInfo(8, is_impl_ipv6addr, data_to_ipv6addr, ipv6addr_to_data, mdef.to_str, 0),
    mdef.TYPE_FLOAT32: PointInfo(2, is_impl_float32, data_to_f32, f32_to_data, mdef.to_float, 0),
    mdef.TYPE_FLOAT64: PointInfo(4, is_impl_float64, data_to_f64, f64_to_data, mdef.to_float, 0),
    mdef.TYPE_STRING: PointInfo(None, is_impl_string, data_to_str, str_to_data, mdef.to_str, ''),
    mdef.TYPE_SUNSSF: PointInfo(1, is_impl_sunssf, data_to_s16, s16_to_data, mdef.to_int, 0),
    mdef.TYPE_EUI48: PointInfo(4, is_impl_eui48, data_to_eui48, eui48_to_data, mdef.to_str, 0)
}
