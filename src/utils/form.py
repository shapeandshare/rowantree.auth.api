import json
import logging
import traceback
from typing import Union

from requests_toolbelt.multipart import decoder
from starlette import status
from starlette.exceptions import HTTPException

from src.contracts.dtos.api_gateway_event import ApiGatewayEvent
from src.contracts.dtos.form_response import FormResponse


def demand_content_type(headers: dict[str, str]) -> str:
    for key in headers.keys():
        if key.lower() == "content-type":
            return headers[key]
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to find content type in request headers"
    )


def parse_form_data(event: ApiGatewayEvent) -> dict[str, str]:
    try:
        encoding: str = "utf-8"
        multipart_data = decoder.MultipartDecoder.from_response(
            FormResponse(
                content=bytes(event.body, encoding), headers={"content-type": demand_content_type(event.headers)}
            )
        )

        form_values: dict[str, str] = {}
        for part in multipart_data.parts:
            entry_name: str = (
                part.headers[b"Content-Disposition"].decode(encoding).split(";")[1].split("=")[1].replace('"', "")
            )
            entry_value: str = part.content.decode(encoding)
            form_values[entry_name] = entry_value

        return form_values
    except HTTPException as error:
        raise error from error
    except Exception as error:
        message_dict: dict[str, Union[dict, str]] = {
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "traceback": traceback.format_exc(),
            "error": str(error),
            "detail": "Unable to parse form data",
        }
        message: str = json.dumps(message_dict)
        logging.error(message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to parse form data") from error
