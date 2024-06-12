import requests
from itertools import cycle

proxies = [
    'http://51.158.68.68:8811',
    'http://51.79.50.31:9300',
    'http://198.50.251.188:8080',
    # other proxies
]

proxy_cycle = cycle(proxies)


def get_proxy():
    return next(proxy_cycle)


def make_request_with_proxy(url, headers=None, params=None):
    proxy = get_proxy()
    try:
        response = requests.get(url, headers=headers, params=params,
                                proxies={"http": proxy, "https": proxy}, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {url} with proxy {proxy}: {e}")
        return None
