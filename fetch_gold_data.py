import requests
import json

def fetch_gold_data():
    """
    Fetches World Bank Gold data for China.
    Returns:
        dict: {'value': float (Trillions), 'year': str, 'source': str} or None.
    """
    print("Fetching World Bank Data (Total Reserves incl. Gold) for China...")
    url = "https://api.worldbank.org/v2/country/CHN/indicator/FI.RES.TOTL.CD?format=json&per_page=10"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if len(data) > 1 and len(data[1]) > 0:
            latest_valid = None
            for entry in data[1]:
                if entry['value'] is not None:
                    latest_valid = entry
                    break

            if latest_valid:
                return {
                    'value': float(latest_valid['value']) / 1e12, # Convert to Trillions
                    'year': latest_valid['date'],
                    'source': "World Bank (Indicator FI.RES.TOTL.CD)"
                }
    except Exception as e:
        print(f"Error fetching World Bank data: {e}")

    return None

if __name__ == "__main__":
    result = fetch_gold_data()
    if result:
        print(f"China Total Reserves (incl. Gold): ${result['value']:.2f} Trillion")
        print(f"Year: {result['year']}")
        print(f"Source: {result['source']}")
    else:
        print("No valid data found.")
