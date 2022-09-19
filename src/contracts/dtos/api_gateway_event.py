from typing import Optional

from rowantree.contracts import BaseModel


class ApiGatewayEventRequestContext(BaseModel):
    resource_path: str
    http_method: str


class ApiGatewayEventHeaders(BaseModel):
    accept: str
    Authorization: Optional[str]


# https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html#apigateway-example-event
# https://github.com/awsdocs/aws-lambda-developer-guide/blob/main/sample-apps/nodejs-apig/event.json
class ApiGatewayEvent(BaseModel):
    resource: str
    path: str
    http_method: str
    headers: ApiGatewayEventHeaders
    request_context: ApiGatewayEventRequestContext

