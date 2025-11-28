import pytest
from unittest.mock import MagicMock
from fetch_tic_data import fetch_tic_data, fetch_fred_proxy

def test_fetch_tic_data_parsing(mock_requests_get):
    mock_text = """
    Major Foreign Holders of Treasury Securities
    (in billions of dollars)

    Country          Jan    Feb    Mar
    China, Mainland  800.1  800.5  850.2
    Japan            1100.1 1100.2 1150.5
    UK               500.0  500.0  500.0
    """

    mock_response = MagicMock()
    mock_response.text = mock_text
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response

    result = fetch_tic_data()

    assert result is not None
    assert result['China'] == "850.2"
    assert result['Japan'] == "1150.5"

def test_fetch_tic_data_failure(mock_requests_get):
    mock_requests_get.side_effect = Exception("Site Down")
    result = fetch_tic_data()
    assert result is None

def test_fetch_fred_proxy(mock_requests_get):
    mock_csv = """DATE,FDHBFIN
2024-01-01,7500.5
"""
    mock_response = MagicMock()
    mock_response.text = mock_csv
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response

    val = fetch_fred_proxy()
    assert val == 7500.5
