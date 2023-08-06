import os

# use /app/model/all-MiniLM-L6-v2 to use the pre-downloaded model
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
EMBEDDING_MODEL_API_KEY = os.getenv('EMBEDDING_MODEL_API_KEY')
EMBEDDING_MODEL_API_BASE = os.getenv('EMBEDDING_MODEL_API_BASE')

COMPLETION_MODEL = os.getenv('COMPLETION_MODEL', 'gpt-4')
COMPLETION_MODEL_API_KEY = os.getenv('COMPLETION_MODEL_API_KEY')
COMPLETION_MODEL_API_BASE = os.getenv('COMPLETION_MODEL_API_BASE')

VECTOR_STORE = os.getenv('VECTOR_STORE', 'redis')
VECTOR_STORE_SCHEMA = os.getenv('VECTOR_STORE_SCHEMA', "langchain")
VECTOR_STORE_URL = os.getenv('VECTOR_STORE_URL', 'redis://localhost:6379')

AICORE_CLIENT_ID = os.getenv('AICORE_CLIENT_ID', None)
AICORE_CLIENT_SECRET = os.getenv('AICORE_CLIENT_SECRET', None)
AICORE_AUTH_URL = os.getenv('AICORE_AUTH_URL', None)

LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
