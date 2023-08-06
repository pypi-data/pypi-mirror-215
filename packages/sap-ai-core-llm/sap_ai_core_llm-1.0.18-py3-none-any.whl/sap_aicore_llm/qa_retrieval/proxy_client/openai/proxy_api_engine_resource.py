from openai import util
from openai.api_resources.abstract.engine_api_resource import EngineAPIResource
from openai.openai_response import OpenAIResponse

MAX_TIMEOUT = 20


class ProxyEngineAPIResource(EngineAPIResource):
    OBJECT_NAME = "chat.completions"

    @classmethod
    def create(
        cls,
        api_key=None,
        api_base=None,
        api_type=None,
        request_id=None,
        api_version=None,
        organization=None,
        **params,
    ):
        (
            deployment_id,
            engine,
            timeout,
            stream,
            headers,
            request_timeout,
            typed_api_type,
            requestor,
            url,
            params,
        ) = ProxyEngineAPIResource.prepare_create_request(
            api_key, api_base, api_type, api_version, organization, **params
        )
        response, _, api_key = requestor.request(
            "post",
            url,
            params=params,
            headers=headers,
            stream=stream,
            request_id=request_id,
            request_timeout=request_timeout,
        )

        if stream:
            raise ValueError('Streaming is not yet supported in the Proxy Service.')
        else:
            obj = util.convert_to_openai_object(
                response,
                api_key,
                api_version,
                organization,
                engine=engine,
                plain_old_data=cls.plain_old_data,
            )

            if timeout is not None:
                obj.wait(timeout=timeout or None)

        return obj

    @classmethod
    def prepare_create_request(
        cls,
        api_key=None,
        api_base=None,
        api_type=None,
        api_version=None,
        organization=None,
        **params,
    ):
        # pylint: disable=too-many-function-args
        (deployment_id,
         engine,
         timeout,
         stream,
         headers,
         request_timeout,
         typed_api_type,
         requestor,
         url,
         params) = ProxyEngineAPIResource._EngineAPIResource__prepare_create_request(api_key, api_base, api_type, api_version, organization, **params)
        # Necessary for Proxy Proxy
        if deployment_id:
            params['deployment_id'] = deployment_id

        return (deployment_id,
                engine,
                timeout,
                stream,
                headers,
                request_timeout,
                typed_api_type,
                requestor,
                url,
                params)

    @staticmethod
    def build_header(token):
        return {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
            'AI-Resource-Group': 'default'
        }
