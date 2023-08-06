import os
import pathlib
from metaflow import FlowSpec, step, argo, environment, Parameter

from sap_aicore_llm.qa_retrieval import IndexingManager


DATA_DIR = str(pathlib.Path('/app/data'))


class IndexUpsert(FlowSpec):
    input_artifacts = [
        {
            'name': 'data',
            'path': DATA_DIR,
            'archive': {
                'none': {}
            }
        }
    ]

    @environment(vars={
        'VECTOR_STORE': 'redis',
        'VECTOR_STORE_URL': 'redis://<ip>:6379',
        'EMBEDDING_MODEL': 'sentence-transformers/all-MiniLM-L6-v2',
        'EMBEDDING_MODEL_API_BASE': '<proxy deployment inference url>',
    })
    @argo(input_artifacts=input_artifacts,
          labels={"ai.sap.com/resourcePlan": "starter"})
    @step
    def start(self):
        indexer = IndexingManager()
        indexer.upsert(DATA_DIR)
        self.next(self.end)

    @step
    def end(self):
        # necessary to end the flow
        pass

if __name__ == '__main__':
    IndexUpsert()
