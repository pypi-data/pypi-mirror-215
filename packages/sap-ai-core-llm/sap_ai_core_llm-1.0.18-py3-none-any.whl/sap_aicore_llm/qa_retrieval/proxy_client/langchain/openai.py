from typing import Dict, Any, Optional
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

from pydantic import root_validator

class ChatProxyOpenAI(ChatOpenAI):
    api_base: Optional[str] = None
    token: Optional[str] = None
    auth_url: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    refresh_token: bool = False

    def __init__(self,
                 api_base=None,
                 token=None,
                 auth_url=None,
                 client_id=None,
                 client_secret=None,
                 refresh_token=False,
                 **kwargs):
        super().__init__(api_base=api_base,
                         token=token,
                         auth_url=auth_url,
                         client_id=client_id,
                         client_secret=client_secret,
                         refresh_token=refresh_token,
                         **kwargs)

    # pylint: disable=no-self-argument
    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:

        from sap_aicore_llm.qa_retrieval.proxy_client.openai import ProxyChatCompletion
        values["client"] = ProxyChatCompletion

        if values["streaming"]:
            raise ValueError('Streaming not support when using the Proxy')
        if values["n"] < 1:
            raise ValueError("n must be at least 1.")
        if values["n"] > 1 and values["streaming"]:
            raise ValueError("n must be 1 when streaming.")
        return values

    @property
    def _default_params(self) -> Dict[str, Any]:
        return {
            **super()._default_params,
            "api_base": self.api_base,
            "auth_url": self.auth_url,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "model": ""
        }


class ProxyOpenAI(OpenAI):
    api_base: Optional[str] = None
    token: Optional[str] = None
    auth_url: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    refresh_token: bool = False

    def __init__(self,
                 api_base=None,
                 token=None,
                 auth_url=None,
                 client_id=None,
                 client_secret=None,
                 refresh_token=False,
                 **kwargs):
        super().__init__(api_base=api_base,
                         token=token,
                         auth_url=auth_url,
                         client_id=client_id,
                         client_secret=client_secret,
                         refresh_token=refresh_token,
                         **kwargs)

    # pylint: disable=no-self-argument
    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        from sap_aicore_llm.qa_retrieval.proxy_client.openai import ProxyCompletion
        values["client"] = ProxyCompletion
        if values["streaming"]:
            raise ValueError('Streaming not support when using the Proxy')
        if values["n"] < 1:
            raise ValueError("n must be at least 1.")
        if values["n"] > 1 and values["streaming"]:
            raise ValueError("n must be 1 when streaming.")
        return values

    @property
    def _default_params(self) -> Dict[str, Any]:
        return {
            **super()._default_params,
            "api_base": self.api_base,
            "auth_url": self.auth_url,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "model": ""
        }

class ProxyOpenAIEmbeddings(OpenAIEmbeddings):
    api_base: Optional[str] = None
    token: Optional[str] = None
    auth_url: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    refresh_token: bool = False

    def __init__(self,
                 api_base=None,
                 token=None,
                 auth_url=None,
                 client_id=None,
                 client_secret=None,
                 refresh_token=False,
                 **kwargs):
        super().__init__(
                         api_base=api_base,
                         token=token,
                         auth_url=auth_url,
                         client_id=client_id,
                         client_secret=client_secret,
                         refresh_token=refresh_token,
                         **kwargs)

    # pylint: disable=no-self-argument
    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        from sap_aicore_llm.qa_retrieval.proxy_client.openai import ProxyEmbedding
        values["client"] = ProxyEmbedding
        return values
