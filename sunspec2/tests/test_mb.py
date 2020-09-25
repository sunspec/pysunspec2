import sunspec2.mb as mb
import pytest


def test_create_unimpl_value():
    with pytest.raises(ValueError):
        mb.create_unimpl_value(None)

    with pytest.raises(ValueError):
        mb.create_unimpl_value('string')

    assert mb.create_unimpl_value('string', len=8) == b'\x00\x00\x00\x00\x00\x00\x00\x00'
    assert mb.create_unimpl_value('ipv6addr') == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    assert mb.create_unimpl_value('int16') == b'\x80\x00'
    assert mb.create_unimpl_value('uint16') == b'\xff\xff'
    assert mb.create_unimpl_value('acc16') == b'\x00\x00'
    assert mb.create_unimpl_value('enum16') == b'\xff\xff'
    assert mb.create_unimpl_value('bitfield16') == b'\xff\xff'
    assert mb.create_unimpl_value('int32') == b'\x80\x00\x00\x00'
    assert mb.create_unimpl_value('uint32') == b'\xff\xff\xff\xff'
    assert mb.create_unimpl_value('acc32') == b'\x00\x00\x00\x00'
    assert mb.create_unimpl_value('enum32') == b'\xff\xff\xff\xff'
    assert mb.create_unimpl_value('bitfield32') == b'\xff\xff\xff\xff'
    assert mb.create_unimpl_value('ipaddr') == b'\x00\x00\x00\x00'
    assert mb.create_unimpl_value('int64') == b'\x80\x00\x00\x00\x00\x00\x00\x00'
    assert mb.create_unimpl_value('uint64') == b'\xff\xff\xff\xff\xff\xff\xff\xff'
    assert mb.create_unimpl_value('acc64') == b'\x00\x00\x00\x00\x00\x00\x00\x00'
    assert mb.create_unimpl_value('float32') == b'N\xff\x80\x00'
    assert mb.create_unimpl_value('sunssf') == b'\x80\x00'
    assert mb.create_unimpl_value('eui48') == b'\x00\x00\xff\xff\xff\xff\xff\xff'
    assert mb.create_unimpl_value('pad') == b'\x00\x00'


def test_data_to_s16():
    assert mb.data_to_s16(b'\x13\x88') == 5000


def test_data_to_u16():
    assert mb.data_to_u16(b'\x27\x10') == 10000


def test_data_to_s32():
    assert mb.data_to_s32(b'\x12\x34\x56\x78') == 305419896
    assert mb.data_to_s32(b'\xED\xCB\xA9\x88') == -305419896


def test_data_to_u32():
    assert mb.data_to_u32(b'\x12\x34\x56\x78') == 305419896


def test_data_to_s64():
    assert mb.data_to_s64(b'\x12\x34\x56\x78\x12\x34\x56\x78') == 1311768465173141112
    assert mb.data_to_s64(b'\xED\xCB\xA9\x87\xED\xCB\xA9\x88') == -1311768465173141112


def test_data_to_u64():
    assert mb.data_to_u64(b'\xff\xff\xff\xff\xff\xff\xff\xff') == 18446744073709551615


def test_data_to_ipv6addr():
    assert mb.data_to_ipv6addr(b'\x20\x01\x0d\xb8\x85\xa3\x00\x00\x00\x00\x8a\x2e\x03\x70\x73\x34') == '20010DB8:85A30000:00008A2E:03707334'


def test_data_to_eui48():
    # need test to test for python 2
    assert mb.data_to_eui48(b'\x00\x00\x12\x34\x56\x78\x90\xAB') == '12:34:56:78:90:AB'


def test_data_to_f64():
    assert mb.data_to_f64(b'\x44\x9a\x43\xf3\x00\x00\x00\x00') == 3.1008742600725133e+22


def test_data_to_str():
    assert mb.data_to_str(b'test') == 'test'
    assert mb.data_to_str(b'444444') == '444444'


def test_s16_to_data():
    assert mb.s16_to_data(5000) == b'\x13\x88'


def test_u16_to_data():
    assert mb.u16_to_data(10000) == b'\x27\x10'


def test_s32_to_data():
    assert mb.s32_to_data(305419896) == b'\x12\x34\x56\x78'
    assert mb.s32_to_data(-305419896) == b'\xED\xCB\xA9\x88'


def test_u32_to_data():
    assert mb.u32_to_data(305419896) == b'\x12\x34\x56\x78'


