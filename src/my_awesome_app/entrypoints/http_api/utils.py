import json
from decimal import Decimal
from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response


encoder_functions = {
    Decimal: lambda v: f'{v:.32f}',
}


def to_json_response(content: Any, **response_kwargs):
    jsonable_content = jsonable_encoder(content, custom_encoder=encoder_functions)
    json_str = json.dumps(jsonable_content)
    return Response(content=json_str, media_type='application/json', **response_kwargs)
