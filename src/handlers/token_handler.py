import json
import logging
import traceback
from typing import Union

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

    try:
        auth_request: AuthenticateUserRequest = AuthenticateUserRequest.parse_obj(parse_form_data(event=event))
        logging.error(auth_request)
        request: OAuth2PasswordRequestForm = OAuth2PasswordRequestForm(
            username=auth_request.username, password=auth_request.password, scope="", grant_type="password"
        )
        logging.error(request)
        response: Token = token_controller.execute(request=request)
        logging.error(response)
        return LambdaResponse(status_code=status.HTTP_200_OK, body=response.json(by_alias=True)).dict(by_alias=True)

    except HTTPException as error:
        message_dict: dict[str, Union[dict, str]] = {
            "statusCode": error.status_code,
            "traceback": traceback.print_exc(),
            "error": str(error),
        }
        message: str = json.dumps(message_dict)
        logging.error(message)
        # raise error from error
        return LambdaResponse(status_code=error.status_code, body=message).dict(by_alias=True)
    except Exception as error:
        message_dict: dict[str, Union[dict, str]] = {
            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "traceback": traceback.print_exc(),
            "error": str(error),
        }
        message: str = json.dumps(message_dict)
        logging.error(message)
        # raise error from error
        return LambdaResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, body=message).dict(by_alias=True)
