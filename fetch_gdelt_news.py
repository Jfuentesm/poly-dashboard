import requests
import json
import urllib.parse

def fetch_gdelt_mentions():
    """
    Fetches GDELT article counts (or samples) for specific queries.
    Returns:
        dict: Keys are topics, values are lists of articles or empty list.
    """
    base_url = "https://api.gdeltproject.org/api/v2/doc/doc"

    queries = {
        "Tariffs": 'tariffs',
        "Protectionism": '(tariffs OR protectionism)'
    }

    print("Fetching GDELT News Mentions (Last 24 Hours)...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    results = {}

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
            data = response.json()
            if 'articles' in data and len(data['articles']) > 0:
                results[label] = data['articles']
            else:
                results[label] = []

        except Exception as e:
            print(f"Error fetching GDELT for {label}: {e}")
            results[label] = []

    return results

if __name__ == "__main__":
    data = fetch_gdelt_mentions()
    for label, articles in data.items():
        if articles:
            print(f"Topic '{label}': Successfully fetched articles.")
            print(f"Sample Title: {articles[0]['title']}")
        else:
            print(f"Topic '{label}': No articles found.")
