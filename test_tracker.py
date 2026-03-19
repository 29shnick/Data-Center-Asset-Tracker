import pytest
from main import validate_ip

def test_valid_ipv4():
    """Test that a standard IPv4 address passes."""
    assert validate_ip("192.168.1.1") == "192.168.1.1"

def test_valid_ipv6():
    """Test that a complex IPv6 address is normalized."""
    raw_v6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    expected = "2001:db8:85a3::8a2e:370:7334"
    assert validate_ip(raw_v6) == expected

def test_invalid_ip():
    """Test that garbage strings return None."""
    assert validate_ip("not-an-ip-address") is None
    assert validate_ip("10.0.0.999") is None

def test_whitespace_handling():
    """Test that the function strips accidental spaces."""
    assert validate_ip("  10.0.0.1  ") == "10.0.0.1"
