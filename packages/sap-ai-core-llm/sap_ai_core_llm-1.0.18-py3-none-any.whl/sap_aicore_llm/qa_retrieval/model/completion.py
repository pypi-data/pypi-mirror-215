

class CompletionModelFactory:
    def get_model(self,
                  model_name: str,
                  api_url: str,
                  api_token: str,
                  aicore_auth_url: str,
                  aicore_client_id: str,
                  aicore_client_secret: str):

        if model_name in ["gpt-4", "gpt-35-turbo"]:
            from sap_aicore_llm.qa_retrieval.proxy_client.langchain.openai import ChatProxyOpenAI as Model
        else:
            from sap_aicore_llm.qa_retrieval.proxy_client.langchain.openai import ProxyOpenAI as Model

        return Model(api_base=api_url,
                     token=api_token,
                     auth_url=aicore_auth_url,
                     client_id=aicore_client_id,
                     client_secret=aicore_client_secret)
