import yfinance as yf
import pandas as pd

def fetch_energy_money():
    print("Fetching Market Data via yfinance...")

    # Symbols
    # Oil: CL=F (WTI Crude Oil Futures)
    # 10Y Yield: ^TNX (CBOE Interest Rate 10 Year T Note).
    # Note: ^TNX value is usually yield * 10 (e.g., 42.50 = 4.25%)

    tickers = ["CL=F", "^TNX"]

    try:
        # Fetch last 1 year of data
        data = yf.download(tickers, period="1y", progress=False)['Close']

        # Extract series
        oil_price = data['CL=F']
        tnx_yield_index = data['^TNX']

        # Convert TNX to actual yield decimal
        # Standard: ^TNX at 42.50 is 4.25%.
        # So divide by 10 to get percent, then by 100 to get decimal. Total divide by 1000.
        treasury_yield = tnx_yield_index / 1000.0

        # Calculate "Price of Theoretical 10Y Zero Coupon Bond" (Face 100)
        # Price = 100 / (1 + r)^10
        bond_price = 100 / ((1 + treasury_yield) ** 10)

        # Metric: Barrels of Oil per Bond
        # This represents how much real-world energy the "safe asset" can purchase.
        energy_value = bond_price / oil_price

        print("\nLatest Data:")
        print(f"Oil Price (WTI): ${oil_price.iloc[-1]:.2f}")
        print(f"10Y Yield: {treasury_yield.iloc[-1]:.2%}")
        print(f"Theoretical Bond Price: ${bond_price.iloc[-1]:.2f}")

        print(f"\nEnergy-Value of Money (Barrels of Oil per 10Y Bond):")
        print(f"{energy_value.iloc[-1]:.2f} Barrels")

    except Exception as e:
        print(f"Error fetching market data: {e}")

if __name__ == "__main__":
    fetch_energy_money()
