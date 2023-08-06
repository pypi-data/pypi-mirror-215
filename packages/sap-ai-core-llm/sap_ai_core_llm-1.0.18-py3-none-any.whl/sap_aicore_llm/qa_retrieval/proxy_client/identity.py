import time
from functools import lru_cache, wraps
from http.client import HTTPException
import requests

CACHE_TOKEN_TIMEOUT = 3600


def get_token(auth_url, client_id, client_secret):
    """Get a token from XSUAA.
    :param auth_url: URL of the XSUAA service
    :param client_id: Client ID of the service instance
    :param client_secret: Client secret of the service instance
    :return: Access token
    """
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }
    print(
        f"Requesting token from {auth_url}/oauth/token?grant_type=client_credentials")
    response = requests.post(
        auth_url + "/oauth/token?grant_type=client_credentials", data=data, timeout=5)
    if response.status_code == 200:
        token_data = response.json()
        return token_data['access_token']
    raise HTTPException(
        f"Failed to get token from {auth_url}: {response.status_code} {response.text}")


def _lru_cache_timeout(timeout=60):
    caching_times = []

    def wrapper(func):

        @lru_cache()
        def f_cached(_time, *args, **kwargs):
            return func(*args, **kwargs)

        @wraps(func)
        def f_wrapped(*args, _uncached=False, **kwargs):
            _time = time.time()
            if len(caching_times) == 0:
                caching_times.append(_time)
            elif (_time - caching_times[0]) > timeout or _uncached:
                caching_times[0] = _time
            return f_cached(caching_times[0], *args, **kwargs)

        return f_wrapped

    return wrapper


get_token_cached = _lru_cache_timeout(CACHE_TOKEN_TIMEOUT)(get_token)
