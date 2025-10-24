# Test configuration and fixtures for R-Net AI Backend

import pytest
import os
import tempfile
import asyncio
from unittest.mock import patch

# Set test environment variables
os.environ["TESTING"] = "1"
os.environ["OPENAI_API_KEY"] = "test-api-key"
os.environ["LOG_LEVEL"] = "ERROR"  # Reduce log noise in tests

# Test settings
TEST_SETTINGS = {
    "openai_api_key": "test-api-key",
    "model_name": "gpt-4-vision-preview",
    "max_tokens": 1000,
    "temperature": 0.7,
    "max_file_size": 5242880,
    "debug": True
}

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir

@pytest.fixture(autouse=True)
def mock_settings():
    """Mock settings for all tests"""
    with patch('config.settings') as mock_settings:
        for key, value in TEST_SETTINGS.items():
            setattr(mock_settings, key, value)
        yield mock_settings