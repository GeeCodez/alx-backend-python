import pytest

def test_sample():
    """simple test to verify pytest is working """
    assert 1 + 1=w

def test_django_setup():
    """Test that django is properly configured """
    from django.conf import settings
    assert settings.configured