import pytest
from app.services.auth_service import hash_password, verify_password

def test_password_hash_and_verify():
    raw_password = "test123"
    hashed = hash_password(raw_password)

    assert hashed != raw_password  # Password should be hashed
    assert verify_password(raw_password, hashed) is True  # Should verify correctly
    assert verify_password("wrongpass", hashed) is False  # Should fail on wrong input