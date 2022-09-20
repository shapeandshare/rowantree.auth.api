import json
import logging

from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.exceptions import HTTPException

from rowantree.auth.sdk import AuthenticateUserRequest, Token
from rowantree.auth.service.controllers.token import TokenController
from rowantree.auth.service.services.auth import AuthService
from rowantree.auth.service.services.db.dao import DBDAO
from rowantree.auth.service.services.db.utils import WrappedConnectionPool

from src.contracts.dtos.lambda_response import LambdaResponse
from src.utils.form import parse_form_data

# Creating database connection pool, and DAO
wrapped_cnxpool: WrappedConnectionPool = WrappedConnectionPool()
dao: DBDAO = DBDAO(cnxpool=wrapped_cnxpool.cnxpool)
auth_service: AuthService = AuthService(dao=dao)

token_controller: TokenController = TokenController(auth_service=auth_service)


def handler(event, context):
    logging.error(event)
    logging.error(context)

    try:
        auth_request: AuthenticateUserRequest = AuthenticateUserRequest.parse_obj(parse_form_data(event=event))
        request: OAuth2PasswordRequestForm = OAuth2PasswordRequestForm(
            username=auth_request.username, password=auth_request.password
        )
        response: Token = token_controller.execute(request=request)
        return LambdaResponse(status_code=status.HTTP_200_OK, body=response.json(by_alias=True)).dict(by_alias=True)

    except HTTPException as error:
        logging.error(str(error))
        # raise error from error
        return LambdaResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, body=json.dumps(error)).dict(
            by_alias=True
        )
    except Exception as error:
        # Caught all other uncaught errors.
        logging.error(str(error))
        return LambdaResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, body=json.dumps(error)).dict(
            by_alias=True
        )
