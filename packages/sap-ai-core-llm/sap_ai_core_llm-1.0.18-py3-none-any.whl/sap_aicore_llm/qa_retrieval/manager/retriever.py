from langchain.chains import RetrievalQA

from sap_aicore_llm.qa_retrieval.model import EmbeddingModelFactory, CompletionModelFactory
from sap_aicore_llm.qa_retrieval.storage import VectorStoreFactory
import sap_aicore_llm.qa_retrieval.config as cfg

embedding_model_factory = EmbeddingModelFactory()
completion_model_factory = CompletionModelFactory()
vector_store_factory = VectorStoreFactory()


class RetrievalManager:
    def __init__(self):
        embedding_model = embedding_model_factory.get_model(cfg.EMBEDDING_MODEL,
                                                            cfg.EMBEDDING_MODEL_API_BASE,
                                                            cfg.EMBEDDING_MODEL_API_KEY,
                                                            cfg.AICORE_AUTH_URL,
                                                            cfg.AICORE_CLIENT_ID,
                                                            cfg.AICORE_CLIENT_SECRET)

        completion_model = completion_model_factory.get_model(cfg.COMPLETION_MODEL,
                                                              cfg.COMPLETION_MODEL_API_BASE,
                                                              cfg.COMPLETION_MODEL_API_KEY,
                                                              cfg.AICORE_AUTH_URL,
                                                              cfg.AICORE_CLIENT_ID,
                                                              cfg.AICORE_CLIENT_SECRET)

        retriever = vector_store_factory.get_client(cfg.VECTOR_STORE,
                                                    cfg.VECTOR_STORE_SCHEMA,
                                                    cfg.VECTOR_STORE_URL,
                                                    embedding_model).as_retriever()

        self.chain = RetrievalQA.from_llm(llm=completion_model,
                                          retriever=retriever,
                                          return_source_documents=True)

    def handle_query(self, user_query: str):
        result = {}
        output = self.chain({"query": user_query})
        result['response'] = output["result"]
        source_documents = output["source_documents"]
        result['source_documents'] = [doc.dict() for doc in source_documents]
        return result
