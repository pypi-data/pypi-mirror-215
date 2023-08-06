from sap_aicore_llm.qa_retrieval.proxy_client.identity import get_token_cached

from .proxy_api_engine_resource import ProxyEngineAPIResource
from sap_aicore_llm.qa_retrieval.proxy_client import get_completions_url


class ProxyChatCompletion(ProxyEngineAPIResource):
    engine_required = False
    OBJECT_NAME = "chat.completions"

    @classmethod
    def create(cls, *args,
               api_base=None,
               token=None,
               auth_url=None,
               client_id=None,
               client_secret=None,
               refresh_token=False, **kwargs):
        """Create a chat completion.
        :param api_base: URL of the Proxy OpenAI Proxy service
        :param token: Proxy OpenAI Proxy token. Provide either token or auth_url, client_id and client_secret
        :param auth_url: Authentication URL of the service instance
        :param client_id: Client ID of the service instance
        :param client_secret: Client secret of the service instance
        :param refresh_token: If True, pulls a new token given auth_url, client_id and client_secret
        :param kwargs: Additional parameters to pass to the API
        :return: The completion response
        """
        return _create(cls, *args,
                       api_base=api_base,
                       token=token,
                       auth_url=auth_url,
                       client_id=client_id,
                       client_secret=client_secret,
                       refresh_token=refresh_token,
                       **kwargs)


class ProxyCompletion(ProxyEngineAPIResource):
    engine_required = False
    OBJECT_NAME = "completions"

    @classmethod
    def create(cls, *args,
               api_base=None,
               token=None,
               auth_url=None,
               client_id=None,
               client_secret=None,
               refresh_token=False, **kwargs):
        """Create a completion.
        :param api_base: URL of the Proxy OpenAI Proxy service
        :param token: Proxy OpenAI Proxy token. Provide either token or auth_url, client_id and client_secret
        :param auth_url: Authentication URL of the service instance
        :param client_id: Client ID of the service instance
        :param client_secret: Client secret of the service instance
        :param refresh_token: If True, pulls a new token given auth_url, client_id and client_secret
        :param kwargs: Additional parameters to pass to the API
        :return: The completion response
        """
        return _create(cls, *args,
                       api_base=api_base,
                       token=token,
                       auth_url=auth_url,
                       client_id=client_id,
                       client_secret=client_secret,
                       refresh_token=refresh_token,
                       **kwargs)


def _create(cls, *args,
            api_base=None,
            token=None,
            auth_url=None,
            client_id=None,
            client_secret=None,
            refresh_token=False, **kwargs):
    kwargs['api_base'] = get_completions_url(api_base)

    if token is not None and refresh_token:
        raise ValueError('Cannot pass token and refresh_token=True.')

    if token is None and kwargs.get('headers') is None:
        try:
            token = get_token_cached(auth_url,
                                     client_id,
                                     client_secret,
                                     _uncached=refresh_token)
        except ValueError as exc:
            raise ValueError(
                'Either provide token or [auth_url, client_id and client_secret] for automatic token retrieval.') from exc

    kwargs['headers'] = kwargs.get('headers') or ProxyEngineAPIResource.build_header(token)

    return ProxyEngineAPIResource.create(cls, *args, **kwargs)
