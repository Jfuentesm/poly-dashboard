import pandas as pd
import requests
import io
import yfinance as yf
from fetch_tic_data import fetch_tic_data, fetch_fred_proxy
from fetch_gold_data import fetch_gold_data

# FRED Series ID for Dollar Index
DXY_SERIES = 'DTWEXBGS' # Trade Weighted U.S. Dollar Index: Broad, Goods and Services

def fetch_dollar_index():
    """
    Fetches the Trade Weighted U.S. Dollar Index from FRED.
    """
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={DXY_SERIES}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text), index_col=0, parse_dates=True)
        return df
    except Exception as e:
        print(f"Error fetching Dollar Index: {e}")
        return None

def fetch_neutral_assets():
    """
    Fetches Gold and Bitcoin prices from Yahoo Finance.
    """
    tickers = ["GC=F", "BTC-USD"]
    try:
        data = yf.download(tickers, period="1y", progress=False, auto_adjust=True)['Close']
        return data
    except Exception as e:
        print(f"Error fetching Neutral Assets: {e}")
        return None

def fetch_module_2_data():
    """
    Aggregates all data for Module 2: De-Dollarization.
    """
    print("Fetching Module 2 Data (De-Dollarization)...")

    # 1. Foreign Confidence (TIC Data)
    tic_data = fetch_tic_data()
    fred_tic = fetch_fred_proxy()

    # 2. Central Bank Flight (Gold Reserves - China Proxy)
    gold_reserves = fetch_gold_data()

    # 3. U.S. Dollar Dominance
    dxy_data = fetch_dollar_index()

    # 4. Performance of Neutral Assets
    neutral_assets = fetch_neutral_assets()

    results = {
        'Foreign_Confidence_TIC': tic_data,
        'Foreign_Confidence_Total': fred_tic,
        'China_Gold_Reserves': gold_reserves,
        'Dollar_Index': dxy_data.iloc[-1].item() if dxy_data is not None and not dxy_data.empty else None,
        'Gold_Price': neutral_assets['GC=F'].iloc[-1] if neutral_assets is not None else None,
        'Bitcoin_Price': neutral_assets['BTC-USD'].iloc[-1] if neutral_assets is not None else None
    }

    return results

if __name__ == "__main__":
    data = fetch_module_2_data()

    print("\n--- Module 2: De-Dollarization Dashboard ---")

    if data['Foreign_Confidence_TIC']:
        print(f"China US Debt Holdings: ${data['Foreign_Confidence_TIC'].get('China', 'N/A')} Billion")
        print(f"Japan US Debt Holdings: ${data['Foreign_Confidence_TIC'].get('Japan', 'N/A')} Billion")

    if data['Foreign_Confidence_Total']:
        print(f"Total Foreign US Debt Holdings (FRED): ${data['Foreign_Confidence_Total']} Billion")

    if data['China_Gold_Reserves']:
        print(f"China Gold Reserves: ${data['China_Gold_Reserves']['value']:.2f} Trillion")

    if data['Dollar_Index']:
        print(f"Trade Weighted USD Index: {data['Dollar_Index']:.2f}")

    if data['Gold_Price']:
        print(f"Gold Price: ${data['Gold_Price']:.2f}")

    if data['Bitcoin_Price']:
        print(f"Bitcoin Price: ${data['Bitcoin_Price']:.2f}")
