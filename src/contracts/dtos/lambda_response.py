from starlette import status

from rowantree.contracts import BaseModel


class LambdaResponse(BaseModel):
    status_code: status
    body: str
