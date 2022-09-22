from rowantree.contracts import BaseModel


class ApiGatewayEvent(BaseModel):
    body: str
    headers: dict[str, str]
