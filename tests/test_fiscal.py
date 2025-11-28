import pytest
import pandas as pd
from io import StringIO
from unittest.mock import MagicMock
from fetch_fiscal_data import fetch_fiscal_data

def test_fetch_fiscal_data_success(mock_requests_get):
    # The function calls requests.get multiple times for different IDs.
    # We need to ensure the returned mock CSV has the correct column name for the requested ID.

    def side_effect(url):
        # Extract series_id from url
        # url is like "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES_ID"
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        series_id = params.get('id', ['VALUE'])[0]

        mock_csv_data = f"""DATE,{series_id}
2023-01-01,1000.0
2024-01-01,1200.0
"""
        mock_resp = MagicMock()
        mock_resp.text = mock_csv_data
        mock_resp.status_code = 200
        return mock_resp

    mock_requests_get.side_effect = side_effect

    # Run the function
    df = fetch_fiscal_data()

    # Verify
    assert df is not None
    assert not df.empty
    # We expect columns like 'Revenue', 'Interest', 'Mandatory_Proxy'
    assert 'Revenue' in df.columns
    assert 'Fiscal_Unsustainability_Ratio' in df.columns

    # Since we returned same value (1200) for all inputs:
    # Mandatory Proxy = SocSec(1200) + Medicare(1200) + Medicaid(1200) = 3600
    # Interest = 1200
    # Revenue = 1200
    # Ratio = (3600 + 1200) / 1200 = 4800 / 1200 = 4.0

    last_row = df.iloc[-1]
    assert last_row['Mandatory_Proxy'] == 3600.0
    assert last_row['Fiscal_Unsustainability_Ratio'] == 4.0

def test_fetch_fiscal_data_failure(mock_requests_get):
    mock_requests_get.side_effect = Exception("API Down")

    df = fetch_fiscal_data()
    assert df is None
