import yfinance as yf
import pandas as pd

def fetch_energy_money():
    """
    Fetches Oil and Treasury Yield data to calculate Energy-Value of Money.
    Returns:
        dict: containing 'Oil_Price', '10Y_Yield', 'Bond_Price', 'Energy_Value' or None.
    """
    print("Fetching Market Data via yfinance...")

    tickers = ["CL=F", "^TNX"]

    try:
        # Fetch last 1 year of data
        # Fix: explicit auto_adjust=True to silence warning
        data = yf.download(tickers, period="1y", progress=False, auto_adjust=True)['Close']

        oil_price = data['CL=F'].iloc[-1]
        tnx_yield_index = data['^TNX'].iloc[-1]

        # Convert TNX to actual yield decimal
        # Verified: Raw ^TNX is percentage (e.g. 4.02 for 4.02%)
        treasury_yield = tnx_yield_index / 100.0

        # Calculate "Price of Theoretical 10Y Zero Coupon Bond" (Face 100)
        bond_price = 100 / ((1 + treasury_yield) ** 10)

        # Metric: Barrels of Oil per Bond
        energy_value = bond_price / oil_price

        return {
            'Oil_Price': oil_price,
            '10Y_Yield': treasury_yield,
            'Bond_Price': bond_price,
            'Energy_Value': energy_value
        }

    except Exception as e:
        print(f"Error fetching market data: {e}")
        return None

if __name__ == "__main__":
    res = fetch_energy_money()
    if res:
        print("\nLatest Data:")
        print(f"Oil Price (WTI): ${res['Oil_Price']:.2f}")
        print(f"10Y Yield: {res['10Y_Yield']:.2%}")
        print(f"Theoretical Bond Price: ${res['Bond_Price']:.2f}")

        print(f"\nEnergy-Value of Money (Barrels of Oil per 10Y Bond):")
        print(f"{res['Energy_Value']:.2f} Barrels")
    else:
        print("Failed to fetch energy money data.")
