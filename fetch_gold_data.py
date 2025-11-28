import requests
import json

def fetch_gold_data():
    """
    Attempts to fetch Central Bank Gold data.
    Note: Direct IMF/World Bank APIs often have strict connectivity or complex params.
    This script demonstrates the World Bank fallback.
    """

    # World Bank API: Total Reserves (includes gold, current US$)
    # Indicator: FI.RES.TOTL.CD
    # Country: USA (United States) as a test since World Aggregates seem empty
    # Or CHN (China)

    # We will try China (CHN)
    print("Fetching World Bank Data (Total Reserves incl. Gold) for China...")
    url = "https://api.worldbank.org/v2/country/CHN/indicator/FI.RES.TOTL.CD?format=json&per_page=10"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # WB response is [metadata, [data]]
        if len(data) > 1 and len(data[1]) > 0:
            # Iterate to find first non-null value
            latest_valid = None
            for entry in data[1]:
                if entry['value'] is not None:
                    latest_valid = entry
                    break

            if latest_valid:
                date = latest_valid['date']
                value = latest_valid['value']
                print(f"China Total Reserves (incl. Gold): ${float(value)/1e12:.2f} Trillion")
                print(f"Year: {date}")
                print("Source: World Bank (Indicator FI.RES.TOTL.CD)")
            else:
                print("No valid data found in recent records.")
        else:
            print("No World Bank data returned.")

    except Exception as e:
        print(f"Error fetching World Bank data: {e}")

if __name__ == "__main__":
    fetch_gold_data()
