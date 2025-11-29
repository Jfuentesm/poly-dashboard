import pytest
from unittest.mock import MagicMock
from fetch_gold_data import fetch_gold_data

def test_fetch_gold_data_success(mock_requests_get):
    # Mock WB JSON response
    # [metadata, [data_points]]
    mock_json = [
        {"page": 1},
        [
            {"date": "2024", "value": 3400000000000}, # 3.4 Trillion
            {"date": "2023", "value": 3200000000000}
        ]
    ]

    mock_response = MagicMock()
    mock_response.json.return_value = mock_json
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response

    result = fetch_gold_data()

    assert result is not None
    # 3.4 Trillion / 1e12 = 3.4
    assert result['value'] == 3.4
    assert result['year'] == "2024"

def test_fetch_gold_data_empty(mock_requests_get):
    mock_json = [{"page": 1}, []]
    mock_response = MagicMock()
    mock_response.json.return_value = mock_json
    mock_requests_get.return_value = mock_response

    result = fetch_gold_data()
    assert result is None
