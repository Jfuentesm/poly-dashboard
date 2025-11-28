import pytest
import pandas as pd
from fetch_energy_money import fetch_energy_money

def test_fetch_energy_money_calculation(mock_yfinance_download):
    # Mock DataFrame return from yfinance
    # Close prices for 2 days
    data_dict = {
        ('Close', 'CL=F'): [70.0, 75.0],
        ('Close', '^TNX'): [4.0, 4.20] # Represents 4.0% and 4.20%
    }
    # yfinance returns MultiIndex columns by default now often, but we access ['Close'] in code
    # The code does: data = yf.download(...)['Close']
    # So we should return a DF that represents that 'Close' slice or the full DF

    # Let's mock the full DF returned by download
    # It has a MultiIndex columns
    arrays = [['Close', 'Close'], ['CL=F', '^TNX']]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples, names=['Price', 'Ticker'])

    df = pd.DataFrame([[70.0, 4.0], [75.0, 4.20]], columns=index)

    # When code calls ['Close'], it gets the Close level
    mock_yfinance_download.return_value = df

    result = fetch_energy_money()

    assert result is not None
    assert result['Oil_Price'] == 75.0

    # 4.20 should be converted to 0.042
    assert result['10Y_Yield'] == 0.042

    # Check Bond Price Calculation
    # Price = 100 / (1 + 0.042)^10
    expected_bond_price = 100 / ((1.042) ** 10)
    assert result['Bond_Price'] == expected_bond_price

    # Check Energy Value
    expected_energy_value = expected_bond_price / 75.0
    assert result['Energy_Value'] == expected_energy_value

def test_fetch_energy_money_failure(mock_yfinance_download):
    mock_yfinance_download.side_effect = Exception("API Error")
    result = fetch_energy_money()
    assert result is None
