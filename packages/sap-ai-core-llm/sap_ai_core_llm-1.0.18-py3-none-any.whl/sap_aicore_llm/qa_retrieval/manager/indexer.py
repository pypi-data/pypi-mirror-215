import logging
from langchain.document_loaders import DirectoryLoader, TextLoader

from sap_aicore_llm.qa_retrieval.model import EmbeddingModelFactory
from sap_aicore_llm.qa_retrieval.storage import VectorStoreFactory
import sap_aicore_llm.qa_retrieval.config as cfg

embedding_model_factory = EmbeddingModelFactory()
vector_store_factory = VectorStoreFactory()


class IndexingManager:
    def __init__(self):
        self.embedding_model = embedding_model_factory.get_model(cfg.EMBEDDING_MODEL,
                                                                 cfg.EMBEDDING_MODEL_API_KEY,
                                                                 cfg.EMBEDDING_MODEL_API_BASE,
                                                                 cfg.AICORE_CLIENT_ID,
                                                                 cfg.AICORE_CLIENT_SECRET,
                                                                 cfg.AICORE_AUTH_URL)

        self.db = vector_store_factory.get_client(cfg.VECTOR_STORE,
                                                    cfg.VECTOR_STORE_SCHEMA,
                                                    cfg.VECTOR_STORE_URL,
                                                    self.embedding_model)
        self.logging = logging.getLogger(__name__)

    def upsert(self, documents_path: str, **kwargs):
        loader = DirectoryLoader(
            documents_path, loader_cls=TextLoader, recursive=True)

        texts = loader.load()

        self.db.add_documents(texts, embedding=self.embedding_model, **kwargs)
