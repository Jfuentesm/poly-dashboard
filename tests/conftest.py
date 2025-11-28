import pytest
from unittest.mock import MagicMock
import sys
import os

# Add root directory to path so we can import fetch scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch("requests.get")

@pytest.fixture
def mock_yfinance_download(mocker):
    return mocker.patch("yfinance.download")