def test_s64_to_data():
    assert mb.s64_to_data(1311768465173141112) == b'\x12\x34\x56\x78\x12\x34\x56\x78'
    assert mb.s64_to_data(-1311768465173141112) == b'\xED\xCB\xA9\x87\xED\xCB\xA9\x88'


def test_u64_to_data():
    assert mb.u64_to_data(18446744073709551615) == b'\xff\xff\xff\xff\xff\xff\xff\xff'


def test_ipv6addr_to_data():
    assert mb.ipv6addr_to_data('20010DB8:85A30000:00008A2E:03707334') == \
           b'\x20\x01\x0d\xb8\x85\xa3\x00\x00\x00\x00\x8a\x2e\x03\x70\x73\x34'
    # need additional test to test for python 2


def test_f32_to_data():
    assert mb.f32_to_data(32500.43359375) == b'F\xfd\xe8\xde'


def test_f64_to_data():
    assert mb.f64_to_data(3.1008742600725133e+22) == b'\x44\x9a\x43\xf3\x00\x00\x00\x00'


def test_str_to_data():
    assert mb.str_to_data('test') == b'test'
    assert mb.str_to_data('444444') == b'444444'
    assert mb.str_to_data('test', 5) == b'test\x00'


def test_eui48_to_data():
    assert mb.eui48_to_data('12:34:56:78:90:AB') == b'\x00\x00\x12\x34\x56\x78\x90\xAB'


def test_is_impl_int16():
    assert not mb.is_impl_int16(-32768)
    assert mb.is_impl_int16(1111)
    assert mb.is_impl_int16(None)


def test_is_impl_uint16():
    assert not mb.is_impl_uint16(0xffff)
    assert mb.is_impl_uint16(0x1111)


def test_is_impl_acc16():
    assert not mb.is_impl_acc16(0)
    assert mb.is_impl_acc16(1111)


def test_is_impl_enum16():
    assert not mb.is_impl_enum16(0xffff)
    assert mb.is_impl_enum16(0x1111)


def test_is_impl_bitfield16():
    assert not mb.is_impl_bitfield16(0xffff)
    assert mb.is_impl_bitfield16(0x1111)


def test_is_impl_int32():
    assert not mb.is_impl_int32(-2147483648)
    assert mb.is_impl_int32(1111111)


def test_is_impl_uint32():
    assert not mb.is_impl_uint32(0xffffffff)
    assert mb.is_impl_uint32(0x11111111)


def test_is_impl_acc32():
    assert not mb.is_impl_acc32(0)
    assert mb.is_impl_acc32(1)


def test_is_impl_enum32():
    assert not mb.is_impl_enum32(0xffffffff)
    assert mb.is_impl_enum32(0x11111111)


def test_is_impl_bitfield32():
    assert not mb.is_impl_bitfield32(0xffffffff)
    assert mb.is_impl_bitfield32(0x11111111)


def test_is_impl_ipaddr():
    assert not mb.is_impl_ipaddr(0)
    assert mb.is_impl_ipaddr('192.168.0.1')


def test_is_impl_int64():
    assert not mb.is_impl_int64(-9223372036854775808)
    assert mb.is_impl_int64(111111111111111)


def test_is_impl_uint64():
    assert not mb.is_impl_uint64(0xffffffffffffffff)
    assert mb.is_impl_uint64(0x1111111111111111)


def test_is_impl_acc64():
    assert not mb.is_impl_acc64(0)
    assert mb.is_impl_acc64(1)


def test_is_impl_ipv6addr():
    assert not mb.is_impl_ipv6addr('\0')
    assert mb.is_impl_ipv6addr(b'\x20\x01\x0d\xb8\x85\xa3\x00\x00\x00\x00\x8a\x2e\x03\x70\x73\x34')


def test_is_impl_float32():
    assert not mb.is_impl_float32(None)
    assert mb.is_impl_float32(0x123456)


def test_is_impl_string():
    assert not mb.is_impl_string('\0')
    assert mb.is_impl_string(b'\x74\x65\x73\x74')


def test_is_impl_sunssf():
    assert not mb.is_impl_sunssf(-32768)
    assert mb.is_impl_sunssf(30000)


def test_is_impl_eui48():
    assert not mb.is_impl_eui48('FF:FF:FF:FF:FF:FF')
    assert mb.is_impl_eui48('00:00:00:00:00:00')
