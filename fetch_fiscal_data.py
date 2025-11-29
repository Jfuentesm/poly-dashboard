import pandas as pd
import requests
import io

# Define the FRED Series IDs
SERIES_MAP = {
    'Revenue': 'W006RC1Q027SBEA',
    'Interest': 'A091RC1Q027SBEA',
    'SocialSecurity': 'W823RC1',
    'Medicare': 'W824RC1',
    'Medicaid': 'W825RC1'
}

def fetch_fred_series_csv(series_id):
    """Fetches a FRED series as a pandas Series using the direct CSV URL."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text), index_col=0, parse_dates=True)
        # Check if column exists, otherwise it might be 'VALUE' or something else if mocked imperfectly
        if series_id in df.columns:
            return df[series_id]
        elif 'VALUE' in df.columns:
             return df['VALUE']
        else:
             # If index only, or weird format
             return df.iloc[:, 0]
    except Exception as e:
        print(f"Error fetching {series_id}: {e}")
        return None

def fetch_fiscal_data():
    """
    Fetches fiscal data from FRED.
    Returns:
        pd.DataFrame: DataFrame with all series and calculated KPIs, or None if failure.
    """
    print("Fetching Fiscal Data from FRED (CSV method)...")

    data_frames = {}
    for name, series_id in SERIES_MAP.items():
        s = fetch_fred_series_csv(series_id)
        if s is not None:
            data_frames[name] = s
        else:
            # If any critical series fails, we might want to return None or Partial
            # For now, let's continue but if empty return None
            pass

    if not data_frames:
        print("Failed to fetch data.")
        return None

    df = pd.DataFrame(data_frames)

    # Fill NA if needed, or drop
    df.dropna(inplace=True)

    if df.empty:
        return None

    # Calculate Mandatory Spending Proxy
    try:
        df['Mandatory_Proxy'] = df['SocialSecurity'] + df['Medicare'] + df['Medicaid']

        # Calculate KPIs
        # Note: These are billions of USD. Ratios are unitless.
        df['Fiscal_Unsustainability_Ratio'] = (df['Mandatory_Proxy'] + df['Interest']) / df['Revenue']
        df['Interest_Revenue_Ratio'] = df['Interest'] / df['Revenue']
    except KeyError as e:
        print(f"Missing columns for calculation: {e}")
        return None

    return df

if __name__ == "__main__":
    df = fetch_fiscal_data()
    if df is not None:
        print("\nLatest Fiscal Data (Annualized Rate, Billions USD):")
        print(df.tail(1))

        print("\nFiscal Unsustainability Ratio (Latest):")
        val = df['Fiscal_Unsustainability_Ratio'].iloc[-1]
        print(f"{val:.2%}")
