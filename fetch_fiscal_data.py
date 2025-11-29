import pandas as pd
import requests
import io

# Define the FRED Series IDs
SERIES_MAP = {
    'Revenue': 'W006RC1Q027SBEA',        # Current Receipts
    'Interest': 'A091RC1Q027SBEA',       # Interest Payments
    'SocialSecurity': 'W823RC1',         # Social Security
    'Medicare': 'W824RC1',               # Medicare
    'Medicaid': 'W825RC1',               # Medicaid
    'PublicDebt_GDP': 'GFDEGDQ188S',     # Federal Debt: Total Public Debt as Percent of GDP
    'FedBalanceSheet': 'WALCL',          # Assets: Total Assets: Total Assets (Less Eliminations from Consolidation)
    'Yield10Y': 'GS10',                  # 10-Year Treasury Constant Maturity Rate
    'Yield2Y': 'GS2'                     # 2-Year Treasury Constant Maturity Rate
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
            print(f"Warning: Failed to fetch {name} ({series_id})")

    if not data_frames:
        print("Failed to fetch data.")
        return None

    # Merge all series into a single DataFrame
    # Note: Different series have different frequencies (Weekly, Monthly, Quarterly).
    # We will forward-fill to match the most frequent or standard frequency for analysis.
    df = pd.DataFrame(data_frames)

    # Forward fill to handle different frequencies (e.g. Weekly WALCL vs Quarterly GDP)
    df.ffill(inplace=True)

    # Fill NA if needed, or drop rows that are still NaN (start of data)
    df.dropna(inplace=True)

    if df.empty:
        return None

    # Calculate Mandatory Spending Proxy and KPIs
    try:
        # Mandatory Spending Proxy
        df['Mandatory_Proxy'] = df['SocialSecurity'] + df['Medicare'] + df['Medicaid']

        # KPI 1: Fiscal Unsustainability Ratio
        # (Mandatory + Interest) / Revenue
        df['Fiscal_Unsustainability_Ratio'] = (df['Mandatory_Proxy'] + df['Interest']) / df['Revenue']

        # KPI 2: Interest Burden (Interest / Revenue)
        df['Interest_Revenue_Ratio'] = df['Interest'] / df['Revenue']

        # KPI 3: Public Debt Burden (Directly from FRED 'PublicDebt_GDP')
        # Already in df['PublicDebt_GDP']

        # KPI 4: Debt Monetization Proxy (Fed Balance Sheet Growth)
        # We can use raw level 'FedBalanceSheet' or calculate YoY change
        df['FedBalanceSheet_YoY'] = df['FedBalanceSheet'].pct_change(periods=52) # approx 1 year for weekly data

    except KeyError as e:
        print(f"Missing columns for calculation: {e}")
        return None

    return df

if __name__ == "__main__":
    df = fetch_fiscal_data()
    if df is not None:
        print("\nLatest Fiscal Data (Snapshot):")
        print(df.tail(1).T)

        print(f"\nFiscal Unsustainability Ratio: {df['Fiscal_Unsustainability_Ratio'].iloc[-1]:.2%}")
        print(f"Public Debt to GDP: {df['PublicDebt_GDP'].iloc[-1]:.2f}%")
        print(f"Fed Balance Sheet: ${df['FedBalanceSheet'].iloc[-1]:,.0f} Million")
        print(f"10Y Yield: {df['Yield10Y'].iloc[-1]:.2f}%")
