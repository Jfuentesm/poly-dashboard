import pytest
from unittest.mock import MagicMock
from fetch_gdelt_news import fetch_gdelt_mentions

def test_fetch_gdelt_mentions_success(mock_requests_get):
    # Mock JSON response
    mock_json = {
        "articles": [
            {"title": "Tariffs are rising", "url": "http://example.com"}
        ]
    }

    mock_response = MagicMock()
    mock_response.json.return_value = mock_json
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response

    results = fetch_gdelt_mentions()

    assert results is not None
    assert "Tariffs" in results
    assert len(results["Tariffs"]) == 1
    assert results["Tariffs"][0]['title'] == "Tariffs are rising"

def test_fetch_gdelt_mentions_empty(mock_requests_get):
    mock_json = {}
    mock_response = MagicMock()
    mock_response.json.return_value = mock_json
    mock_requests_get.return_value = mock_response

    results = fetch_gdelt_mentions()
    assert results["Tariffs"] == []
