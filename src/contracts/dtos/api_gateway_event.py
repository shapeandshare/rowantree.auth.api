from rowantree.contracts import BaseModel
from src.contracts.dtos.header_type import HeaderType


class ApiGatewayEvent(BaseModel):
    body: str
    headers: dict[HeaderType, str]
