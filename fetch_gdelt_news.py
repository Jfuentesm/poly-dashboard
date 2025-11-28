import requests
import json
import urllib.parse

def fetch_gdelt_mentions():
    # GDELT Doc API 2.0
    base_url = "https://api.gdeltproject.org/api/v2/doc/doc"

    # GDELT requires specific quoting for OR.
    # Try simple query first without OR to verify.
    queries = {
        "Tariffs": 'tariffs',
        "Protectionism": '(tariffs OR protectionism)'
    }

    print("Fetching GDELT News Mentions (Last 24 Hours)...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    for label, query in queries.items():
        params = {
            'query': f'{query} sourcelang:eng',
            'mode': 'artlist',
            'maxrecords': 1,
            'format': 'json',
            'timespan': '1d'
        }

        try:
            response = requests.get(base_url, params=params, headers=headers)

            try:
                data = response.json()
                if 'articles' in data and len(data['articles']) > 0:
                    print(f"Topic '{label}': Successfully fetched articles.")
                    print(f"Sample Title: {data['articles'][0]['title']}")
                else:
                    print(f"Topic '{label}': No articles found.")
            except json.JSONDecodeError:
                print(f"Topic '{label}': Failed to decode JSON. Response text preview:")
                print(response.text[:200])

        except Exception as e:
            print(f"Error fetching GDELT for {label}: {e}")

if __name__ == "__main__":
    fetch_gdelt_mentions()
