from langchain.vectorstores.base import VectorStore
from langchain.embeddings.base import Embeddings


class VectorStoreFactory:
    def get_client(self,
                   vector_store: str,
                   schema: str,
                   url: str,
                   embedding_model: Embeddings) -> VectorStore:
        if vector_store == 'redis':
            from langchain.vectorstores.redis import Redis
            return Redis(url, schema, embedding_model.embed_query)
        else:
            raise NotImplementedError('Vector store {} not implemented'.format(vector_store))
