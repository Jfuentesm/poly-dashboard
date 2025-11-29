import pandas as pd
import requests
import io
from fetch_gdelt_news import fetch_gdelt_mentions

# FRED Series
FRED_SERIES = {
    'TradeBalance_Total': 'BOPGSTB', # Trade Balance: Goods and Services, Balance of Payments Basis
    'Imports_China': 'IMPCH',        # U.S. Imports of Goods by Customs Basis from China
    'Exports_China': 'EXPCH',        # U.S. Exports of Goods by F.A.S. Basis to China
    'Industrial_Production': 'INDPRO' # Industrial Production: Total Index
}

# World Bank Series
WB_SERIES = {
    'GDP_Nominal': 'NY.GDP.MKTP.CD',
    'GDP_PPP': 'NY.GDP.MKTP.PP.CD',
    'Manuf_GDP_Share': 'NV.IND.MANF.ZS' # Manufacturing, value added (% of GDP)
}

def fetch_fred_series(series_id):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text), index_col=0, parse_dates=True)
        return df.iloc[-1]
    except Exception as e:
        print(f"Error fetching FRED {series_id}: {e}")
        return None

def fetch_world_bank_data(indicator, country_code):
    """
    Fetches latest available data from World Bank API.
    """
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if len(data) > 1 and len(data[1]) > 0:
            return data[1][0]
    except Exception as e:
        print(f"Error fetching World Bank {indicator} for {country_code}: {e}")
    return None

def fetch_module_4_data():
    print("Fetching Module 4 Data (Geopolitics)...")

    results = {}

    # 1. Trade Conflict Monitor
    # Calculate US-China Trade Balance
    imp_ch = fetch_fred_series(FRED_SERIES['Imports_China'])
    exp_ch = fetch_fred_series(FRED_SERIES['Exports_China'])

    if imp_ch is not None and exp_ch is not None:
        # Note: Imports/Exports are usually monthly millions. Balance = Exp - Imp
        # Imports are positive numbers in FRED, representing outflow of cash?
        # Usually Trade Balance = Exports - Imports.
        balance_ch = exp_ch.item() - imp_ch.item()
        results['US_China_Trade_Balance'] = balance_ch

    # Total Trade Balance
    results['Trade_Balance_Total'] = fetch_fred_series(FRED_SERIES['TradeBalance_Total'])

    # 2. Industrial Onshoring
    results['Industrial_Production'] = fetch_fred_series(FRED_SERIES['Industrial_Production'])

    # Manufacturing Share of GDP (USA)
    manuf_share = fetch_world_bank_data(WB_SERIES['Manuf_GDP_Share'], 'USA')
    if manuf_share:
        results['Manuf_GDP_Share'] = manuf_share['value']
        results['Manuf_GDP_Share_Year'] = manuf_share['date']

    # 3. U.S. vs China Economic Scale
    for metric_name, indicator in [('GDP_Nominal', WB_SERIES['GDP_Nominal']), ('GDP_PPP', WB_SERIES['GDP_PPP'])]:
        usa = fetch_world_bank_data(indicator, 'USA')
        chn = fetch_world_bank_data(indicator, 'CHN')

        if usa:
            results[f'{metric_name}_USA'] = usa['value']
        if chn:
            results[f'{metric_name}_CHN'] = chn['value']

    # 4. Prevailing Ism (GDELT)
    # We call the existing function
    results['News_Mentions'] = fetch_gdelt_mentions()

    return results

if __name__ == "__main__":
    data = fetch_module_4_data()

    print("\n--- Module 4: Geopolitical Realignment Dashboard ---")

    if 'US_China_Trade_Balance' in data:
        print(f"US-China Trade Balance: ${data['US_China_Trade_Balance']:,.2f} Million")

    if 'Industrial_Production' in data and data['Industrial_Production'] is not None:
         print(f"US Industrial Production Index: {data['Industrial_Production'].item():.2f}")

    if 'Manuf_GDP_Share' in data:
        print(f"US Manufacturing % of GDP ({data.get('Manuf_GDP_Share_Year')}): {data['Manuf_GDP_Share']:.2f}%")

    if 'GDP_Nominal_USA' in data and 'GDP_Nominal_CHN' in data:
        print(f"GDP Nominal - USA: ${data['GDP_Nominal_USA']/1e12:.2f}T, China: ${data['GDP_Nominal_CHN']/1e12:.2f}T")

    if 'GDP_PPP_USA' in data and 'GDP_PPP_CHN' in data:
        print(f"GDP PPP - USA: ${data['GDP_PPP_USA']/1e12:.2f}T, China: ${data['GDP_PPP_CHN']/1e12:.2f}T")

    if 'News_Mentions' in data:
        print(f"News Tracker: {len(data['News_Mentions'])} topics tracked.")
