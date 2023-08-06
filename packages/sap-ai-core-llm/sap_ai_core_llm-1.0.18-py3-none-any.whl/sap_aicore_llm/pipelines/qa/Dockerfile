FROM python:3.11

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN mkdir -p /app/src

# Build from source
COPY *pipelines/qa/src/index.py /app/src/index.py
COPY *pipelines/qa/src/query.py /app/src/query.py
COPY *pipelines/qa/requirements.txt /app/src/requirements.txt

# Build from package
COPY *sap_aicore_llm/pipelines/qa/src/index.py /app/src/index.py
COPY *sap_aicore_llm/pipelines/qa/src/query.py /app/src/query.py
COPY *sap_aicore_llm/pipelines/qa/requirements.txt /app/src/requirements.txt

COPY sap_aicore_llm /app/src/sap_aicore_llm

# Metaflow fix
RUN mkdir -p /app/metaflow && cp -r /app/src/sap_aicore_llm /app/metaflow/sap_aicore_llm

RUN mkdir nonexistent && chgrp -R 65534 /app /nonexistent || true && \
    chmod -R 777 /app /nonexistent || true

RUN pip3 install -r /app/src/requirements.txt

WORKDIR /app
