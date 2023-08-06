import os

COMPLETION_ENDPOINT = "/v1/predict?"


def get_completions_url(url):
    if isinstance(url, str) and url.endswith(COMPLETION_ENDPOINT):
        return url
    return url.rstrip('/?') + COMPLETION_ENDPOINT
