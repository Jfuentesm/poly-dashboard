import yfinance as yf
import pandas as pd
import requests
import io

def fetch_energy_money_data():
    """
    Fetches Oil and Treasury Yield data to calculate Energy-Value of Money.
    Reused from original fetch_energy_money.py logic.
    """
    tickers = ["CL=F", "^TNX"]
    try:
        data = yf.download(tickers, period="1y", progress=False, auto_adjust=True)['Close']

        # Check if data is valid
        if data.empty or 'CL=F' not in data or '^TNX' not in data:
            return None

        oil_price = data['CL=F'].iloc[-1]
        tnx_yield_index = data['^TNX'].iloc[-1]
        treasury_yield = tnx_yield_index / 100.0
        bond_price = 100 / ((1 + treasury_yield) ** 10)
        energy_value = bond_price / oil_price

        return {
            'Oil_Price': oil_price,
            '10Y_Yield': treasury_yield,
            'Bond_Price': bond_price,
            'Energy_Value': energy_value
        }
    except Exception as e:
        print(f"Error fetching Energy-Money data: {e}")
        return None

def fetch_commodity_prices():
    """
    Fetches Copper and Food (Wheat/Corn) prices.
    """
    # HG=F: Copper, ZW=F: Wheat, ZC=F: Corn
    tickers = ["HG=F", "ZW=F", "ZC=F"]
    try:
        data = yf.download(tickers, period="1y", progress=False, auto_adjust=True)['Close']
        return data.iloc[-1]
    except Exception as e:
        print(f"Error fetching Commodity prices: {e}")
        return None

def fetch_us_energy_production():
    """
    Fetches U.S. Crude Oil Production Proxy from FRED.
    Series: IPG211111CN (Industrial Production: Mining: Crude Oil, Index 2017=100)
    Note: MCRFPUS2 (Barrels/Day) was returning 404, so using IndPro Index as proxy.
    """
    series_id = 'IPG211111CN'
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text), index_col=0, parse_dates=True)
        return df.iloc[-1]
    except Exception as e:
        print(f"Error fetching US Energy Production: {e}")
        return None

def fetch_module_3_data():
    print("Fetching Module 3 Data (Physical Economy)...")

    # 1. Energy-Value of Money & Oil
    evm_data = fetch_energy_money_data()

    # 2. Key Commodities (Copper, Food)
    commodities = fetch_commodity_prices()

    # 3. U.S. Energy Independence (Production)
    production = fetch_us_energy_production()

    results = {
        'Energy_Money': evm_data,
        'Commodities': commodities,
        'Energy_Production': production
    }

    return results

if __name__ == "__main__":
    data = fetch_module_3_data()

    print("\n--- Module 3: Physical Economy Dashboard ---")

    if data['Energy_Money']:
        print(f"Oil Price (WTI): ${data['Energy_Money']['Oil_Price']:.2f}")
        print(f"Energy-Value of Money: {data['Energy_Money']['Energy_Value']:.2f} Barrels/Bond")

    if data['Commodities'] is not None:
        print(f"Copper Price: ${data['Commodities'].get('HG=F', 'N/A'):.2f}")
        print(f"Wheat Price: ${data['Commodities'].get('ZW=F', 'N/A'):.2f}")
        print(f"Corn Price: ${data['Commodities'].get('ZC=F', 'N/A'):.2f}")

    if data['Energy_Production'] is not None:
        val = data['Energy_Production'].iloc[0]
        date = data['Energy_Production'].name.strftime('%Y-%m')
        print(f"US Crude Oil Production Index ({date}): {val:.2f} (2017=100)")
