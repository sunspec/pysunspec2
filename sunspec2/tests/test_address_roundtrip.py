"""Address-value regressions from issue #125, through public Point conversion."""
import pytest

from sunspec2 import device, mb


@pytest.mark.parametrize('text', [
    '2001:db8::1',
    '2001:0DB8:0000:0000:0000:0000:0000:0001',
    '20010DB8:00000000:00000000:00000001',
    '20010db8:00000000:00000000:00000001',
    '20010db8000000000000000000000001',
])
def test_ipv6_point_roundtrip(text):
    wire = bytes.fromhex('20010db8000000000000000000000001')
    point = device.Point({'name': 'Address', 'type': 'ipv6addr'})
    point.value = text
    assert point.get_mb() == wire
    point.set_mb(wire)
    assert point.cvalue == '2001:db8::1'
    assert point.get_mb() == wire


@pytest.mark.parametrize('text', ['::1', '::ffff:192.0.2.1', 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'])
def test_ipv6_standard_forms(text):
    import ipaddress
    wire = ipaddress.IPv6Address(text).packed
    assert mb.ipv6addr_to_data(text) == wire
    assert mb.data_to_ipv6addr(wire) == str(ipaddress.IPv6Address(text))


@pytest.mark.parametrize('text', ['not an address', '2001:db8::1::2', '12345::1', '2001:db8', '192.0.2.1'])
def test_invalid_ipv6_is_rejected(text):
    with pytest.raises(ValueError):
        mb.ipv6addr_to_data(text)


def test_ipv6_unimplemented_value_is_preserved():
    point = device.Point({'name': 'Address', 'type': 'ipv6addr'})
    point.set_mb(bytes(16))
    assert point.value is None
    assert not point.is_impl()
    assert point.get_mb() == bytes(16)


@pytest.mark.parametrize('text', ['00:00:00:00:00:00', 'b8:27:eb:12:34:56', 'B8:27:EB:12:34:56'])
def test_eui48_point_roundtrip(text):
    wire = bytes(2) + bytes.fromhex(text.replace(':', ''))
    point = device.Point({'name': 'Address', 'type': 'eui48'})
    point.set_mb(wire)
    assert point.value == text.upper()
    assert point.is_impl()
    point.value = text
    assert point.get_mb() == wire


def test_eui48_unimplemented_value_is_preserved():
    point = device.Point({'name': 'Address', 'type': 'eui48'})
    point.set_mb(bytes(2) + b'\xff' * 6)
    assert point.value is None
    assert not point.is_impl()
    assert point.get_mb() == bytes(2) + b'\xff' * 6
