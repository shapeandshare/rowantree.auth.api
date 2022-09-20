from requests_toolbelt.multipart import decoder

from src.contracts.dtos.form_response import FormResponse


def parse_form_data(event: dict) -> dict[str, str]:
    encoding: str = "utf-8"
    multipart_data = decoder.MultipartDecoder.from_response(
        FormResponse(content=bytes(event["body"], encoding), headers={"content-type": event["headers"]["Content-Type"]})
    )

    form_values: dict[str, str] = {}
    for part in multipart_data.parts:
        entry_name: str = (
            part.headers[b"Content-Disposition"].decode(encoding).split(";")[1].split("=")[1].replace('"', "")
        )
        entry_value: str = part.content.decode(encoding)
        form_values[entry_name] = entry_value

    return form_values
