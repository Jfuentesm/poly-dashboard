import requests
import re
import pandas as pd
from datetime import datetime

# URL for Major Foreign Holders of Treasury Securities (Text File)
TIC_URL = "https://ticdata.treasury.gov/resource-center/data-chart-center/tic/Documents/mfh.txt"

def fetch_tic_data():
    print(f"Fetching TIC Data from {TIC_URL}...")
    try:
        response = requests.get(TIC_URL)
        response.raise_for_status()
        raw_text = response.text

        # Parse the text file
        # The file usually has a header section, then a table.
        # We need to find the lines for "China, Mainland" and "Japan".

        # Simple Regex to find country lines
        # Format often looks like: "Country Name      val1   val2   val3 ..."

        lines = raw_text.split('\n')

        # Look for the date header to understand the "Latest" column
        # Usually the last column is the most recent.

        china_line = None
        japan_line = None

        for line in lines:
            if "China, Mainland" in line:
                china_line = line
            if "Japan" in line:
                japan_line = line

        print("\n--- Granular Country Data (Scraped) ---")
        if china_line:
            # Extract the last number in the line (assuming it's the latest holdings)
            # Lines are often space-delimited
            parts = china_line.split()
            # The country name might be split, but the numbers are at the end.
            latest_val = parts[-1]
            print(f"China Holdings: ${latest_val} Billion")
        else:
            print("Could not find 'China, Mainland' in TIC file.")

        if japan_line:
            parts = japan_line.split()
            latest_val = parts[-1]
            print(f"Japan Holdings: ${latest_val} Billion")
        else:
            print("Could not find 'Japan' in TIC file.")

    except Exception as e:
        print(f"Error fetching TIC data: {e}")

def fetch_fred_proxy():
    print("\n--- FRED Proxy Data ---")
    # FDHBFIN: Federal Debt Held by Foreign and International Investors
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=FDHBFIN"
    try:
        df = pd.read_csv(url, index_col=0, parse_dates=True)
        latest_val = df['FDHBFIN'].iloc[-1]
        print(f"Total Foreign Holdings (FRED FDHBFIN): ${latest_val} Billion")
    except Exception as e:
        print(f"Error fetching FRED proxy: {e}")

if __name__ == "__main__":
    fetch_tic_data()
    fetch_fred_proxy()
