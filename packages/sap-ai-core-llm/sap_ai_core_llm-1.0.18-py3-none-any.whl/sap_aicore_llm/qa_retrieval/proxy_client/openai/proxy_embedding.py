import base64
import time

from openai import util
from openai.datalib.numpy_helper import assert_has_numpy
from openai.datalib.numpy_helper import numpy as np
from openai.error import TryAgain
from .proxy_api_engine_resource import ProxyEngineAPIResource
from .proxy_completion import _create


class ProxyEmbedding(ProxyEngineAPIResource):
    engine_required = False
    OBJECT_NAME = "embeddings"

    @classmethod
    def create(cls, *args,
               api_base=None,
               token=None,
               auth_url=None,
               client_id=None,
               client_secret=None,
               refresh_token=False,
               **kwargs):
        """
        Creates a new embedding for the provided input and parameters.
        See https://platform.openai.com/docs/api-reference/embeddings for a list
        of valid parameters.
        """
        start = time.time()
        timeout = kwargs.pop("timeout", None)

        user_provided_encoding_format = kwargs.get("encoding_format", None)

        # If encoding format was not explicitly specified, we opaquely use base64 for performance
        if not user_provided_encoding_format:
            kwargs["encoding_format"] = "base64"

        while True:
            try:
                response = _create(cls,
                                   *args,
                                   api_base=api_base,
                                   token=token,
                                   auth_url=auth_url,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   refresh_token=refresh_token,
                                   **kwargs)

                # If a user specifies base64, we'll just return the encoded string.
                # This is only for the default case.
                if not user_provided_encoding_format:    
                    for data in response.data:
                        # If an engine isn't using this optimization, don't do anything
                        if type(data["embedding"]) == str:
                            assert_has_numpy()
                            data["embedding"] = np.frombuffer(
                                base64.b64decode(data["embedding"]), dtype="float32"
                            ).tolist()
                return response
            except TryAgain as e:
                if timeout is not None and time.time() > start + timeout:
                    raise

                util.log_info("Waiting for model to warm up", error=e)
