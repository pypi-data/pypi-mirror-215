from typing import List

from api_utils.api_resource.api_response import JsonApiResponsePayload


class ApiProtocolTypesListResponse(JsonApiResponsePayload):
    protocol_types: List[str]
