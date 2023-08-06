from typing import Dict
from ul_api_utils.api_resource.api_response import JsonApiResponsePayload


class ApiFullTranslationCacheResponse(JsonApiResponsePayload):
    __root__: Dict[str, Dict[str, str]]


class ApiLangTranslationCacheResponse(JsonApiResponsePayload):
    __root__: Dict[str, str]
