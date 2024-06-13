import requests
from itertools import cycle

proxies = [
    'http://43.130.238.86:3128',
    'http://194.67.113.86:3128',
    'http://43.133.160.119:3128',
]

proxy_cycle = cycle(proxies)


def get_proxy():
    return next(proxy_cycle)


def make_request_with_proxy(url, headers=None, params=None):
    proxy = get_proxy()
    try:
        response = requests.get(url, headers=headers, params=params, proxies={"http": proxy, "https": proxy},
                                timeout=10, verify=False)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {url} with proxy {proxy}: {e}")
        return None
