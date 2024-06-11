import os
import requests
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')


def test_pexels_api(query, per_page=10, page=1):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page={per_page}&page={page}"
    headers = {
        'Authorization': PEXELS_API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Total:", data['total_results'])
        for idx, photo in enumerate(data['photos'], 1):
            print(f"{idx}. Fotoğraf URL: {photo['src']['large']}")
            print(f"   Desc: {photo['alt']}\n")
    else:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    test_pexels_api("ananas")
