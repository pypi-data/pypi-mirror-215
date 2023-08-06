import os
from huggingface_hub.utils._errors import RepositoryNotFoundError


class EmbeddingModelFactory:
    def get_model(self,
                  model_name: str,
                  api_url: str,
                  api_token: str,
                  aicore_client_id: str,
                  aicore_client_secret: str,
                  aicore_auth_url: str):
        model_name_split = model_name.split('/')
        model_prefix = model_name_split[0]

        if model_prefix == 'sentence-transformers' or os.path.exists(model_name):
            try:
                from langchain.embeddings import HuggingFaceEmbeddings
                return HuggingFaceEmbeddings(model_name=model_name)
            except RepositoryNotFoundError as exc:
                raise ValueError(
                    f"Model {model_name} not found in HuggingFace. Please check the model name.") from exc

        try:
            # Azure OpenAI proxied embedding models
            from sap_aicore_llm.qa_retrieval.proxy_client.langchain.openai import ProxyOpenAIEmbeddings
            return ProxyOpenAIEmbeddings(api_base=api_url,
                                            token=api_token,
                                            auth_url=aicore_auth_url,
                                            client_id=aicore_client_id,
                                            client_secret=aicore_client_secret)
        except Exception as exc:
            raise ValueError(
                f"Model {model_name} not supported. Please check the model name.") from exc
