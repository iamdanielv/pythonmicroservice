"""Tests for the configuration"""

from src.config import Settings


def test_settings():
    """Test the Settings class"""
    # Test with default settings
    settings = Settings()
    assert settings.environment == "dev"
    assert settings.is_prod is False

    # Test with prod environment
    settings = Settings(environment="prod")
    assert settings.is_prod is True
