from typing import List

from api_utils.api_resource.api_response import JsonApiResponsePayload


class ApiPacketTypesListResponse(JsonApiResponsePayload):
    packet_types: List[str]
