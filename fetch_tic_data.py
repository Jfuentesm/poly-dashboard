import requests
import re
import pandas as pd
from datetime import datetime
import io

# URL for Major Foreign Holders of Treasury Securities (Text File)
TIC_URL = "https://ticdata.treasury.gov/resource-center/data-chart-center/tic/Documents/mfh.txt"

def fetch_tic_data():
    """
    Fetches TIC data and returns a dictionary with the results.
    Returns:
        dict: containing 'China', 'Japan' holdings (in Billions) or None if failed.
    """
    print(f"Fetching TIC Data from {TIC_URL}...")
    results = {}

    try:
        response = requests.get(TIC_URL)
        response.raise_for_status()
        raw_text = response.text

        lines = raw_text.split('\n')

        china_line = None
        japan_line = None

        for line in lines:
            if "China, Mainland" in line:
                china_line = line
            if "Japan" in line:
                japan_line = line

        if china_line:
            parts = china_line.split()
            results['China'] = parts[-1]

        if japan_line:
            parts = japan_line.split()
            results['Japan'] = parts[-1]

    except Exception as e:
        print(f"Error fetching TIC data: {e}")
        return None

    return results

def fetch_fred_proxy():
    """
    Fetches FRED proxy data for total foreign holdings.
    Returns:
        float: Total holdings in Billions, or None.
    """
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=FDHBFIN"
    try:
        # Refactored to use requests so it can be mocked easily
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text), index_col=0, parse_dates=True)
        latest_val = df['FDHBFIN'].iloc[-1]
        return latest_val
    except Exception as e:
        print(f"Error fetching FRED proxy: {e}")
        return None

if __name__ == "__main__":
    tic_data = fetch_tic_data()
    print("\n--- Granular Country Data (Scraped) ---")
    if tic_data:
        if 'China' in tic_data:
            print(f"China Holdings: ${tic_data['China']} Billion")
        else:
            print("Could not find 'China, Mainland' in TIC file.")

        if 'Japan' in tic_data:
            print(f"Japan Holdings: ${tic_data['Japan']} Billion")
        else:
            print("Could not find 'Japan' in TIC file.")
    else:
        print("Failed to fetch TIC data.")

    print("\n--- FRED Proxy Data ---")
    fred_val = fetch_fred_proxy()
    if fred_val:
        print(f"Total Foreign Holdings (FRED FDHBFIN): ${fred_val} Billion")
